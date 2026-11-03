"""Optional information-condition diagnostic for research pivots (NO FIT/IO).

An Oracle advantage is not evidence that a deployable policy can identify the
best action before decision time. This reviewer validates submitted premises
only; it never declares a task successful, learns from data, grants permission
or changes the live Task/protocol automatically.
"""
from __future__ import annotations
import math
from core.contracts import ContractError

def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{field} must be nonempty text")
    return value.strip()

def _setting(obj: object, name: str) -> dict:
    if not isinstance(obj, dict):
        raise ContractError(f"{name} must be a setting object")
    for key in ("task_id", "protocol_id", "k_unit"):
        _text(obj.get(key), f"{name}.{key}")
    k = obj.get("target_label_k")
    if type(k) is not int or k < 0:
        raise ContractError(f"{name}.target_label_k must be nonnegative integer")
    info = obj.get("legal_predecision_information")
    if not isinstance(info, list) or any(not isinstance(v, str) or not v.strip() for v in info):
        raise ContractError(f"{name}.legal_predecision_information must be a string list")
    if len(set(info)) != len(info):
        raise ContractError(f"{name} duplicates legal information")
    return obj

def review_information_shift(value: dict) -> dict:
    """Advisory classification, NOT a new compulsory scientific approval gate.

    Optional inputs refer to evidence already obtained; NEVER opens or fits a dataset.
    """
    if not isinstance(value, dict):
        raise ContractError("information transition must be a JSON object")
    root = _text(value.get("root_problem"), "root_problem")
    old = _setting(value.get("before"), "before")
    new = _setting(value.get("after"), "after")
    if old["task_id"] == new["task_id"] and old["protocol_id"] == new["protocol_id"]:
        raise ContractError("changed information condition requires a versioned Task/protocol")
    change = value.get("new_information", {})
    if not isinstance(change, dict):
        raise ContractError("new_information must be an object")
    access = change.get("available_before_prediction")
    disjoint = change.get("support_query_disjoint")
    affordable = change.get("cost_feasible")
    for field, flag in (("available_before_prediction", access),
                        ("support_query_disjoint", disjoint), ("cost_feasible", affordable)):
        if flag is not None and type(flag) is not bool:
            raise ContractError(field + " must be true, false or null")
    evidence = value.get("evidence", {})
    if not isinstance(evidence, dict):
        raise ContractError("evidence must be a JSON object")
    for field in ("oracle_gain", "learned_vs_simple"):
        num = evidence.get(field)
        if num is not None and (type(num) not in (float,int) or not math.isfinite(num)):
            raise ContractError(field + " must be finite numeric or unknown")
    interval = evidence.get("oracle_gain_range")
    if interval is not None and (not isinstance(interval, list) or len(interval)!=2 or
        any(type(x) not in (int,float) or not math.isfinite(x) for x in interval) or interval[0]>interval[1]):
        raise ContractError("oracle_gain_range must be finite [lower,upper]")
    stable = evidence.get("learned_policy_stable_advantage")
    if stable is not None and type(stable) is not bool:
        raise ContractError("learned_policy_stable_advantage must be boolean or unknown")
    refs = evidence.get("refs", [])
    if not isinstance(refs, list) or any(not isinstance(p,str) or not p.strip() for p in refs):
        raise ContractError("evidence.refs must be nonempty strings when supplied")
    shared = value.get("unresolved_shared_blockers", [])
    if not isinstance(shared, list) or any(not isinstance(p,str) or not p.strip() for p in shared):
        raise ContractError("unresolved_shared_blockers must be strings")
    changed_k = old["target_label_k"] != new["target_label_k"] or old["k_unit"] != new["k_unit"]
    new_inputs = sorted(set(new["legal_predecision_information"]) - set(old["legal_predecision_information"]))
    changed_info = bool(changed_k or new_inputs)
    oracle = evidence.get("oracle_gain")
    learned = evidence.get("learned_vs_simple")
    oracle_policy_gap = ((oracle is not None and learned is not None and oracle > 0 and learned <= 0)
                          or (interval is not None and interval[0] > 0 and stable is False))
    warnings = []
    if oracle_policy_gap:
        warnings.append("ORACLE_GAIN_DOES_NOT_ESTABLISH_PREDECISION_IDENTIFIABILITY")
    if not refs:
        warnings.append("NO_PRIMARY_EVIDENCE_REFERENCES")
    if change.get("same_information_simple_baseline") is not True:
        warnings.append("SAME_INFORMATION_SAME_K_SIMPLE_BASELINE_REQUIRED")
    if change.get("cost_feasible") is None:
        warnings.append("DEPLOYMENT_COST_UNKNOWN")
    if shared:
        warnings.append("COMMON_FAILURE_PREMISE_NOT_RESOLVED")
    if not changed_info:
        decision = "NO_NEW_INFORMATION_LEVER"
    elif access is False or disjoint is False or affordable is False:
        decision = "INADMISSIBLE_OR_UNAFFORDABLE_INFORMATION"
    elif shared:
        decision = "UNRESOLVED_SHARED_PREMISE"
    elif access is None or disjoint is None:
        decision = "ACCESS_OR_SUPPORT_QUERY_UNKNOWN"
    else:
        decision = "INFORMATION_SETTING_PIVOT_CANDIDATE"
    return {
        "status": "ADVISORY_NOT_EXECUTED",
        "root_problem": root,
        "decision": decision,
        "new_information_lever": {"k_changed":changed_k, "new_legal_inputs":new_inputs},
        "oracle_policy_gap": oracle_policy_gap,
        "warnings": warnings,
        "requires_new_task_protocol_and_claim": changed_info,
        "science_success": "NOT_EVALUATED",
        "previous_task_success": "NOT_INFERRED",
        "required_next_probe": "Check independent DEV label/group evidence, same-K simple baseline, conditional transfer and negative slices; preserve selection history",
        "authorization": "NOT_GRANTED_BY_THIS_REVIEW",
    }
