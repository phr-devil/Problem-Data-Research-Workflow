"""Evidence-driven mechanism candidates: validate decisions, do not invent science."""
from __future__ import annotations
from core.contracts import ContractError

LEVERS = {"EXTRA_INFORMATION", "INDUCTIVE_BIAS", "OPTIMIZATION", "CAPACITY",
          "MEASUREMENT", "TASK_REFRAME"}

def validate_probe(value: dict) -> dict:
    if not isinstance(value, dict):
        raise ContractError("probe must be an object")
    required = ("probe_id", "task_id", "parent_run_id", "observed_error",
                "failed_premise", "competing_explanation", "mechanism",
                "distinct_prediction", "minimum_test", "if_positive", "if_negative",
                "if_invalid", "estimated_cost", "authorization_scope")
    for key in required:
        if not isinstance(value.get(key), str) or not value[key].strip():
            raise ContractError("missing nonempty probe field: " + key)
    if value.get("lever") not in LEVERS:
        raise ContractError("unknown scientific lever")
    refs = value.get("evidence_refs")
    if not isinstance(refs, list) or not refs or any(not isinstance(x,str) or not x.strip() for x in refs):
        raise ContractError("probe requires real error-evidence references")
    if value["distinct_prediction"].strip().casefold() == value["competing_explanation"].strip().casefold():
        raise ContractError("no distinguishable prediction")
    return value

def review_probe(value: dict, *, previous_failed_premises: list[str] | None = None,
                 authorization_granted: bool = False) -> dict:
    """Advisory only. Never runs a test or determines STOP/GO on scientific grounds."""
    probe = validate_probe(value)
    repeats = probe["failed_premise"] in (previous_failed_premises or [])
    return {"probe_id": probe["probe_id"], "task_id": probe["task_id"],
            "decision": "REVIEW_DIFFERENT_LEVER" if repeats else
                        ("AUTH_REQUIRED" if not authorization_granted else "PROBE_READY_FOR_EXECUTION"),
            "repeated_failed_premise": repeats,
            "note": "Structural candidate only; agent/human must verify evidence, cost and actual permission. No test was run."}
