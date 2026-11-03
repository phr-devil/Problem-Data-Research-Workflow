"""Read-only task qualification; never runs the model/evaluator or opens sealed labels."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from core.contracts import ContractError

def _required(obj: dict, *fields: str) -> None:
    for field in fields:
        if not isinstance(obj.get(field), str) or not obj[field].strip():
            raise ContractError(f"TaskSpec missing nonempty {field}")

def _list(obj: dict, key: str, *, required: bool = True) -> list[str]:
    values = obj.get(key)
    if not isinstance(values, list) or (required and not values) or any(
        not isinstance(v, str) or not v.strip() for v in values
    ):
        raise ContractError(f"TaskSpec {key} must contain nonempty strings")
    return values

def validate_task_spec(value: dict) -> dict:
    """A TaskSpec is a plan for evidence, not proof that a dataset or metric is valid."""
    if not isinstance(value, dict):
        raise ContractError("TaskSpec must be a JSON object")
    _required(value, "task_id", "protocol_id", "dataset_version",
              "target_definition", "label_provenance", "prediction_time",
              "group_key", "independent_unit", "metric", "metric_direction",
              "evaluator_version")
    if value["metric_direction"] not in {"max", "min"}:
        raise ContractError("metric_direction must be max/min")
    _list(value, "legal_inputs")
    editable = _list(value, "editable_paths")
    protected = _list(value, "protected_paths")
    if set(editable) & set(protected):
        raise ContractError("editable_paths and protected_paths overlap")
    references = value.get("references")
    if not isinstance(references, dict):
        raise ContractError("TaskSpec needs references for manifests and evaluator")
    _required(references, "data_manifest", "split_manifest", "evaluator")
    for p in protected:
        if p not in references.values():
            raise ContractError("protected path not backed by referenced file: " + p)
    checks = value.get("correctness_checks")
    if not isinstance(checks, list) or not checks or any(
        not isinstance(x, str) or not x.strip() for x in checks
    ):
        raise ContractError("TaskSpec requires at least one observable correctness check")
    return value

def _inside(root: Path, relative_path: str) -> Path:
    base = root.resolve()
    path = (base / relative_path).resolve()
    if not path.is_relative_to(base) or not path.is_file():
        raise ContractError("missing or outside project root: " + relative_path)
    return path

def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as src:
        for chunk in iter(lambda: src.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def qualify_task(root: Path, task_spec_path: str) -> dict:
    """Check file presence, fingerprints, and optional development split disjointness.

    This NEVER executes the evaluator, fits data or accesses sealed holdout labels.
    """
    root = Path(root)
    spec_file = _inside(root, task_spec_path)
    try:
        spec = validate_task_spec(json.loads(spec_file.read_text(encoding="utf-8")))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError("TaskSpec is not UTF-8 JSON") from exc
    fingerprints = {name: _hash_file(_inside(root, ref))
                    for name, ref in spec["references"].items()}
    for name, expected in spec.get("expected_sha256", {}).items():
        if name not in fingerprints or fingerprints[name] != expected:
            raise ContractError(f"stale protected input fingerprint: {name}")
    split = json.loads(_inside(root, spec["references"]["split_manifest"]).read_text(encoding="utf-8"))
    if not isinstance(split, dict):
        raise ContractError("split manifest must be an object")
    checks = []
    for train, dev in (("train_ids", "dev_ids"), ("train_groups", "dev_groups")):
        if train in split and dev in split:
            a, b = split[train], split[dev]
            if not isinstance(a, list) or not isinstance(b, list) or any(not isinstance(x, (str,int)) for x in a+b):
                raise ContractError(f"invalid split list: {train}/{dev}")
            if len(a) != len(set(a)) or len(b) != len(set(b)):
                raise ContractError(f"duplicate entries in {train}/{dev}")
            if set(a) & set(b):
                raise ContractError(f"train/dev leakage: {train}/{dev}")
            checks.append(f"{train}/{dev}:DISJOINT")
        else:
            checks.append(f"{train}/{dev}:UNKNOWN")
    return {"qualification": "STRUCTURAL_PRECHECK_ONLY",
            "task_id": spec["task_id"], "protocol_id": spec["protocol_id"],
            "task_spec_sha256": _hash_file(spec_file),
            "fingerprints": fingerprints, "split_checks": checks,
            "not_verified": ["label truth", "causal availability", "evaluator semantics",
                             "statistical validity", "scientific novelty", "authorization"]}

def check_run_task_alignment(root: Path, run: dict) -> None:
    """Optional linkage for newer Runs. Older v1.4 Runs are still valid."""
    spec_ref = run.get("task_spec_ref")
    expected = run.get("task_spec_sha256")
    if spec_ref is None and expected is None:
        return
    if not isinstance(spec_ref, str) or not isinstance(expected, str):
        raise ContractError("task_spec_ref and task_spec_sha256 must be paired")
    audit = qualify_task(root, spec_ref)
    if audit["task_spec_sha256"] != expected:
        raise ContractError("TaskSpec changed since Run was planned")
    for field in ("task_id", "protocol_id", "dataset_version", "evaluator_version"):
        spec = json.loads(_inside(Path(root), spec_ref).read_text(encoding="utf-8"))
        if run[field] != spec[field]:
            raise ContractError("Run and TaskSpec mismatch: " + field)
    if sorted(run["legal_inputs"]) != sorted(spec["legal_inputs"]):
        raise ContractError("Run legal_inputs differ from TaskSpec")
