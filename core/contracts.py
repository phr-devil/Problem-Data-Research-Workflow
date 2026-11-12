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
    if obj.get("evidence_path", "EMPIRICAL") != "EMPIRICAL":
        raise ContractError("Run records are empirical; use NON_DATA Claim for proof/simulation")
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
        _text(obj, "claim_scope")
        if obj["status"] in {"SUPPORTED", "CONFIRMED"}:
            _text(obj, "assumptions_ref")
            if not obj.get("evidence_refs") or not obj.get("artifact_refs"):
                raise ContractError("supported NON_DATA claims require local evidence and artifact references")
            _text(obj, "strongest_alternative")
        if obj["status"] == "CONFIRMED":
            if not obj.get("independent_validation_refs"):
                raise ContractError("confirmed NON_DATA claims require independent validation references")
            # A review of the very same file does not create independent evidence.
            original = set(obj["evidence_refs"] + obj["artifact_refs"] + [obj["assumptions_ref"]])
            if original.intersection(obj["independent_validation_refs"]):
                raise ContractError("independent validation must reference a separate artifact")
            _text(obj, "confirmation_protocol_ref", "confirmation_scope",
                  "independence_limit")
            if obj["evidence_type"] == "SIMULATION" and obj["confirmation_scope"] != "SIMULATION_DOMAIN_ONLY":
                raise ContractError("simulation confirmation cannot assert empirical generalization")
            if obj["evidence_type"] == "THEORETICAL_PROOF" and obj["confirmation_scope"] != "THEOREM_SCOPE_ONLY":
                raise ContractError("proof confirmation is bounded by theorem assumptions")
            if obj["evidence_type"] == "AUDITED_MECHANISM" and obj["confirmation_scope"] != "MECHANISM_SCOPE_ONLY":
                raise ContractError("mechanism audit cannot assert empirical generalization")
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

    # Activity entry, human choice and operational authorization are orthogonal.
    # Every reference below is untrusted caller metadata, not an authenticated grant.
    entry_refs = packet.get("entry_evidence_refs", {})
    if not isinstance(entry_refs, dict):
        raise ContractError("entry_evidence_refs must be an object")
    entry_checks = spec.get("entry_checks", {})
    entry_keys = list(entry_checks.get("all", []))
    entry_keys += entry_checks.get(evidence_path, [])
    execution_kind = packet.get("execution_kind", "UNSPECIFIED")
    if activity_id == "04":
        if execution_kind not in {
            "UNSPECIFIED", "CONTROLLED_EXPERIMENT", "NO_CONTROLLED_EXPERIMENT"
        }:
            raise ContractError("invalid execution_kind")
        if execution_kind == "CONTROLLED_EXPERIMENT":
            # v1 legacy original permission remains valid; new work may cite
            # H5-backed standing local DEV autonomy. Neither string is a
            # verified credential, so an execution adapter must recheck scope.
            required = entry_checks.get("when_controlled_experiment", [])
            alternatives = entry_checks.get("legacy_alternative_when_controlled_experiment", [])
            if not any(isinstance(entry_refs.get(k), str) and entry_refs[k].strip()
                       for k in [*required, *alternatives]):
                entry_keys += required
    if activity_id == "06":
        entry_keys += entry_checks.get(
            "when_unavailable" if has_ref("CONFIRMATION_UNAVAILABLE")
            else "when_confirming", []
        )
    missing_entry = [
        key for key in entry_keys
        if not isinstance(entry_refs.get(key), str) or not entry_refs[key].strip()
    ]
    entry_declarations_complete = not missing_entry
    applicability_map = packet.get("human_review_applicability", {})
    if not isinstance(applicability_map, dict):
        raise ContractError("human_review_applicability must be an object")

    def review_not_applicable(name: str) -> bool:
        entry = applicability_map.get(name)
        return (
            isinstance(entry, dict)
            and entry.get("status") == "NOT_APPLICABLE"
            and isinstance(entry.get("reason"), str) and bool(entry["reason"].strip())
            and isinstance(entry.get("evidence_ref"), str) and bool(entry["evidence_ref"].strip())
        )

    if activity_id == "04" and skip_declared:
        if not isinstance(packet.get("not_applicable_evidence_ref"), str) or not packet["not_applicable_evidence_ref"].strip():
            raise ContractError("non-method activity 04 needs an independent rationale evidence ref")
        if execution_kind != "NO_CONTROLLED_EXPERIMENT":
            raise ContractError("non-method activity 04 requires NO_CONTROLLED_EXPERIMENT declaration")
    required_review = {
        "01": ["H5"], "02": ["H5"], "03": ["H6"],
        "04": ["H6"] if review_not_applicable("H7") else ["H7"],
        "05": ["H8"],
        "06": ["H10"] if (has_ref("CONFIRMATION_UNAVAILABLE")
                         and review_not_applicable("H9")) else ["H9", "H10"],
    }[activity_id]
    if any(name not in {"H7", "H9"} for name in applicability_map):
        raise ContractError("only H7 and H9 are conditional review nodes")
    if "H7" in applicability_map and not review_not_applicable("H7"):
        raise ContractError("invalid H7 NOT_APPLICABLE declaration")
    if "H9" in applicability_map and not review_not_applicable("H9"):
        raise ContractError("invalid H9 NOT_APPLICABLE declaration")
    if activity_id != "04" and "H7" in applicability_map:
        raise ContractError("H7 applicability belongs to activity 04")
    if activity_id != "06" and "H9" in applicability_map:
        raise ContractError("H9 applicability belongs to activity 06")
    if activity_id == "06" and has_ref("INDEPENDENT_CONFIRM") and review_not_applicable("H9"):
        raise ContractError("H9 cannot be skipped when independent confirmation is claimed")

    human_packet = packet.get("human_review_packet")
    human_status = "NOT_CHECKED"
    human_missing = required_review
    if human_packet is not None:
        if not isinstance(human_packet, dict):
            raise ContractError("human_review_packet must be an object")
        from core.human_decision_review import CONTRACT as HUMAN_CONTRACT, review as review_human
        if human_packet.get("protocol_version") not in (
                HUMAN_CONTRACT["protocol_version"],
                *HUMAN_CONTRACT.get("legacy_protocol_versions", ())):
            human_status = "LEGACY_OR_UNSUPPORTED_NOT_VERIFIED"
        else:
            human_missing = []
            legacy_agent_strategy = False
            for name in required_review:
                candidate = dict(human_packet)
                candidate["target"] = name
                try:
                    decision = review_human(candidate)
                except ValueError as exc:
                    raise ContractError(f"invalid human_review_packet: {exc}") from exc
                if not decision["can_advance_declarations_only"]:
                    human_missing.append(name)
                # A legacy agent-supplied H6/H8 record cannot represent a new
                # author choice; permit unchanged historical research only when
                # a separately recorded scope continuity ref is declared.
                if name in {"H6", "H8"} and decision.get(
                        "legacy_agent_strategy_not_author_approved"):
                    legacy_agent_strategy = True
            if legacy_agent_strategy and not (
                    isinstance(packet.get("legacy_unchanged_scope_ref"), str)
                    and packet["legacy_unchanged_scope_ref"].strip()):
                human_missing.extend(
                    name for name in required_review if name in {"H6", "H8"}
                    and name not in human_missing)
            human_status = ("DECLARED_COMPLETE_NOT_AUTHENTICATED"
                            if not human_missing else
                            "LEGACY_SCOPE_CONTINUITY_REQUIRED" if legacy_agent_strategy
                            else "DECLARED_INCOMPLETE")
    # A complete H6/H8 author *declaration* is not necessarily accompanied
    # by the required ranked scientific choices. Join the two independent
    # preflights at the actual 03/05 handoff, and verify their declared choices
    # describe the same user message and option. Neither check authenticates it.
    strategy_review_status = "NOT_APPLICABLE"
    strategy_review_missing = []
    strategy_review_ready = True
    if activity_id in {"03", "05"} and isinstance(human_packet, dict) and (
            human_packet.get("protocol_version") == "pd-rw-human-review-v1.3"):
        strategy_review_ready = False
        strategy = packet.get("strategy_checkpoint_packet")
        expected = "H6_TASK" if activity_id == "03" else "H8_CLAIM"
        decision_id = "H6" if activity_id == "03" else "H8"
        if not isinstance(strategy, dict):
            strategy_review_status = "MISSING_STRATEGY_CHECKPOINT"
            strategy_review_missing = ["strategy_checkpoint_packet"]
        elif strategy.get("trigger") != expected:
            strategy_review_status = "STRATEGY_TRIGGER_MISMATCH"
            strategy_review_missing = [f"expected_{expected}"]
        else:
            from core.execution_preflight import science_checkpoint
            strategy_result = science_checkpoint(strategy)
            strategy_review_missing = list(strategy_result["missing"])
            if strategy_result["result"] != "READY_FOR_SCIENTIFIC_REVIEW":
                strategy_review_status = strategy_result["result"]
            else:
                row = human_packet.get("decisions", {}).get(decision_id, {})
                selection = strategy.get("author_review", {}).get("selection", {})
                if not isinstance(row, dict) or not isinstance(selection, dict):
                    strategy_review_missing.append("matching_author_decision")
                else:
                    match = (
                        row.get("kind") == selection.get("kind")
                        and row.get("original_user_message_ref")
                        == selection.get("original_user_message_ref")
                    )
                    if row.get("kind") == "USER_CONFIRMED":
                        match = match and row.get("chosen_option") == selection.get("chosen_option_id")
                        choices = strategy["author_review"]["options"]
                        chosen = next((o for o in choices if isinstance(o, dict)
                                       and o.get("id") == row.get("chosen_option")), None)
                        match = (match and chosen is not None
                                 and chosen.get("primary_type") == strategy.get("primary_type")
                                 and chosen.get("route") == strategy.get("route"))
                    elif row.get("kind") == "USER_DELEGATED":
                        match = match and row.get("delegated_scope") == selection.get("delegated_scope")
                    if not match:
                        strategy_review_missing.append("author_strategy_selection_mismatch")
                strategy_review_ready = not strategy_review_missing
                strategy_review_status = (
                    "DECLARED_MATCH_NOT_AUTHENTICATED" if strategy_review_ready
                    else "STRATEGY_DECISION_MISMATCH"
                )
    elif activity_id in {"03", "05"} and not isinstance(human_packet, dict):
        strategy_review_ready = False
        strategy_review_status = "HUMAN_DECISION_PACKET_MISSING"

    human_declared_complete = human_status == "DECLARED_COMPLETE_NOT_AUTHENTICATED"
    declared_complete = not (
        missing or unresolved_critical or malformed or missing_outputs
        or missing_alternatives or missing_path_deliverables
        or contradictory_confirmation or skip_declared
    )
    unavailable = activity_id == "06" and has_ref("CONFIRMATION_UNAVAILABLE")
    # Legacy handoff completeness remains evidence/deliverables only; the new
    # stage disposition cannot silently promote it to entry or permission PASS.
    non_method_scope_ready = (
        skip_declared and review_not_applicable("H7")
        and entry_declarations_complete and human_declared_complete
        and strategy_review_ready
    )
    full_scope_ready = (
        declared_complete and entry_declarations_complete
        and human_declared_complete and strategy_review_ready and not skip_declared
        and (activity_id != "04" or execution_kind != "UNSPECIFIED")
    )
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
        "required_human_review_declarations": required_review,
        "human_review_declarations_status": human_status,
        "human_review_declarations_missing": human_missing,
        "strategy_review_status": strategy_review_status,
        "strategy_review_missing": strategy_review_missing,
        "strategy_review_ready_declarations_only": strategy_review_ready,
        "missing_entry_evidence_declarations": missing_entry,
        "entry_declarations_complete_not_authenticated": entry_declarations_complete,
        "declared_activity_ready_not_authenticated": full_scope_ready,
        "declared_non_method_scope_ready_not_authenticated": non_method_scope_ready,
        "non_method_disposition": ("JUSTIFIED_NOT_APPLICABLE_DECLARED"
                                  if skip_declared else "ACTIVE"),
        "execution_kind": execution_kind if activity_id == "04" else None,
        "parallel_science_activities": spec["allowed_parallel_activities"],
        "declared_handoff_complete_not_verified": declared_complete,
        "justified_non_method_skip_declared": skip_declared,
        "confirmation_unavailable_declared": unavailable,
        "real_evidence_and_user_message_authentication_required": True,
        "scientific_truth_verified": False,
        "authorizes_download_fitting_sealed_figures_or_writing": False,
        "note": "Structural review of untrusted declarations only. Entry refs and H "
                "packet are not authenticated; declared readiness NEVER authorizes "
                "downloads, fitting, SEALED, figures or writing. UNKNOWN/NOT_RUN "
                "must not become positive science; an unavailable confirmation "
                "does not confirm a Claim.",
    }
