"""Development-only comparison; cannot establish scientific novelty."""
from __future__ import annotations
from core.contracts import ContractError, validate_run

REQUIRED_SAME = ("task_id", "protocol_id", "dataset_version", "evaluator_version",
                 "split", "group_split", "sample_ids_hash", "level_id",
                 "k_unit", "support_query_policy")

def compare_runs(champion: dict, challenger: dict, metric: str,
                 *, lower_is_better: bool = False) -> dict:
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
    delta = b["metrics"][metric] - a["metrics"][metric]
    budget_review = a.get("budget_basis") != b.get("budget_basis")
    return {"comparison_status": "BUDGET_REVIEW_REQUIRED" if budget_review else "DEVELOPMENT_ONLY",
            "metric": metric, "champion_run_id": a["run_id"],
            "challenger_run_id": b["run_id"], "delta": delta,
            "improvement": -delta if lower_is_better else delta,
            "warning": "Structural comparison only; assess tuning fairness, independent groups, uncertainty and claim scope."}
