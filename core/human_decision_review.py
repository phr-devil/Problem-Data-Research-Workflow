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
DECISIONS = {"USER_CONFIRMED", "USER_DELEGATED", "PENDING"}
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
    if protocol_version not in (None, CONTRACT["protocol_version"]):
        raise ValueError("Unsupported human review protocol version")
    strict = protocol_version == CONTRACT["protocol_version"]
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
        if not isinstance(entry.get("original_user_message_ref"), str) or not entry["original_user_message_ref"].strip():
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
            missing_d = [
                dim for dim in spec["required_dimensions"]
                if not isinstance(dims.get(dim), str) or dims[dim].strip().upper() in UNDECIDED
            ]
            missing_e = [
                evidence for evidence in spec["evidence_minimum"]
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
            or any(step not in STEPS for step in invalidated)
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
            "and scientific evidence manually. This is not execution authorization, "
            "novelty certification or automatic approval. H9 requires independent "
            "confirmation authorization; H10 never bypasses the separate writing gate. "
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
