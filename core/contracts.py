"""Structural contracts only: passing validation does NOT certify scientific truth."""
from __future__ import annotations
import math
from typing import Any

class ContractError(ValueError):
    """A missing/invalid field or unsupported structural assertion."""

RUN_STATUSES = {"VALID", "INVALID", "INCONCLUSIVE", "NOT_RUN"}
CLAIM_STATUSES = {"HYPOTHESIZED", "EVIDENCE_CANDIDATE", "SUPPORTED", "CONFIRMED"}
SPLITS = {"dev", "validation", "sealed"}

def _object(value: Any) -> dict:
    if not isinstance(value, dict):
        raise ContractError("artifact must be a JSON object")
    return value

def _text(obj: dict, *keys: str) -> None:
    for key in keys:
        if not isinstance(obj.get(key), str) or not obj[key].strip():
            raise ContractError(f"missing nonempty text: {key}")

def _strings(obj: dict, key: str) -> None:
    values = obj.get(key)
    if not isinstance(values, list) or any(not isinstance(x, str) or not x.strip() for x in values):
        raise ContractError(f"{key} must be a list of nonempty strings")

def validate_run(value: Any) -> dict:
    obj = _object(value)
    _text(obj, "run_id", "task_id", "protocol_id", "dataset_version",
          "evaluator_version", "group_split", "sample_ids_hash")
    if obj.get("status") not in RUN_STATUSES or obj.get("split") not in SPLITS:
        raise ContractError("invalid run status/split")
    _strings(obj, "legal_inputs")
    for opt in ("level_id", "k_unit", "support_query_policy", "budget_basis"):
        if opt in obj:
            _text(obj, opt)
    if "metric_direction" in obj and obj["metric_direction"] not in {"max", "min"}:
        raise ContractError("metric_direction must be max or min when declared")
    metrics = obj.get("metrics", {})
    if not isinstance(metrics, dict):
        raise ContractError("metrics must be an object")
    if obj["status"] == "VALID":
        if not metrics or any(
            not isinstance(k, str) or not k or isinstance(v, bool)
            or not isinstance(v, (int, float)) or not math.isfinite(v)
            for k, v in metrics.items()
        ):
            raise ContractError("VALID run needs finite numeric metrics")
        refs = obj.get("artifact_refs")
        if not isinstance(refs, dict):
            raise ContractError("VALID run requires artifact_refs object")
        _text(refs, "metrics", "predictions", "code")
    if obj["split"] == "sealed":
        _text(obj, "frozen_protocol_ref", "authorization_ref")
    return obj

def validate_claim(value: Any) -> dict:
    obj = _object(value)
    _text(obj, "claim_id", "task_id", "claim_text")
    if obj.get("status") not in CLAIM_STATUSES:
        raise ContractError("invalid claim status")
    for key in ("evidence_run_ids", "artifact_refs", "confirmation_run_ids"):
        if key in obj:
            _strings(obj, key)
    if obj["status"] in {"SUPPORTED", "CONFIRMED"}:
        if not obj.get("evidence_run_ids") or not obj.get("artifact_refs"):
            raise ContractError("supported claims require Run and artifact references")
        _text(obj, "strongest_alternative")
    if obj["status"] == "CONFIRMED":
        if not obj.get("confirmation_run_ids"):
            raise ContractError("CONFIRMED requires confirmation Run IDs")
        _text(obj, "confirmation_protocol_ref")
    return obj

def validate_state(value: Any) -> dict:
    obj = _object(value)
    _text(obj, "schema_version", "project_id")
    if obj.get("last_event_id") is not None and not isinstance(obj["last_event_id"], str):
        raise ContractError("invalid last_event_id")
    if not isinstance(obj.get("evidence_refs"), list):
        raise ContractError("evidence_refs must be a list")
    return obj
