"""Optional PD-RW routing for an externally verified DEV feasibility profile.

A self-declared JSON cannot establish signal or scientific novelty. When the
report comes from Forge, inspect the original SHA-backed Runs before treating
its source status as verified. No training, downloading, writes or STOP gates.
"""
from __future__ import annotations

import math
from core.contracts import ContractError

SIGNALS = {
    "UNKNOWN_WITHOUT_MATCHED_REFERENCE",
    "DEV_IMPROVEMENT_OVER_REFERENCE_OBSERVED",
    "NO_DEV_IMPROVEMENT_OVER_REFERENCE_OBSERVED",
    "DEV_TIE_WITH_REFERENCE",
}


def review_feasibility(value: dict) -> dict:
    if not isinstance(value, dict):
        raise ContractError("Feasibility profile must be a JSON object")
    for field in ("task_id", "protocol_id", "candidate"):
        if not isinstance(value.get(field), str) or not value[field].strip():
            raise ContractError(f"missing feasibility {field}")
    signal = value.get("signal_evidence")
    if signal not in SIGNALS:
        raise ContractError("unknown signal evidence status")
    groups = value.get("n_independent_groups")
    if type(groups) is not int or groups < 0:
        raise ContractError("n_independent_groups must be nonnegative integer")
    evidence_ref = value.get("evidence_ref")
    if not isinstance(evidence_ref, str) or not evidence_ref.strip():
        raise ContractError("evidence_ref must point to the source report/Run")
    remainder = value.get("remaining_error")
    if not isinstance(remainder, dict) or remainder.get("theoretical_attainable_gain") != "UNKNOWN":
        raise ContractError("Residual magnitude must not be mistaken for attainable gain")
    paired = value.get("paired_evidence")
    if signal == "UNKNOWN_WITHOUT_MATCHED_REFERENCE":
        if paired is not None:
            raise ContractError("unmatched reference cannot contain paired gain")
        route = "GET_FAIR_SIMPLE_REFERENCE_IF_AUTHORIZED"
    else:
        if not isinstance(paired, dict) or paired.get("scientific_claim_confirmed") is not False:
            raise ContractError("DEV comparison must not claim independent scientific confirmation")
        delta = paired.get("directional_delta")
        if type(delta) not in (int,float) or not math.isfinite(delta):
            raise ContractError("paired delta must be finite")
        expected = (
            "DEV_IMPROVEMENT_OVER_REFERENCE_OBSERVED" if delta > 0 else
            "NO_DEV_IMPROVEMENT_OVER_REFERENCE_OBSERVED" if delta < 0 else
            "DEV_TIE_WITH_REFERENCE"
        )
        if signal != expected:
            raise ContractError("declared signal contradicts paired delta")
        route = ("VERIFY_RESIDUAL_MECHANISM_AND_UNSEEN_GROUPS"
                 if delta > 0 else
                 "REVIEW_NEW_LEGAL_INFORMATION_OR_DISTINCT_FAILURE_PREMISE")
    kind = value.get("evaluation_type")
    if kind == "forge-dev-event-v1":
        route = "USE_TASK_SPECIFIC_EVENT_DIAGNOSTIC"
    return {
        "status": "ADVISORY_INPUT_NOT_REVERIFIED",
        "suggested_route": route,
        "decision_scope": "DEVELOPMENT_PROBE_ONLY",
        "data_evidence": value.get("data_validity", "UNVERIFIED"),
        "n_independent_groups": groups,
        "group_uncertainty": "LIMITED_GROUP_EVIDENCE" if groups < 4 else "GROUP_DIAGNOSTIC_STILL_EXPLORATORY",
        "signal": signal,
        "source": evidence_ref,
        "next_probe": (
            "Inspect original verified Runs, same-information strong baseline, "
            "independent-group residual mechanism and legal label budget; "
            "choose the cheapest discriminating experiment"
        ),
        "scientific_success": "NOT_DETERMINED",
        "automatic_project_stop": False,
        "fitting_performed": False,
        "authorization_granted": False,
        "notes": [
            "Input report is self-declared until original Run receipts are independently checked",
            "DEV error and Oracle advantage do not establish achievable performance headroom",
            "A reference Run is not necessarily a strong or fairly tuned simple baseline",
            "Retain valid negative results and model/Task-level distinction",
        ],
    }
