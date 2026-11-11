"""Structural contracts only: passing validation does NOT certify scientific truth."""
from __future__ import annotations
import math
from typing import Any

class ContractError(ValueError):
    """A missing/invalid field or unsupported structural assertion."""

RUN_STATUSES = {"VALID", "INVALID", "INCONCLUSIVE", "NOT_RUN"}
CLAIM_STATUSES = {"HYPOTHESIZED", "EVIDENCE_CANDIDATE", "SUPPORTED", "CONFIRMED"}
SPLITS = {"dev", "validation", "sealed"}

def _object(value: Any) -> dict:
    if not isinstance(value, dict):
        raise ContractError("artifact must be a JSON object")
    return value

def _text(obj: dict, *keys: str) -> None:
    for key in keys:
        if not isinstance(obj.get(key), str) or not obj[key].strip():
            raise ContractError(f"missing nonempty text: {key}")

def _strings(obj: dict, key: str) -> None:
    values = obj.get(key)
    if not isinstance(values, list) or any(not isinstance(x, str) or not x.strip() for x in values):
        raise ContractError(f"{key} must be a list of nonempty strings")

def validate_run(value: Any) -> dict:
    obj = _object(value)
    _text(obj, "run_id", "task_id", "protocol_id", "dataset_version",
          "evaluator_version", "group_split", "sample_ids_hash")
    if obj.get("status") not in RUN_STATUSES or obj.get("split") not in SPLITS:
        raise ContractError("invalid run status/split")
    _strings(obj, "legal_inputs")
    for opt in ("level_id", "k_unit", "support_query_policy", "budget_basis"):
        if opt in obj:
            _text(obj, opt)
    if "metric_direction" in obj and obj["metric_direction"] not in {"max", "min"}:
        raise ContractError("metric_direction must be max or min when declared")
    metrics = obj.get("metrics", {})
    if not isinstance(metrics, dict):
        raise ContractError("metrics must be an object")
    if obj["status"] == "VALID":
        if not metrics or any(
            not isinstance(k, str) or not k or isinstance(v, bool)
            or not isinstance(v, (int, float)) or not math.isfinite(v)
            for k, v in metrics.items()
        ):
            raise ContractError("VALID run needs finite numeric metrics")
        refs = obj.get("artifact_refs")
        if not isinstance(refs, dict):
            raise ContractError("VALID run requires artifact_refs object")
        _text(refs, "metrics", "predictions", "code")
    if obj["split"] == "sealed":
        _text(obj, "frozen_protocol_ref", "authorization_ref")
    return obj

def validate_claim(value: Any) -> dict:
    """Validate a scoped Claim. Missing evidence_path is legacy EMPIRICAL.

    NON_DATA is restricted to auditable theoretical/simulation claims; it is
    NOT an alternative for empirical performance or population generalization.
    Source authenticity and scientific correctness remain external checks.
    """
    obj = _object(value)
    _text(obj, "claim_id", "task_id", "claim_text")
    if obj.get("status") not in CLAIM_STATUSES:
        raise ContractError("invalid claim status")
    evidence_path = obj.get("evidence_path", "EMPIRICAL")
    if evidence_path not in {"EMPIRICAL", "NON_DATA"}:
        raise ContractError("claim evidence_path must be EMPIRICAL or NON_DATA")
    for key in ("evidence_run_ids", "artifact_refs", "confirmation_run_ids",
                "evidence_refs", "independent_validation_refs"):
        if key in obj:
            _strings(obj, key)
    if evidence_path == "NON_DATA":
        if obj.get("evidence_run_ids") or obj.get("confirmation_run_ids"):
            raise ContractError("NON_DATA claims may not disguise empirical Runs; split mixed claims")
        if obj.get("evidence_type") not in {"THEORETICAL_PROOF", "SIMULATION", "AUDITED_MECHANISM"}:
            raise ContractError("NON_DATA requires explicit bounded evidence_type")
        _text(obj, "claim_scope", "assumptions_ref")
        if obj["status"] in {"SUPPORTED", "CONFIRMED"}:
            if not obj.get("evidence_refs") or not obj.get("artifact_refs"):
                raise ContractError("supported NON_DATA claims require local evidence and artifact references")
            _text(obj, "strongest_alternative")
        if obj["status"] == "CONFIRMED":
            if not obj.get("independent_validation_refs"):
                raise ContractError("confirmed NON_DATA claims require independent validation references")
            _text(obj, "confirmation_protocol_ref", "confirmation_scope",
                  "independence_limit")
            if obj["evidence_type"] == "SIMULATION" and obj["confirmation_scope"] != "SIMULATION_DOMAIN_ONLY":
                raise ContractError("simulation confirmation cannot assert empirical generalization")
            if obj["evidence_type"] == "THEORETICAL_PROOF" and obj["confirmation_scope"] != "THEOREM_SCOPE_ONLY":
                raise ContractError("proof confirmation is bounded by theorem assumptions")
    else:
        if obj["status"] in {"SUPPORTED", "CONFIRMED"}:
            if not obj.get("evidence_run_ids") or not obj.get("artifact_refs"):
                raise ContractError("supported empirical claims require Run and artifact references")
            _text(obj, "strongest_alternative")
        if obj["status"] == "CONFIRMED":
            if not obj.get("confirmation_run_ids"):
                raise ContractError("CONFIRMED empirical claims require confirmation Run IDs")
            _text(obj, "confirmation_protocol_ref")
    return obj

def validate_state(value: Any) -> dict:
    obj = _object(value)
    _text(obj, "schema_version", "project_id")
    if obj.get("last_event_id") is not None and not isinstance(obj["last_event_id"], str):
        raise ContractError("invalid last_event_id")
    if not isinstance(obj.get("evidence_refs"), list):
        raise ContractError("evidence_refs must be a list")
    return obj


# Existing six activities: declared evidence-handoff check, not a permission gate.
# Scientific scope belongs to WORKFLOW.md; the JSON is a tested structural mirror.
def review_activity_handoff(packet: dict) -> dict:
    """Review caller-supplied handoff metadata without opening source artifacts."""
    import json
    from pathlib import Path

    if not isinstance(packet, dict) or packet.get("format") != "pd-rw-activity-handoff-v1":
        raise ContractError("invalid activity handoff format")
    path = Path(__file__).resolve().parents[1] / "contracts" / "research_activity_protocol.v1.json"
    contract = json.loads(path.read_text(encoding="utf-8"))
    if packet.get("contract_version") != contract["contract_version"]:
        raise ContractError("unsupported activity contract version")
    activity_id = packet.get("activity_id")
    if activity_id not in contract["activities"]:
        raise ContractError("unknown activity")
    spec = contract["activities"][activity_id]
    evidence_path = packet.get("evidence_path")
    if evidence_path not in spec["alternative_evidence_paths"]:
        raise ContractError("unsupported evidence path")
    evidence = packet.get("evidence", {})
    deliverables = packet.get("deliverable_refs", {})
    if not isinstance(evidence, dict) or not isinstance(deliverables, dict):
        raise ContractError("evidence and deliverable_refs must be objects")
    if any(not isinstance(k, str) for k in evidence):
        raise ContractError("evidence keys must be strings")
    statuses = {"VERIFIED", "REPORTED", "EXPLORATORY", "UNKNOWN",
                "NOT_RUN", "INVALID", "STALE", "NOT_APPLICABLE"}
    positive = {"VERIFIED", "REPORTED", "EXPLORATORY"}
    missing = []
    unresolved_critical = []
    reported_gaps = []
    malformed = []
    for item in spec["mandatory_evidence"]:
        key = item["key"]
        statement = evidence.get(key)
        if statement is None:
            missing.append(key)
            continue
        if not isinstance(statement, dict) or statement.get("status") not in statuses:
            malformed.append(key)
            continue
        status = statement["status"]
        ref = statement.get("ref")
        if status in positive and (not isinstance(ref, str) or not ref.strip()):
            malformed.append(key)
            continue
        if status not in positive:
            reported_gaps.append(key)
            if item["critical"]:
                unresolved_critical.append(key)
        elif item["critical"] and status == "EXPLORATORY":
            # Exploratory evidence is usable as a hypothesis, not decisive
            # evidence for a formal downstream scientific assertion.
            unresolved_critical.append(key)

    def has_ref(key: str) -> bool:
        return isinstance(deliverables.get(key), str) and bool(deliverables[key].strip())

    missing_outputs = [key for key in spec["required_deliverables"] if not has_ref(key)]
    missing_alternatives = [
        group for group in spec["one_of_deliverables"]
        if not any(has_ref(key) for key in group)
    ]
    missing_path_deliverables = [
        key for key in spec.get("path_required_deliverables", {}).get(evidence_path, [])
        if not has_ref(key)
    ]
    contradictory_confirmation = (
        activity_id == "06"
        and has_ref("INDEPENDENT_CONFIRM")
        and has_ref("CONFIRMATION_UNAVAILABLE")
    )
    applicability = packet.get("applicability", "ACTIVE")
    if applicability not in {"ACTIVE", "NOT_APPLICABLE"}:
        raise ContractError("invalid applicability declaration")
    skip_reason = packet.get("not_applicable_reason")
    if applicability == "NOT_APPLICABLE":
        if activity_id != "04" or not isinstance(skip_reason, str) or not skip_reason.strip():
            raise ContractError("only non-method activity 04 may declare justified NOT_APPLICABLE")
    skip_declared = applicability == "NOT_APPLICABLE"
    declared_complete = not (
        missing or unresolved_critical or malformed or missing_outputs
        or missing_alternatives or missing_path_deliverables
        or contradictory_confirmation or skip_declared
    )
    unavailable = activity_id == "06" and has_ref("CONFIRMATION_UNAVAILABLE")
    return {
        "activity_id": activity_id,
        "contract_version": contract["contract_version"],
        "evidence_path": evidence_path,
        "missing_evidence_declarations": missing,
        "malformed_evidence_declarations": malformed,
        "unresolved_critical_evidence": unresolved_critical,
        "documented_gaps": reported_gaps,
        "missing_deliverables": missing_outputs,
        "missing_alternative_deliverable_groups": missing_alternatives,
        "missing_evidence_path_deliverables": missing_path_deliverables,
        "contradictory_confirmation_outputs": contradictory_confirmation,
        "human_review_nodes": spec["human_review"],
        "parallel_science_activities": spec["allowed_parallel_activities"],
        "declared_handoff_complete_not_verified": declared_complete,
        "justified_non_method_skip_declared": skip_declared,
        "confirmation_unavailable_declared": unavailable,
        "real_evidence_and_user_message_authentication_required": True,
        "scientific_truth_verified": False,
        "authorizes_download_fitting_sealed_figures_or_writing": False,
        "note": "Structural review of untrusted declarations only. Check original artifacts, "
                "actual human choices and separate operation permissions. UNKNOWN/NOT_RUN "
                "must not be upgraded to positive evidence. A recorded unavailable "
                "confirmation does not certify the Claim.",
    }
