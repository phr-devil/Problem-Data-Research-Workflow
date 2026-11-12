"""Deterministic PD-RW action and scientific-checkpoint preflight.

Advisory when called from an Agent/CLI: no JSON field, source pointer or self-
asserted approval authenticates user permission. Real blocking requires the
host executor to call this gate and independently enforce filesystem/tool ACLs.
Never imports data, trains, opens SEALED files, or executes actions.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SAFE = {"READ_PUBLIC", "ANALYZE_EXISTING_METADATA", "REVIEW_RULES"}
DEV = {"DEV_CODE", "DEV_TRAIN", "DEV_EVALUATE", "DEV_FIX"}
PROTECTED = {
    "DOWNLOAD", "READ_SEALED", "RUN_CONFIRMATION", "DRAW_IMAGE",
    "WRITE_MANUSCRIPT", "SUBMIT", "PAY", "EXTERNAL_UPLOAD",
    "UNSAFE_INSTALL", "PROJECT_SCOPE_CHANGE", "PROJECT_STOP",
}
ALL_ACTIONS = SAFE | DEV | PROTECTED
ROUTES = {"R1", "R2", "R3", "R4", "R5", "R6"}
TYPES = {f"C{i:02d}" for i in range(1, 13)}
TRIGGERS = {"H6_TASK", "NEW_ALGORITHM", "SIGNIFICANT_RUN", "NEGATIVE_RESULT",
            "H8_CLAIM", "CLAIM_PROMOTION"}
NEEDS_CONTRIBUTION = {"H6_TASK", "H8_CLAIM", "CLAIM_PROMOTION"}
NEEDS_RESULTS = {"SIGNIFICANT_RUN", "NEGATIVE_RESULT", "H8_CLAIM", "CLAIM_PROMOTION"}


def action_preflight(packet: dict, *, independently_authorized: bool = False) -> dict:
    """independently_authorized is a host-only kwarg, not a packet field.

    A host must independently authenticate the original grant and its scope;
    this function cannot do it. The CLI never passes True.
    """
    if not isinstance(packet, dict):
        return {"decision": "BLOCK", "reason": "MALFORMED_ACTION_PACKET"}
    action = packet.get("action")
    if not isinstance(action, str) or action not in ALL_ACTIONS:
        return {"decision": "BLOCK", "reason": "UNKNOWN_ACTION"}
    if packet.get("explicit_prohibition") is True:
        return {"decision": "BLOCK", "reason": "EXPLICIT_PROHIBITION"}
    if packet.get("effect_forbidden") is True:
        return {"decision": "BLOCK", "reason": "EFFECT_FORBIDDEN"}
    if action in SAFE:
        return {"decision": "ALLOW", "reason": "NO_RESTRICTED_EFFECT_REQUESTED",
                "enforcement": "ADVISORY_NOT_TOOL_SANDBOX"}
    if action in DEV:
        conditions = ("h5_scope_confirmed", "dev_inputs_verified", "within_h5_scope",
                      "safe_local_nonpaid", "no_project_specific_prohibition",
                      "within_author_selected_strategy")
        if (packet.get("h6_strategy_pending") is True
                and packet.get("legacy_unchanged_scope_confirmed") is not True):
            return {"decision": "BLOCK", "reason": "H6_AUTHOR_STRATEGY_PENDING"}
        if any(packet.get(k) is False for k in conditions):
            return {"decision": "BLOCK", "reason": "DEV_PREREQUISITE_OR_STRATEGY_DENIED"}
        if any(packet.get(k) is not True for k in conditions):
            return {"decision": "UNKNOWN", "reason": "DEV_PREREQUISITE_NOT_AUTHENTICATED"}
        # Existing unchanged legacy research does not need a retroactive H6
        # signoff. These are only caller declarations; the host must verify.
        current = packet.get("h6_author_strategy_confirmed")
        legacy = packet.get("legacy_unchanged_scope_confirmed")
        if current is not True and legacy is not True:
            if current is False and legacy is False:
                return {"decision": "BLOCK", "reason": "NO_VALID_H6_OR_LEGACY_SCOPE"}
            return {"decision": "UNKNOWN", "reason": "H6_AUTHOR_STRATEGY_NOT_VERIFIED"}
        if not independently_authorized:
            return {"decision": "UNKNOWN", "reason": "HOST_MUST_VERIFY_ORIGINAL_SCOPE",
                    "enforcement": "ADVISORY_ONLY"}
        return {"decision": "ALLOW", "reason": "HOST_ATTESTED_DEV_SCOPE",
                "enforcement": "HOST_MUST_STILL_ENFORCE"}
    # A user grant for one effect never grants another effect.
    if not independently_authorized:
        return {"decision": "UNKNOWN", "reason": "INDEPENDENT_EFFECT_AUTH_REQUIRED",
                "enforcement": "ADVISORY_ONLY"}
    return {"decision": "ALLOW", "reason": "HOST_ATTESTED_SPECIFIC_EFFECT",
            "enforcement": "HOST_MUST_STILL_ENFORCE"}


AUTHOR_NODES = {"H6_TASK", "H8_CLAIM"}
P_ORIENTATIONS = {"P1", "P2", "P3", "P4", "P5"}


def author_strategy_review(packet: dict) -> dict:
    """Check proposal/decision *declarations*, never authenticate user messages."""
    if not isinstance(packet, dict):
        return {"result": "BLOCK_HANDOFF", "missing": ["author_review_packet_object"]}
    trigger = packet.get("trigger")
    if not isinstance(trigger, str) or trigger not in AUTHOR_NODES:
        return {"result": "BLOCK_HANDOFF", "missing": ["author_review_trigger"]}
    review = packet.get("author_review", {})
    review = review if isinstance(review, dict) else {}
    missing = []
    options = review.get("options")
    if not isinstance(options, list) or not (1 <= len(options) <= 3):
        options = []
        missing.append("one_to_three_ranked_options")
    ids = []
    for i, option in enumerate(options):
        if not isinstance(option, dict):
            missing.append(f"options[{i}]_object")
            continue
        for key in ("id", "claim_or_task", "primary_type", "route", "p_orientation",
                    "independent_knowledge", "prior_gap", "decisive_evidence",
                    "science_value", "cost_and_speed", "failure_premise"):
            if not _present(option.get(key)):
                missing.append(f"options[{i}].{key}")
        if not isinstance(option.get("primary_type"), str) or option["primary_type"] not in TYPES:
            missing.append(f"options[{i}].valid_C_type")
        if not isinstance(option.get("route"), str) or option["route"] not in ROUTES:
            missing.append(f"options[{i}].valid_R_route")
        if not isinstance(option.get("p_orientation"), str) or option["p_orientation"] not in P_ORIENTATIONS:
            missing.append(f"options[{i}].valid_P_orientation")
        if trigger == "H8_CLAIM" and (not isinstance(option.get("h8_action"), str) or option.get("h8_action") not in {
                "KEEP", "UPGRADE", "NARROW", "REFRAME", "HOLD"}):
            missing.append(f"options[{i}].valid_h8_action")
        ids.append(option.get("id") if _present(option.get("id")) else None)
    if len(ids) != len(set(ids)):
        missing.append("unique_option_ids")
    if len(options) > 1:
        distinct = {
            (o.get("claim_or_task"), o.get("failure_premise"))
            for o in options if isinstance(o, dict)
            and isinstance(o.get("claim_or_task"), str)
            and isinstance(o.get("failure_premise"), str)
        }
        if len(distinct) < 2:
            missing.append("genuinely_distinct_alternatives")
    if len(options) == 1 and not _present(review.get("single_option_reason")):
        missing.append("single_option_reason")
    recommended = review.get("recommended_option_id")
    if recommended not in ids or not _present(review.get("recommendation_rationale")):
        missing.append("grounded_recommendation")
    if not _present(review.get("key_unknown")):
        missing.append("key_unknown")
    if trigger == "H8_CLAIM":
        for key in ("positive_negative_evidence_ref", "strongest_objection",
                    "publication_potential_or_unknown", "confirmation_gap"):
            if not _present(review.get(key)):
                missing.append(key)
    if missing:
        return {"result": "BLOCK_HANDOFF", "missing": missing,
                "author_approval_authenticated": False}
    selection = review.get("selection", {})
    if not isinstance(selection, dict) or not isinstance(selection.get("kind"), str) or selection.get("kind") not in {
            "USER_CONFIRMED", "USER_DELEGATED"}:
        return {"result": "AUTHOR_CHOICE_REQUIRED", "missing": ["author_choice_or_delegation"],
                "recommended_option_id": recommended, "author_approval_authenticated": False}
    if not _present(selection.get("original_user_message_ref")):
        missing.append("original_user_message_ref")
    if selection.get("kind") == "USER_CONFIRMED":
        if selection.get("chosen_option_id") not in ids:
            missing.append("chosen_option_id")
    else:
        if not _present(selection.get("delegated_scope")):
            missing.append("delegated_scope")
    if missing:
        return {"result": "BLOCK_HANDOFF", "missing": missing,
                "author_approval_authenticated": False}
    return {"result": "DECLARED_AUTHOR_CHOICE_PRESENT_NOT_AUTHENTICATED",
            "missing": [], "recommended_option_id": recommended,
            "author_approval_authenticated": False, "tool_permission_granted": False}


def science_checkpoint(packet: dict) -> dict:
    """Validate completion fields only; real author messages and science need audit."""
    if not isinstance(packet, dict):
        return {"result": "BLOCK_HANDOFF", "missing": ["science_packet_object"],
                "scientific_truth_verified": False, "author_approval_authenticated": False}
    trigger = packet.get("trigger")
    if not isinstance(trigger, str) or trigger not in TRIGGERS:
        return {"result": "BLOCK_HANDOFF", "missing": ["valid_trigger"],
                "scientific_truth_verified": False}
    missing = []
    if trigger in NEEDS_CONTRIBUTION:
        if not isinstance(packet.get("primary_type"), str) or packet["primary_type"] not in TYPES:
            missing.append("primary_type_C01_C12")
        if not isinstance(packet.get("route"), str) or packet["route"] not in ROUTES:
            missing.append("route_R1_R6")
        if not _present(packet.get("claim_or_question")):
            missing.append("claim_or_question")
        if not _present(packet.get("nearest_neighbor_or_unknown")):
            missing.append("nearest_neighbor_or_unknown")
    if trigger == "NEW_ALGORITHM":
        for key in ("observed_bottleneck_or_hypothesis", "simple_alternative",
                    "distinguishing_prediction"):
            if not _present(packet.get(key)):
                missing.append(key)
    if trigger in NEEDS_RESULTS:
        for key in ("actual_evidence_ref_or_not_run", "negative_evidence_or_none",
                    "strongest_alternative_or_unknown", "next_decisive_step"):
            if not _present(packet.get(key)):
                missing.append(key)
    if trigger == "CLAIM_PROMOTION":
        if not _present(packet.get("independent_validation_ref_or_unavailable")):
            missing.append("independent_validation_ref_or_unavailable")
        if not isinstance(packet.get("claim_status"), str) or packet.get("claim_status") not in {"HYPOTHESIZED", "EVIDENCE_CANDIDATE",
                                             "SUPPORTED", "CONFIRMED"}:
            missing.append("claim_status")
        if packet.get("claim_status") in {"SUPPORTED", "CONFIRMED"}:
            if (not _present(packet.get("actual_evidence_ref_or_not_run")) or
                    packet.get("actual_evidence_ref_or_not_run") == "NOT_RUN"):
                missing.append("real_evidence_for_supported_claim")
            # Only a *frozen primary* research strategy requires H8 author
            # choice. Valid secondary DEV findings may be supported without
            # repeatedly requesting an author decision. Missing role retains
            # the stricter legacy primary-claim interpretation.
            role = packet.get("claim_role", "PRIMARY_FROZEN")
            if not isinstance(role, str) or role not in {"PRIMARY_FROZEN", "SECONDARY_DEV"}:
                missing.append("valid_claim_role")
            if (role == "PRIMARY_FROZEN" and
                    not (_present(packet.get("h8_author_choice_ref"))
                         or _present(packet.get("legacy_unchanged_claim_ref")))):
                missing.append("author_selected_main_claim_or_unchanged_legacy")
        independent_ref = packet.get("independent_validation_ref_or_unavailable")
        if (packet.get("claim_status") == "CONFIRMED"
                and isinstance(independent_ref, str)
                and independent_ref.strip().upper() in {
                    "UNAVAILABLE", "UNKNOWN", "NOT_RUN", "NONE"}):
            missing.append("confirmed_needs_real_independent_evidence")
    author = author_strategy_review(packet) if trigger in AUTHOR_NODES else None
    if author and author["result"] == "BLOCK_HANDOFF":
        missing.extend("author_review." + v for v in author["missing"])
    if missing:
        result = "BLOCK_HANDOFF"
    elif author and author["result"] == "AUTHOR_CHOICE_REQUIRED":
        result = "AUTHOR_CHOICE_REQUIRED"
    else:
        result = "READY_FOR_SCIENTIFIC_REVIEW"
    return {"result": result, "missing": missing, "scientific_truth_verified": False,
            "author_approval_authenticated": False,
            "author_review_result": author["result"] if author else "NOT_APPLICABLE",
            "next": "Check original author message and science; no tool permission implied"}

def _present(x):
    return isinstance(x, str) and bool(x.strip())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["action", "science"])
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    packet = json.loads(args.packet.read_text(encoding="utf-8"))
    result = action_preflight(packet) if args.mode == "action" else science_checkpoint(packet)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("decision") == "ALLOW" or result.get("result") == "READY_FOR_SCIENTIFIC_REVIEW" else 2


if __name__ == "__main__":
    raise SystemExit(main())
