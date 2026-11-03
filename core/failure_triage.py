"""Advisory failure triage: report scope, not a research or authorization verdict.

Inputs are user/Agent-declared evidence pointers. This module neither opens
datasets nor decides whether a scientific claim is true.
"""
from __future__ import annotations
from core.contracts import ContractError

KINDS = {
    "EVALUATION_INVALID", "TRAINING_INADEQUATE", "LEGAL_INFORMATION_GAP",
    "SIMPLE_BASELINE_DOMINATES", "CLAIM_NOT_DISTINCT", "STATISTICAL_UNCERTAINTY",
    "MECHANISM_NEGATIVE", "EXPLORATORY_OBSERVATION",
}
PRIORITY = (
    ("EVALUATION_INVALID", "REPAIR_AFFECTED_EVIDENCE", "RUN"),
    ("TRAINING_INADEQUATE", "CHECK_TRAINING_AND_FAIR_BUDGET", "RUN"),
    ("LEGAL_INFORMATION_GAP", "REVIEW_INFORMATION_PIVOT", "TASK"),
    ("SIMPLE_BASELINE_DOMINATES", "KEEP_BASELINE_REVIEW_NEW_LEVER", "MECHANISM"),
    ("CLAIM_NOT_DISTINCT", "REVIEW_CLAIM_OR_NEAREST_WORK", "CLAIM"),
    ("STATISTICAL_UNCERTAINTY", "INCONCLUSIVE_MINIMUM_PROBE", "CLAIM"),
    ("MECHANISM_NEGATIVE", "DISCARD_MECHANISM_REVIEW_ALTERNATIVE", "MECHANISM"),
    ("EXPLORATORY_OBSERVATION", "LOW_COST_DISCRIMINATING_PROBE", "RUN"),
)

def review_failure(value: dict) -> dict:
    if not isinstance(value, dict):
        raise ContractError("triage input must be a JSON object")
    for key in ("task_id", "protocol_id"):
        if not isinstance(value.get(key), str) or not value[key].strip():
            raise ContractError("triage requires " + key)
    findings = value.get("findings")
    if not isinstance(findings, list) or not findings:
        raise ContractError("triage requires at least one finding")
    seen = []
    for item in findings:
        if not isinstance(item, dict) or item.get("kind") not in KINDS:
            raise ContractError("invalid triage finding kind")
        if item.get("evidence_level") not in {"OBSERVED", "HYPOTHESIZED"}:
            raise ContractError("evidence_level must be OBSERVED/HYPOTHESIZED")
        if not isinstance(item.get("evidence_ref"), str) or not item["evidence_ref"].strip():
            raise ContractError("each finding needs a source evidence_ref")
        seen.append(item)
    # Observed claims are still unverified until the referenced original Run is checked.
    observed = {i["kind"] for i in seen if i["evidence_level"] == "OBSERVED"}
    matched = next(((kind, action, scope) for kind, action, scope in PRIORITY if kind in observed), None)
    if matched is None:
        action, scope = "INSPECT_PRIMARY_EVIDENCE", "RUN"
        chosen = None
    else:
        chosen, action, scope = matched
    next_probe = value.get("next_probe")
    if next_probe is not None and (not isinstance(next_probe, str) or not next_probe.strip()):
        raise ContractError("next_probe must be nonempty text or omitted")
    return {
        "status": "ADVISORY_NOT_EXECUTED",
        "task_id": value["task_id"], "protocol_id": value["protocol_id"],
        "primary_finding": chosen, "suggested_route": action,
        "decision_scope": scope, "next_probe": next_probe or "Find the cheapest evidence that distinguishes the remaining explanations",
        "all_evidence_refs": sorted({i["evidence_ref"] for i in seen}),
        "hypotheses_not_established": sorted({i["kind"] for i in seen if i["evidence_level"] == "HYPOTHESIZED"}),
        "cautions": [
            "OBSERVED is self-declared: inspect original Run, evaluator, and group-level evidence",
            "No automatic project STOP, new Task authorization, or scientific confirmation",
            "Different K / prediction-time information requires a new Task, protocol and Claim",
        ],
        "execution": "NOT_RUN", "authorization": "NOT_GRANTED",
    }
