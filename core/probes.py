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
    cost=value.get("cost_estimate")
    if cost is not None:
        if not isinstance(cost,dict) or not cost or any(
            k not in {"gpu_hours","cpu_hours","human_hours","tokens"} or
            isinstance(v,bool) or not isinstance(v,(int,float)) or v<0 or v!=v
            or v==float("inf") for k,v in cost.items()
        ):
            raise ContractError("cost_estimate requires finite nonnegative numerical budgets")
    return value

def review_probe(value: dict, *, previous_failed_premises: list[str] | None = None,
                 authorization_granted: bool = False,
                 remaining_budget: dict | None = None) -> dict:
    """Advisory only. Never runs a test or determines STOP/GO on scientific grounds."""
    probe = validate_probe(value)
    repeats = probe["failed_premise"] in (previous_failed_premises or [])
    estimate = probe.get("cost_estimate", {})
    beyond = []
    if remaining_budget is not None:
        if not isinstance(remaining_budget,dict):
            raise ContractError("remaining_budget must be a numeric dictionary")
        for kind, cost in estimate.items():
            available = remaining_budget.get(kind)
            if available is None or isinstance(available,bool) or not isinstance(available,(int,float)) or available<0 or available!=available:
                beyond.append(kind + ":BUDGET_UNKNOWN")
            elif cost>available:
                beyond.append(kind + ":EXCEEDS_REMAINING")
    return {"probe_id": probe["probe_id"], "task_id": probe["task_id"],
            "decision": "REVIEW_DIFFERENT_LEVER" if repeats else
                        ("BUDGET_REVIEW_REQUIRED" if beyond else
                         ("AUTH_REQUIRED" if not authorization_granted else "READY_FOR_MANUAL_SCOPE_CHECK")),
            "repeated_failed_premise": repeats, "budget_warnings": beyond,
            "note": "Structural candidate only; agent/human must verify evidence, cost and actual permission. No test was run."}
