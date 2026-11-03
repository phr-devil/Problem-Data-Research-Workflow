"""Optional external Forge DEV metric verification, without importing its 'core'.

RWF runs in an isolated subprocess for module name compatibility. The PD-RW
legacy evidence ledger remains readable; the caller opts in at key DEV Runs.
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

from core.contracts import ContractError


def _inside(root: Path, path: Path) -> Path:
    root = root.resolve()
    target = (root / path).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        raise ContractError("PD-RW Run must exist under its project root")
    return target


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for part in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(part)
    return h.hexdigest()


def verify_with_forge(
    pd_root: Path, pd_run: Path, forge_repo: Path, forge_project: Path,
    forge_run: Path, metric: str,
) -> dict:
    """Perform RWF's independent raw DEV verification; no fitting or writes."""
    pd_root, forge_repo = pd_root.resolve(), forge_repo.resolve()
    pd_path = _inside(pd_root, pd_run)
    if not (forge_repo / "adapters" / "pd_rw_bridge.py").is_file():
        raise ContractError("RWF PD-RW bridge missing; use the current RWF checkout")
    if not metric or not metric.strip():
        raise ContractError("metric required")
    project_path = forge_project.resolve()
    run_path = (forge_run if forge_run.is_absolute()
                else project_path / forge_run).resolve()
    cmd = [
        sys.executable, "-m", "adapters.pd_rw_bridge",
        "--project", str(project_path),
        "--forge-run", str(run_path),
        "--pd-root", str(pd_root),
        "--pd-run", str(pd_path),
        "--metric", metric,
    ]
    try:
        process = subprocess.run(
            cmd, cwd=forge_repo, capture_output=True, text=True,
            timeout=120, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise ContractError("Forge verification timed out; no verified result") from exc
    if process.returncode:
        detail = process.stderr.strip()[:600]
        raise ContractError("Forge DEV verification failed: " + detail)
    try:
        evidence = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise ContractError("Forge returned no valid verification JSON") from exc
    if (not isinstance(evidence, dict)
            or evidence.get("status") != "METRIC_VERIFIED_DEV_ONLY"
            or evidence.get("metric") != metric
            or evidence.get("pd_run_sha256") != _sha(pd_path)):
        raise ContractError("Forge handoff receipt does not match current PD-RW Run")
    for key in ("forge_run_sha256", "prediction_sha256"):
        if (not isinstance(evidence.get(key), str)
                or len(evidence[key]) != 64
                or any(c not in "0123456789abcdefABCDEF" for c in evidence[key])):
            raise ContractError("Forge handoff receipt missing real SHA-256: " + key)
    metric_value = evidence.get("recomputed_value")
    if (type(metric_value) not in (float, int)
            or not math.isfinite(metric_value)):
        raise ContractError("Forge handoff receipt lacks finite recomputed metric")
    return {
        "verification": evidence["status"],
        "run": str(pd_path),
        "metric": metric,
        "value": evidence.get("recomputed_value"),
        "evidence": evidence,
        "scope": "DEV_METRIC_ARITHMETIC_ONLY",
        "scientific_confirmation": False,
        "training_provenance_attested": False,
    }
