"""Read-only advisory checker for declared PD-RW H1-H10 human science choices.

No source-message authentication, permissions, resource operations, network access,
training, manuscript writing, or new workflow/CLI status is provided.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

# A machine-readable mirror of the scientific review definitions in WORKFLOW.md.
# Changing a definition must update the canonical policy and its regression tests.
CONTRACT_PATH = Path(__file__).resolve().parents[1] / "contracts" / "human_review_protocol.v1.json"
CONTRACT = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
STEPS = tuple(CONTRACT["steps"])
DEPENDENCIES = {
    step: tuple(spec["prerequisites"]) for step, spec in CONTRACT["steps"].items()
}
DECISIONS = {"USER_CONFIRMED", "USER_DELEGATED", "AGENT_DECIDED", "PENDING"}
AGENT_OWNED = {"H7"}
LEGACY_AGENT_OWNED = {"H6", "H7", "H8"}
AUTHOR_STRATEGY_NODES = {"H6", "H8"}
LEGACY_STRATEGY_DIMS = {
    "H6": (["task_hypothesis", "legal_inputs", "independent_evaluation"],
           ["valid_dev_or_theory_basis", "falsifier_and_comparator"]),
    "H8": (["main_claim", "positive_negative_evidence", "continue_narrow_pivot_hold"],
           ["valid_results", "strongest_alternative"]),
}

UNDECIDED = {"", "UNKNOWN", "UNDECIDED", "PENDING", "TBD", "N/A"}



def dependencies_of(node: str) -> set[str]:
    """Transitive prerequisites, excluding the target decision itself."""
    if node not in DEPENDENCIES:
        raise ValueError("Unrecognized H decision")
    result = set()
    for upstream in DEPENDENCIES[node]:
        result.add(upstream)
        result.update(dependencies_of(upstream))
    return result


def review(packet: dict) -> dict:
    """Check supplied decision metadata only; never certify actual user messages."""
    if not isinstance(packet, dict) or packet.get("format") != "pd-rw-human-review-v1":
        raise ValueError("Invalid advisory packet format")
    target = packet.get("target")
    if target not in STEPS:
        raise ValueError("target must be one of H1..H10")
    rows = packet.get("decisions")
    if not isinstance(rows, dict) or any(k not in STEPS for k in rows):
        raise ValueError("decisions must be an H-ID keyed object")

    protocol_version = packet.get("protocol_version")
    accepted = (None, CONTRACT["protocol_version"], *CONTRACT.get("legacy_protocol_versions", ()))
    if protocol_version not in accepted:
        raise ValueError("Unsupported human review protocol version")
    strict = protocol_version is not None
    present = set()
    malformed = []
    pending = set()
    missing_dimensions = {}
    missing_evidence = {}
    for name, entry in rows.items():
        if not isinstance(entry, dict) or entry.get("kind") not in DECISIONS:
            malformed.append(name)
            continue
        if entry["kind"] == "PENDING":
            pending.add(name)
            continue
        # Only H7 is agent-owned in the current protocol. Legacy H6/H8 agent
        # declarations remain readable, but never become new author approval.
        if entry["kind"] == "AGENT_DECIDED":
            # Existing projects can carry forward a real v1.2 H6/H8
            # decision without pretending it is a new author confirmation.
            # The source/ref are untrusted declarations: inspect original
            # records and verify strategy continuity outside this function.
            legacy_continuation = (
                protocol_version == CONTRACT["protocol_version"]
                and name in AUTHOR_STRATEGY_NODES
                and entry.get("legacy_source_protocol") == "pd-rw-human-review-v1.2"
                and isinstance(entry.get("legacy_unchanged_scope_ref"), str)
                and bool(entry["legacy_unchanged_scope_ref"].strip())
            )
            allowed_agent = (LEGACY_AGENT_OWNED if (
                protocol_version == "pd-rw-human-review-v1.2" or legacy_continuation
            ) else AGENT_OWNED)
            if (name not in allowed_agent
                    or not isinstance(entry.get("agent_decision_ref"), str)
                    or not entry["agent_decision_ref"].strip()
                    or not isinstance(entry.get("h5_scope_ref"), str)
                    or not entry["h5_scope_ref"].strip()):
                malformed.append(name)
                continue
        else:
            if (name in AGENT_OWNED and protocol_version == CONTRACT["protocol_version"]):
                malformed.append(name)
                continue
            if (not isinstance(entry.get("original_user_message_ref"), str)
                    or not entry["original_user_message_ref"].strip()):
                malformed.append(name)
                continue
            key = "chosen_option" if entry["kind"] == "USER_CONFIRMED" else "delegated_scope"
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                malformed.append(name)
                continue
        if strict:
            spec = CONTRACT["steps"][name]
            dims = entry.get("dimension_decisions")
            refs = entry.get("evidence_refs")
            dims = dims if isinstance(dims, dict) else {}
            refs = refs if isinstance(refs, dict) else {}
            dimensions = spec["required_dimensions"]
            minimum = spec["evidence_minimum"]
            is_legacy_step = (name in LEGACY_STRATEGY_DIMS
                              and entry["kind"] == "AGENT_DECIDED"
                              and (protocol_version == "pd-rw-human-review-v1.2"
                                   or entry.get("legacy_source_protocol")
                                   == "pd-rw-human-review-v1.2"))
            if is_legacy_step:
                dimensions, minimum = LEGACY_STRATEGY_DIMS[name]
            missing_d = [
                dim for dim in dimensions
                if not isinstance(dims.get(dim), str) or dims[dim].strip().upper() in UNDECIDED
            ]
            missing_e = [
                evidence for evidence in minimum
                if not isinstance(refs.get(evidence), str) or not refs[evidence].strip()
            ]
            if missing_d:
                missing_dimensions[name] = missing_d
            if missing_e:
                missing_evidence[name] = missing_e
            if missing_d or missing_e:
                continue
        present.add(name)

    # A previously declared choice may be obsolete after a change in upstream
    # truth, resource, task, or protocol. Only the supplied *declarations* are
    # checked here; an Agent must inspect real evidence to identify reopenings.
    invalidated = packet.get("invalidated_decisions", [])
    if (not isinstance(invalidated, list)
            or any(not isinstance(step, str) or step not in STEPS for step in invalidated)
            or len(set(invalidated)) != len(invalidated)):
        raise ValueError("invalidated_decisions must be distinct H1..H10 IDs")
    invalidated_set = set(invalidated)
    stale = {
        step for step in present
        if step in invalidated_set
        or bool(dependencies_of(step) & invalidated_set)
    }
    effective_present = present - stale
    required = dependencies_of(target)
    missing = sorted(required - effective_present, key=STEPS.index)
    blocked_by_reopened = sorted(
        invalidated_set & (required | {target}), key=STEPS.index
    )
    result = (
        "DECLARED_DEPENDENCIES_PRESENT_NOT_AUTHENTICATED"
        if not (missing or malformed or blocked_by_reopened)
        else "REVIEW_REQUIRED"
    )
    can_present = not (missing or blocked_by_reopened or malformed)
    can_advance = can_present and target in effective_present
    next_review = None
    if strict:
        next_review = next(
            (step for step in CONTRACT["new_project_sequence"] if step not in effective_present),
            "H6" if target in CONTRACT["new_project_sequence"] else target,
        )
        if target not in CONTRACT["new_project_sequence"] and not missing:
            next_review = target if not can_advance else None
        if can_advance and target in CONTRACT["new_project_sequence"][:-1]:
            next_review = CONTRACT["new_project_sequence"][
                CONTRACT["new_project_sequence"].index(target) + 1
            ]
    return {
        "target": target,
        "target_decision_owner": CONTRACT["steps"][target]["decision_owner"],
        "target_requires_user_scientific_choice": CONTRACT["steps"][target]["decision_owner"] == "USER",
        "target_decision_owner_under_source_protocol": (
            "AGENT_LEGACY" if protocol_version == "pd-rw-human-review-v1.2"
            and target in AUTHOR_STRATEGY_NODES else CONTRACT["steps"][target]["decision_owner"]),
        "author_strategy_review_node": target in AUTHOR_STRATEGY_NODES,
        "author_choice_pending": (target in AUTHOR_STRATEGY_NODES
                                  and protocol_version == CONTRACT["protocol_version"]
                                  and target not in effective_present),
        "target_legacy_continuation_not_new_author_approval": (
            target in AUTHOR_STRATEGY_NODES and target in effective_present
            and rows[target]["kind"] == "AGENT_DECIDED"),
        "legacy_agent_strategy_not_author_approved": sorted(
            (name for name in effective_present if name in AUTHOR_STRATEGY_NODES
             and rows[name]["kind"] == "AGENT_DECIDED"), key=STEPS.index),
        "agent_decision_declarations": sorted(
            (name for name in effective_present if rows[name]["kind"] == "AGENT_DECIDED"),
            key=STEPS.index,
        ),
        "protocol_version": protocol_version or "legacy_unverified",
        "can_present_review_declarations_only": can_present,
        "can_advance_declarations_only": can_advance,
        "next_review": next_review,
        "missing_required_dimensions": missing_dimensions,
        "missing_evidence_refs": missing_evidence,
        "result": result,
        "missing_prerequisites": missing,
        "malformed_declarations": sorted(malformed, key=STEPS.index),
        "pending_steps": sorted(pending, key=STEPS.index),
        "declared_completed": sorted(present, key=STEPS.index),
        "effective_declarations_after_reopening": sorted(effective_present, key=STEPS.index),
        "invalidated_decisions": sorted(invalidated_set, key=STEPS.index),
        "stale_declarations": sorted(stale, key=STEPS.index),
        "target_blocked_by_reopening": blocked_by_reopened,
        "requires_original_user_message_review": True,
        "allows_download_training_sealed_or_writing": False,
        "note": (
            "Declarations and message refs are untrusted; verify the original user messages "
            "and scientific evidence manually. In the current protocol H6/H8 "
            "require author strategy/claim choice or explicit scoped delegation; "
            "H7 and ordinary in-scope safe DEV work remain agent-owned. A complete "
            "Agent declaration is not authenticated user approval or tool permission. "
            "Old agent-owned H6/H8 records remain legacy, not new author signoff. "
            "H9 requires independent confirmation authorization; H10 never bypasses "
            "the separate writing gate. "
            "Reopened decisions are caller declarations, not evidence that the "
            "actual user changed their mind or that all dependent claims were found."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only declared human decision dependency check")
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    result = review(json.loads(args.packet.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
