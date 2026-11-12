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
    action = packet.get("action")
    if action not in ALL_ACTIONS:
        return {"decision": "BLOCK", "reason": "UNKNOWN_ACTION"}
    if packet.get("explicit_prohibition") is True:
        return {"decision": "BLOCK", "reason": "EXPLICIT_PROHIBITION"}
    if action in SAFE:
        return {"decision": "ALLOW", "reason": "NO_RESTRICTED_EFFECT_REQUESTED",
                "enforcement": "ADVISORY_NOT_TOOL_SANDBOX"}
    if action in DEV:
        conditions = ("h5_scope_confirmed", "dev_inputs_verified", "within_h5_scope",
                      "safe_local_nonpaid", "no_project_specific_prohibition")
        if any(packet.get(k) is False for k in conditions):
            return {"decision": "BLOCK", "reason": "DEV_PREREQUISITE_DENIED"}
        if any(packet.get(k) is not True for k in conditions):
            return {"decision": "UNKNOWN", "reason": "DEV_PREREQUISITE_NOT_AUTHENTICATED"}
        if not independently_authorized:
            return {"decision": "UNKNOWN", "reason": "HOST_MUST_VERIFY_ORIGINAL_SCOPE",
                    "enforcement": "ADVISORY_ONLY"}
        return {"decision": "ALLOW", "reason": "HOST_ATTESTED_DEV_SCOPE",
                "enforcement": "HOST_MUST_STILL_ENFORCE"}
    # A user grant for one effect never grants another effect.
    if packet.get("effect_forbidden") is True:
        return {"decision": "BLOCK", "reason": "EFFECT_FORBIDDEN"}
    if not independently_authorized:
        return {"decision": "UNKNOWN", "reason": "INDEPENDENT_EFFECT_AUTH_REQUIRED",
                "enforcement": "ADVISORY_ONLY"}
    return {"decision": "ALLOW", "reason": "HOST_ATTESTED_SPECIFIC_EFFECT",
            "enforcement": "HOST_MUST_STILL_ENFORCE"}


def science_checkpoint(packet: dict) -> dict:
    """Validate completeness only: original paper, Runs, and truth not checked."""
    trigger = packet.get("trigger")
    if trigger not in TRIGGERS:
        return {"result": "BLOCK_HANDOFF", "missing": ["valid_trigger"],
                "scientific_truth_verified": False}
    missing = []
    if trigger in NEEDS_CONTRIBUTION:
        if packet.get("primary_type") not in TYPES:
            missing.append("primary_type_C01_C12")
        if packet.get("route") not in ROUTES:
            missing.append("route_R1_R6")
        if not _present(packet.get("claim_or_question")):
            missing.append("claim_or_question")
        if not _present(packet.get("nearest_neighbor_or_unknown")):
            missing.append("nearest_neighbor_or_unknown")
    if trigger == "NEW_ALGORITHM":
        for k in ("observed_bottleneck_or_hypothesis", "simple_alternative",
                  "distinguishing_prediction"):
            if not _present(packet.get(k)):
                missing.append(k)
    if trigger in NEEDS_RESULTS:
        for k in ("actual_evidence_ref_or_not_run", "negative_evidence_or_none",
                  "strongest_alternative_or_unknown", "next_decisive_step"):
            if not _present(packet.get(k)):
                missing.append(k)
    if trigger == "CLAIM_PROMOTION":
        if not _present(packet.get("independent_validation_ref_or_unavailable")):
            missing.append("independent_validation_ref_or_unavailable")
        if packet.get("claim_status") not in {"HYPOTHESIZED", "EVIDENCE_CANDIDATE",
                                               "SUPPORTED", "CONFIRMED"}:
            missing.append("claim_status")
        if packet.get("claim_status") in {"SUPPORTED", "CONFIRMED"} and (
                not _present(packet.get("actual_evidence_ref_or_not_run")) or
                packet.get("actual_evidence_ref_or_not_run") == "NOT_RUN"):
            missing.append("real_evidence_for_supported_claim")
    return {"result": "READY_FOR_SCIENTIFIC_REVIEW" if not missing else "BLOCK_HANDOFF",
            "missing": missing, "scientific_truth_verified": False,
            "next": "review real source artifacts and scope; no permission implied"}


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
