"""Development-only structural comparison; never certifies scientific novelty.

A positive raw delta is not necessarily an improvement: loss/error metrics decrease.
Without an explicit metric direction, improvement remains UNKNOWN.
"""
from __future__ import annotations
from core.contracts import ContractError, validate_run

REQUIRED_SAME = ("task_id", "protocol_id", "dataset_version", "evaluator_version",
                 "split", "group_split", "sample_ids_hash", "level_id",
                 "k_unit", "support_query_policy")


def compare_runs(champion: dict, challenger: dict, metric: str,
                 *, lower_is_better: bool | None = None) -> dict:
    a, b = validate_run(champion), validate_run(challenger)
    if a["status"] != "VALID" or b["status"] != "VALID":
        raise ContractError("only VALID runs may be compared")
    if a["split"] == "sealed" or b["split"] == "sealed":
        raise ContractError("sealed data cannot be used for iterative comparison")
    mismatched = [field for field in REQUIRED_SAME if a.get(field) != b.get(field)]
    if sorted(a["legal_inputs"]) != sorted(b["legal_inputs"]):
        mismatched.append("legal_inputs")
    if mismatched:
        raise ContractError("NOT_COMPARABLE: mismatched " + ", ".join(mismatched))
    if metric not in a["metrics"] or metric not in b["metrics"]:
        raise ContractError("requested metric missing")
    if lower_is_better is not None and type(lower_is_better) is not bool:
        raise ContractError("lower_is_better must be boolean or None")

    a_direction, b_direction = a.get("metric_direction"), b.get("metric_direction")
    if a_direction is not None or b_direction is not None:
        if a_direction != b_direction:
            raise ContractError("NOT_COMPARABLE: metric_direction differs or is missing")
        direction = a_direction
        if lower_is_better is not None and lower_is_better != (direction == "min"):
            raise ContractError("metric direction flag conflicts with Run declarations")
        direction_source = "MATCHED_RUN_DECLARATIONS_NOT_INDEPENDENTLY_VERIFIED"
    elif lower_is_better is not None:
        direction = "min" if lower_is_better else "max"
        direction_source = "CALLER_FLAG_NOT_INDEPENDENTLY_VERIFIED"
    else:
        direction = None
        direction_source = "UNSPECIFIED"

    delta = b["metrics"][metric] - a["metrics"][metric]
    budget_review = (not a.get("budget_basis") or not b.get("budget_basis")
                     or a["budget_basis"] != b["budget_basis"])
    status = ("BUDGET_REVIEW_REQUIRED" if budget_review
              else "METRIC_DIRECTION_REVIEW_REQUIRED" if direction is None
              else "DEVELOPMENT_ONLY")
    return {
        "comparison_status": status,
        "metric": metric,
        "champion_run_id": a["run_id"],
        "challenger_run_id": b["run_id"],
        "delta": delta,
        "improvement": None if direction is None else (-delta if direction == "min" else delta),
        "metric_direction": direction or "UNKNOWN",
        "metric_direction_source": direction_source,
        "metric_direction_review_required": direction is None,
        "budget_review_required": budget_review,
        "warning": ("Structural DEV comparison only; positive delta is not automatically improvement. "
                    "Verify metric semantics, tuned budget fairness, independent groups, "
                    "uncertainty and claim scope."),
    }
