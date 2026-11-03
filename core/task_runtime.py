"""Task manifest qualification; never executes model/evaluator or requests sealed labels."""
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
    if set(references) != {"data_manifest", "split_manifest", "evaluator"}:
        raise ContractError("TaskSpec references must contain only data/split metadata and evaluator")
    if any(not isinstance(name, str) or not isinstance(ref, str) or not ref.strip() for name, ref in references.items()):
        raise ContractError("reference names and paths must be text")
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
    expected_hashes = spec.get("expected_sha256", {})
    if not isinstance(expected_hashes, dict):
        raise ContractError("expected_sha256 must be a map of reference name to hash")
    for name, expected in expected_hashes.items():
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
            "protected_snapshot_frozen": set(expected_hashes) == set(fingerprints),
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
    if not audit["protected_snapshot_frozen"]:
        raise ContractError("TaskSpec has no complete pinned protected-file SHA-256 set; run task-pin first")
    spec = json.loads(_inside(Path(root), spec_ref).read_text(encoding="utf-8"))
    for field in ("task_id", "protocol_id", "dataset_version", "evaluator_version"):
        if run[field] != spec[field]:
            raise ContractError("Run and TaskSpec mismatch: " + field)
    if sorted(run["legal_inputs"]) != sorted(spec["legal_inputs"]):
        raise ContractError("Run legal_inputs differ from TaskSpec")


def audit_run_reproducibility(root: Path, run_path: str) -> dict:
    """Describe replay metadata gaps; does not rerun experiment or certify reproducibility."""
    from core.contracts import validate_run
    root=Path(root)
    obj=validate_run(json.loads(_inside(root, run_path).read_text(encoding="utf-8")))
    if obj["status"] != "VALID":
        return {"status":"NOT_A_VALID_RUN", "run_id":obj["run_id"], "gaps":["no valid measured Run"]}
    refs=obj["artifact_refs"]
    hashes={k:_hash_file(_inside(root,p)) for k,p in refs.items()}
    execution=obj.get("execution")
    gaps=[]
    if not isinstance(execution,dict):
        execution={}
    for name in ("command","git_commit","python_version","environment_ref"):
        if not isinstance(execution.get(name),str) or not execution[name].strip():
            gaps.append("execution."+name)
    if type(execution.get("seed")) is not int:
        gaps.append("execution.seed")
    if isinstance(execution.get("environment_ref"),str) and execution["environment_ref"].strip():
        hashes["environment"]=_hash_file(_inside(root,execution["environment_ref"]))
    if not obj.get("budget_basis"):
        gaps.append("budget_basis")
    if obj.get("task_spec_ref") and obj.get("task_spec_sha256"):
        check_run_task_alignment(root,obj)
        hashes["task_spec"]=_hash_file(_inside(root,obj["task_spec_ref"]))
    else:
        gaps.append("task_spec_ref+sha256")
    return {"status":"METADATA_COMPLETE_NOT_REPRODUCED" if not gaps else "PROVENANCE_PARTIAL",
            "run_id":obj["run_id"],"fingerprints":hashes,"gaps":gaps,
            "note":"No model, evaluator or scientific inference was executed; environment equivalence needs real replay."}


def pin_task(root: Path, spec_path: str, output_path: str) -> dict:
    """Explicitly write a *new* TaskSpec with protected reference SHA-256 values."""
    root=Path(root)
    # Read and qualify only metadata and evaluator (no training or sealed labels).
    audit=qualify_task(root,spec_path)
    original=validate_task_spec(json.loads(_inside(root,spec_path).read_text(encoding="utf-8")))
    pinned=dict(original)
    pinned["expected_sha256"]=audit["fingerprints"]
    base=root.resolve()
    dest=(base/output_path).resolve()
    if not dest.is_relative_to(base):
        raise ContractError("pinned TaskSpec output cannot be outside project root")
    dest.parent.mkdir(parents=True,exist_ok=True)
    try:
        with dest.open("x",encoding="utf-8") as out:
            json.dump(pinned,out,ensure_ascii=False,sort_keys=True,indent=2)
            out.write("\n")
    except FileExistsError as exc:
        raise ContractError("pinned TaskSpec already exists; choose a versioned path") from exc
    return {"status":"REFERENCE_HASHES_PINNED_NOT_SCIENTIFICALLY_VERIFIED",
            "path":dest.relative_to(base).as_posix(), "sha256":_hash_file(dest),
            "referenced_sha256":audit["fingerprints"],
            "note":"Check TaskSpec correctness and actual user authorization before fitting."}
