"""Offline H6/H8 author-choice contract regression; no user messages authenticated."""
import copy
import unittest

from core.human_decision_review import CONTRACT, review
from core.contracts import review_activity_handoff
import json
from pathlib import Path


def declared_step(name, *, kind=None, protocol=None):
    spec = CONTRACT["steps"][name]
    if kind is None:
        kind = "AGENT_DECIDED" if name == "H7" else "USER_CONFIRMED"
    step = {"kind": kind}
    if kind == "AGENT_DECIDED":
        step.update(agent_decision_ref="agent/technical/H7", h5_scope_ref="H5/message")
    else:
        step.update(original_user_message_ref="original/user/message",
                    chosen_option="A", delegated_scope="AI within H5 scoped R4")
    step["dimension_decisions"] = {x: "EXPLICIT_SCOPE" for x in spec["required_dimensions"]}
    step["evidence_refs"] = {x: "source/artifact" for x in spec["evidence_minimum"]}
    if protocol == "pd-rw-human-review-v1.2":
        legacy = {
            "H6": (["task_hypothesis", "legal_inputs", "independent_evaluation"],
                   ["valid_dev_or_theory_basis", "falsifier_and_comparator"]),
            "H8": (["main_claim", "positive_negative_evidence", "continue_narrow_pivot_hold"],
                   ["valid_results", "strongest_alternative"])
        }
        if name in legacy:
            dims, refs = legacy[name]
            step["dimension_decisions"] = {x: "EXPLICIT_SCOPE" for x in dims}
            step["evidence_refs"] = {x: "source/artifact" for x in refs}
    return step


def packet(target, *, protocol=None):
    protocol = protocol or CONTRACT["protocol_version"]
    decisions = {}
    for h in ("H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8"):
        decisions[h] = declared_step(h, protocol=protocol)
    return {"format": "pd-rw-human-review-v1",
            "protocol_version": protocol, "target": target,
            "decisions": decisions, "invalidated_decisions": []}


class AuthorH6H8ContractTests(unittest.TestCase):
    def test_current_protocol_requires_h6_h8_author(self):
        self.assertEqual(CONTRACT["steps"]["H6"]["decision_owner"], "USER")
        self.assertEqual(CONTRACT["steps"]["H8"]["decision_owner"], "USER")
        self.assertEqual(CONTRACT["steps"]["H7"]["decision_owner"], "AGENT")
        for h in ("H6", "H8"):
            p = packet(h)
            r = review(p)
            self.assertTrue(r["can_advance_declarations_only"])
            self.assertTrue(r["target_requires_user_scientific_choice"])
            self.assertFalse(r["allows_download_training_sealed_or_writing"])

    def test_agent_cannot_fake_h6_h8_decision(self):
        for h in ("H6", "H8"):
            p = packet(h)
            p["decisions"][h] = declared_step(h, kind="AGENT_DECIDED")
            r = review(p)
            self.assertFalse(r["can_advance_declarations_only"])
            self.assertIn(h, r["malformed_declarations"])
            self.assertTrue(r["author_choice_pending"])

    def test_author_delegation_is_recognized_without_becoming_access_grant(self):
        p = packet("H8")
        p["decisions"]["H8"] = declared_step("H8", kind="USER_DELEGATED")
        r = review(p)
        self.assertTrue(r["can_advance_declarations_only"])
        self.assertTrue(r["requires_original_user_message_review"])
        self.assertFalse(r["allows_download_training_sealed_or_writing"])

    def test_required_author_recommendation_evidence_cannot_be_empty(self):
        p = packet("H6")
        del p["decisions"]["H6"]["evidence_refs"]["ranked_options_and_ai_recommendation"]
        r = review(p)
        self.assertFalse(r["can_advance_declarations_only"])
        self.assertIn("ranked_options_and_ai_recommendation", r["missing_evidence_refs"]["H6"])

    def test_malformed_reopen_list_is_rejected_cleanly(self):
        p = packet("H8")
        p["invalidated_decisions"] = [{"malformed": True}]
        with self.assertRaises(ValueError):
            review(p)

    def test_legacy_ownership_is_not_current_author_approval(self):
        p = packet("H6", protocol="pd-rw-human-review-v1.2")
        p["decisions"]["H6"] = declared_step(
            "H6", kind="AGENT_DECIDED", protocol="pd-rw-human-review-v1.2")
        r = review(p)
        self.assertEqual(r["target_decision_owner_under_source_protocol"], "AGENT_LEGACY")
        self.assertIn("H6", r["legacy_agent_strategy_not_author_approved"])

    def test_technical_h7_remains_agent_owned(self):
        p = packet("H7")
        r = review(p)
        self.assertTrue(r["can_advance_declarations_only"])
        self.assertFalse(r["target_requires_user_scientific_choice"])

    def test_h6_reopening_invalidates_h8_not_h5(self):
        p = packet("H8")
        p["invalidated_decisions"] = ["H6"]
        r = review(p)
        self.assertFalse(r["can_advance_declarations_only"])
        self.assertIn("H8", r["stale_declarations"])
        self.assertNotIn("H5", r["stale_declarations"])

    def test_current_h8_can_follow_unchanged_legacy_h6(self):
        p = packet("H8")
        old_h6 = declared_step("H6", kind="AGENT_DECIDED",
                                protocol="pd-rw-human-review-v1.2")
        old_h6.update(legacy_source_protocol="pd-rw-human-review-v1.2",
                      legacy_unchanged_scope_ref="legacy/scope/validated")
        p["decisions"]["H6"] = old_h6
        r = review(p)
        self.assertTrue(r["can_advance_declarations_only"])
        self.assertIn("H6", r["legacy_agent_strategy_not_author_approved"])
        self.assertFalse(r["target_legacy_continuation_not_new_author_approval"])

    def test_mixed_legacy_requires_exact_source_and_scope(self):
        p = packet("H8")
        old_h6 = declared_step("H6", kind="AGENT_DECIDED",
                                protocol="pd-rw-human-review-v1.2")
        old_h6["legacy_source_protocol"] = "pd-rw-human-review-v1.2"
        p["decisions"]["H6"] = old_h6
        self.assertFalse(review(p)["can_advance_declarations_only"])
        old_h6["legacy_unchanged_scope_ref"] = "legacy/provenance"
        self.assertTrue(review(p)["can_advance_declarations_only"])

    def test_legacy_agent_strategy_readable_but_never_author_approved(self):
        p = packet("H6", protocol="pd-rw-human-review-v1.2")
        p["decisions"]["H6"] = declared_step(
            "H6", kind="AGENT_DECIDED", protocol="pd-rw-human-review-v1.2")
        p["decisions"]["H8"] = declared_step(
            "H8", kind="AGENT_DECIDED", protocol="pd-rw-human-review-v1.2")
        r = review(p)
        self.assertTrue(r["can_advance_declarations_only"])
        self.assertIn("H6", r["legacy_agent_strategy_not_author_approved"])
        self.assertTrue(r["requires_original_user_message_review"])


def strategy_packet(activity, *, kind="USER_CONFIRMED"):
    trigger = "H6_TASK" if activity == "03" else "H8_CLAIM"
    option = {
        "id": "A", "claim_or_task": "Boundary under contact changes",
        "primary_type": "C11", "route": "R4", "p_orientation": "P3",
        "independent_knowledge": "Measured failure boundary",
        "prior_gap": "Prior unknown", "decisive_evidence": "DEV grouped falsifier",
        "science_value": "Risk recognition", "cost_and_speed": "existing DEV",
        "failure_premise": "label axis invalid"
    }
    if trigger == "H8_CLAIM":
        option["h8_action"] = "KEEP"
    review = {
        "options": [option], "single_option_reason": "Only feasible evidence source",
        "recommended_option_id": "A", "recommendation_rationale": "Closest valid prior",
        "key_unknown": "UNKNOWN",
        "selection": {"kind": kind, "original_user_message_ref": "original/user/message",
                      "chosen_option_id": "A", "delegated_scope": "AI within H5 scoped R4",
                      "allowed_option_ids": ["A"]}
    }
    p = {"trigger": trigger, "primary_type": "C11", "route": "R4",
         "claim_or_question": "Contact boundary", "nearest_neighbor_or_unknown": "UNKNOWN",
         "author_review": review}
    if trigger == "H8_CLAIM":
        review.update(positive_negative_evidence_ref="runs/dev1",
                      strongest_objection="Confounding",
                      publication_potential_or_unknown="UNKNOWN",
                      confirmation_gap="SEALED not yet authorized")
        p.update(actual_evidence_ref_or_not_run="runs/dev1",
                 negative_evidence_or_none="No method gain",
                 strongest_alternative_or_unknown="Confounding",
                 next_decisive_step="Grouped comparison")
    return p


def activity_packet(activity, human):
    path = Path(__file__).resolve().parents[1] / "contracts" / "research_activity_protocol.v1.json"
    contract = json.loads(path.read_text(encoding="utf-8"))
    spec = contract["activities"][activity]
    return {
        "format": "pd-rw-activity-handoff-v1",
        "contract_version": contract["contract_version"],
        "activity_id": activity, "evidence_path": "EMPIRICAL",
        "evidence": {item["key"]: {"status": "VERIFIED", "ref": "dev/evidence"}
                     for item in spec["mandatory_evidence"]},
        "deliverable_refs": {key: "project/artifact" for key in spec["required_deliverables"]},
        "entry_evidence_refs": {key: "project/evidence" for key in spec["entry_checks"]["all"]},
        "human_review_packet": human,
    }


class AuthorActivityHandoffTests(unittest.TestCase):
    def test_current_author_h6_03_is_declared_complete(self):
        p = activity_packet("03", packet("H6"))
        p["strategy_checkpoint_packet"] = strategy_packet("03")
        r = review_activity_handoff(p)
        self.assertTrue(r["declared_activity_ready_not_authenticated"])
        self.assertFalse(r["authorizes_download_fitting_sealed_figures_or_writing"])

    def test_strategy_packet_required_for_current_h6(self):
        p = activity_packet("03", packet("H6"))
        self.assertFalse(review_activity_handoff(p)["declared_activity_ready_not_authenticated"])
        self.assertEqual(review_activity_handoff(p)["strategy_review_status"],
                         "MISSING_STRATEGY_CHECKPOINT")
        p["strategy_checkpoint_packet"] = strategy_packet("03")
        self.assertTrue(review_activity_handoff(p)["declared_activity_ready_not_authenticated"])

    def test_strategy_packet_required_for_current_h8(self):
        p = activity_packet("05", packet("H8"))
        self.assertFalse(review_activity_handoff(p)["declared_activity_ready_not_authenticated"])
        p["strategy_checkpoint_packet"] = strategy_packet("05")
        r = review_activity_handoff(p)
        self.assertTrue(r["declared_activity_ready_not_authenticated"])
        self.assertFalse(r["scientific_truth_verified"])

    def test_mismatched_author_selection_is_blocked(self):
        p = activity_packet("03", packet("H6"))
        s = strategy_packet("03")
        s["author_review"]["selection"]["original_user_message_ref"] = "other/original"
        p["strategy_checkpoint_packet"] = s
        r = review_activity_handoff(p)
        self.assertFalse(r["declared_activity_ready_not_authenticated"])
        self.assertEqual(r["strategy_review_status"], "STRATEGY_DECISION_MISMATCH")

    def test_author_delegation_scope_must_match(self):
        human = packet("H8")
        human["decisions"]["H8"] = declared_step("H8", kind="USER_DELEGATED")
        p = activity_packet("05", human)
        p["strategy_checkpoint_packet"] = strategy_packet("05", kind="USER_DELEGATED")
        self.assertTrue(review_activity_handoff(p)["declared_activity_ready_not_authenticated"])
        p["strategy_checkpoint_packet"]["author_review"]["selection"]["delegated_scope"] = "different"
        self.assertFalse(review_activity_handoff(p)["declared_activity_ready_not_authenticated"])

    def test_new_h8_handoff_with_unchanged_legacy_h6(self):
        human = packet("H8")
        old_h6 = declared_step("H6", kind="AGENT_DECIDED",
                                protocol="pd-rw-human-review-v1.2")
        old_h6.update(legacy_source_protocol="pd-rw-human-review-v1.2",
                      legacy_unchanged_scope_ref="legacy/scope/validated")
        human["decisions"]["H6"] = old_h6
        p = activity_packet("05", human)
        p["strategy_checkpoint_packet"] = strategy_packet("05")
        self.assertFalse(review_activity_handoff(p)["declared_activity_ready_not_authenticated"])
        p["legacy_unchanged_scope_ref"] = "legacy/scope/validated"
        r = review_activity_handoff(p)
        self.assertTrue(r["declared_activity_ready_not_authenticated"])
        self.assertEqual(r["strategy_review_status"], "DECLARED_MATCH_NOT_AUTHENTICATED")

    def test_old_h6_does_not_need_a_new_recommendation_packet(self):
        human = packet("H6")
        old_h6 = declared_step("H6", kind="AGENT_DECIDED",
                                protocol="pd-rw-human-review-v1.2")
        old_h6.update(legacy_source_protocol="pd-rw-human-review-v1.2",
                      legacy_unchanged_scope_ref="legacy/scope/validated")
        human["decisions"]["H6"] = old_h6
        p = activity_packet("03", human)
        p["legacy_unchanged_scope_ref"] = "legacy/scope/validated"
        r = review_activity_handoff(p)
        self.assertTrue(r["declared_activity_ready_not_authenticated"])
        self.assertEqual(r["strategy_review_status"],
                         "LEGACY_CONTINUITY_DECLARED_NOT_NEW_APPROVAL")

    def test_legacy_agent_h6_requires_scope_continuity(self):
        legacy = packet("H6", protocol="pd-rw-human-review-v1.2")
        legacy["decisions"]["H6"] = declared_step(
            "H6", kind="AGENT_DECIDED", protocol="pd-rw-human-review-v1.2")
        p = activity_packet("03", legacy)
        r = review_activity_handoff(p)
        self.assertFalse(r["declared_activity_ready_not_authenticated"])
        self.assertEqual(r["human_review_declarations_status"],
                         "LEGACY_SCOPE_CONTINUITY_REQUIRED")
        p["legacy_unchanged_scope_ref"] = "project/unchanged-old-task"
        self.assertTrue(review_activity_handoff(p)["declared_activity_ready_not_authenticated"])

    def test_new_h8_agent_decision_is_not_accepted(self):
        human = packet("H8")
        human["decisions"]["H8"] = declared_step("H8", kind="AGENT_DECIDED")
        p = activity_packet("05", human)
        r = review_activity_handoff(p)
        self.assertFalse(r["declared_activity_ready_not_authenticated"])
        self.assertIn("H8", r["human_review_declarations_missing"])


if __name__ == "__main__":
    unittest.main()
