"""Offline behavioral checks for the preflight; no real permissions inferred."""
import unittest

from core.execution_preflight import action_preflight, science_checkpoint


class ActionTests(unittest.TestCase):
    def test_unknown_effect_fails_closed(self):
        self.assertEqual(action_preflight({"action": "MYSTERY"})["decision"], "BLOCK")

    def test_readonly_is_legal_but_not_approval_for_other_effects(self):
        self.assertEqual(action_preflight({"action": "READ_PUBLIC"})["decision"], "ALLOW")

    def test_restricted_agent_claims_never_authenticate_grants(self):
        for effect in ("DOWNLOAD", "READ_SEALED", "RUN_CONFIRMATION",
                       "WRITE_MANUSCRIPT", "DRAW_IMAGE", "SUBMIT", "PAY",
                       "EXTERNAL_UPLOAD", "PROJECT_SCOPE_CHANGE", "PROJECT_STOP"):
            got = action_preflight({"action": effect, "authorization_verified": True,
                                    "user_approved": True, "authorization_ref": "fake"})
            self.assertEqual(got["decision"], "UNKNOWN", effect)

    def test_explicit_denial_blocks(self):
        self.assertEqual(action_preflight({"action": "DEV_TRAIN",
                                           "explicit_prohibition": True})["decision"], "BLOCK")

    def test_dev_has_no_per_run_human_approval_but_scope_check(self):
        p = {"action": "DEV_TRAIN", "h5_scope_confirmed": True,
             "dev_inputs_verified": True, "within_h5_scope": True,
             "within_author_selected_strategy": True,
             "h6_author_strategy_confirmed": True,
             "safe_local_nonpaid": True, "no_project_specific_prohibition": True}
        self.assertEqual(action_preflight(p)["decision"], "UNKNOWN")
        self.assertEqual(action_preflight(p, independently_authorized=True)["decision"], "ALLOW")
        p["within_h5_scope"] = False
        self.assertEqual(action_preflight(p, independently_authorized=True)["decision"], "BLOCK")

    def test_dev_missing_author_strategy_is_not_implicitly_approved(self):
        p = {"action": "DEV_TRAIN", "h5_scope_confirmed": True,
             "dev_inputs_verified": True, "within_h5_scope": True,
             "within_author_selected_strategy": True,
             "safe_local_nonpaid": True, "no_project_specific_prohibition": True}
        self.assertEqual(action_preflight(p, independently_authorized=True)["decision"], "UNKNOWN")
        p["h6_strategy_pending"] = True
        self.assertEqual(action_preflight(p, independently_authorized=True)["decision"], "BLOCK")

    def test_unchanged_legacy_strategy_does_not_require_reapproval(self):
        p = {"action": "DEV_TRAIN", "h5_scope_confirmed": True,
             "dev_inputs_verified": True, "within_h5_scope": True,
             "within_author_selected_strategy": True,
             "legacy_unchanged_scope_confirmed": True,
             "safe_local_nonpaid": True, "no_project_specific_prohibition": True}
        self.assertEqual(action_preflight(p, independently_authorized=True)["decision"], "ALLOW")

    def test_protected_action_requires_host_attestation(self):
        self.assertEqual(action_preflight({"action": "READ_SEALED"},
                                          independently_authorized=True)["decision"], "ALLOW")


class MalformedPacketTests(unittest.TestCase):
    def test_malformed_action_is_blocked_not_exception(self):
        for p in (None, [], {"action": []}, {"action": {"wrong": "type"}}):
            self.assertEqual(action_preflight(p)["decision"], "BLOCK")

    def test_forbidden_read_and_dev_are_not_allowed(self):
        self.assertEqual(action_preflight({
            "action": "READ_PUBLIC", "effect_forbidden": True
        })["decision"], "BLOCK")

    def test_malformed_science_and_option_fields_are_blocked(self):
        from core.execution_preflight import author_strategy_review
        for p in (None, [], {"trigger": []}):
            self.assertEqual(science_checkpoint(p)["result"], "BLOCK_HANDOFF")
        p = {"trigger": "H6_TASK",
             "author_review": {"options": [{
                 "id": "A", "primary_type": {}, "route": [],
                 "p_orientation": {"bad": True}
             }]}}
        self.assertEqual(author_strategy_review(p)["result"], "BLOCK_HANDOFF")
        self.assertEqual(science_checkpoint({"trigger": "CLAIM_PROMOTION",
                                            "claim_status": []})["result"], "BLOCK_HANDOFF")

    def test_secondary_dev_supported_does_not_trigger_author_strategy(self):
        p = {"trigger": "CLAIM_PROMOTION", "route": "R5", "primary_type": "C09",
             "claim_or_question": "Metric error", "nearest_neighbor_or_unknown": "paper",
             "actual_evidence_ref_or_not_run": "runs/123", "negative_evidence_or_none": "NONE",
             "strongest_alternative_or_unknown": "confound", "next_decisive_step": "probe",
             "independent_validation_ref_or_unavailable": "UNAVAILABLE",
             "claim_status": "SUPPORTED", "claim_role": "SECONDARY_DEV"}
        self.assertEqual(science_checkpoint(p)["result"], "READY_FOR_SCIENTIFIC_REVIEW")
        p["claim_role"] = "PRIMARY_FROZEN"
        self.assertIn("author_selected_main_claim_or_unchanged_legacy",
                      science_checkpoint(p)["missing"])

    def test_whitespace_unavailable_not_independent_confirmation(self):
        p = {"trigger": "CLAIM_PROMOTION", "route": "R5", "primary_type": "C09",
             "claim_or_question": "Metric error", "nearest_neighbor_or_unknown": "paper",
             "actual_evidence_ref_or_not_run": "runs/123", "negative_evidence_or_none": "NONE",
             "strongest_alternative_or_unknown": "confound", "next_decisive_step": "probe",
             "independent_validation_ref_or_unavailable": " UNAVAILABLE ",
             "claim_status": "CONFIRMED", "claim_role": "SECONDARY_DEV"}
        self.assertIn("confirmed_needs_real_independent_evidence",
                      science_checkpoint(p)["missing"])


class ScienceTests(unittest.TestCase):
    @staticmethod
    def sample_author_packet(trigger="H6_TASK"):
        option = {"id": "A", "claim_or_task": "Trustworthy contact",
                  "primary_type": "C11", "route": "R4", "p_orientation": "P3",
                  "independent_knowledge": "Boundary by contact state",
                  "prior_gap": "Unknown on measured data",
                  "decisive_evidence": "Cross-session contrast",
                  "science_value": "Broad failure criterion",
                  "cost_and_speed": "Reuses DEV runs",
                  "failure_premise": "Wrong labels"}
        review = {"options": [option], "single_option_reason": "Only feasible data",
                  "recommended_option_id": "A",
                  "recommendation_rationale": "Valid independent groups",
                  "key_unknown": "Sensor axis not fully checked"}
        if trigger == "H8_CLAIM":
            option["h8_action"] = "KEEP"
            review.update(positive_negative_evidence_ref="runs/R12",
                          strongest_objection="Session confounding",
                          publication_potential_or_unknown="UNKNOWN",
                          confirmation_gap="SEALED not yet authorized")
        packet = {"trigger": trigger,
                  "claim_or_question": "When can contact fail?",
                  "nearest_neighbor_or_unknown": "UNKNOWN",
                  "primary_type": "C11", "route": "R4",
                  "author_review": review}
        if trigger == "H8_CLAIM":
            packet.update(actual_evidence_ref_or_not_run="runs/R12",
                          negative_evidence_or_none="No overall gain",
                          strongest_alternative_or_unknown="Session confounding",
                          next_decisive_step="DEV group comparison")
        return packet

    def test_h6_proposal_needs_author_selection(self):
        p = self.sample_author_packet()
        self.assertEqual(science_checkpoint(p)["result"], "AUTHOR_CHOICE_REQUIRED")
        p["author_review"]["selection"] = {
            "kind": "USER_CONFIRMED",
            "chosen_option_id": "A",
            "original_user_message_ref": "user-message-2026-11-12"}
        self.assertEqual(science_checkpoint(p)["result"], "READY_FOR_SCIENTIFIC_REVIEW")
        self.assertFalse(science_checkpoint(p)["author_approval_authenticated"])

    def test_fake_author_approval_is_not_a_selection(self):
        p = self.sample_author_packet()
        p["author_review"]["user_approved"] = True
        p["author_review"]["selection"] = {"kind": "AGENT_DECIDED",
                                            "original_user_message_ref": "agent"}
        self.assertEqual(science_checkpoint(p)["result"], "AUTHOR_CHOICE_REQUIRED")

    def test_author_scope_delegation_is_acceptable_declaration(self):
        p = self.sample_author_packet()
        p["author_review"]["selection"] = {
            "kind": "USER_DELEGATED", "delegated_scope": "R4 within H5; no SEALED",
            "original_user_message_ref": "user-message"}
        self.assertEqual(science_checkpoint(p)["result"], "READY_FOR_SCIENTIFIC_REVIEW")

    def test_h8_requires_author_upgrade_choice(self):
        p = self.sample_author_packet("H8_CLAIM")
        self.assertEqual(science_checkpoint(p)["result"], "AUTHOR_CHOICE_REQUIRED")
        p["author_review"]["selection"] = {
            "kind": "USER_CONFIRMED", "chosen_option_id": "A",
            "original_user_message_ref": "author-choice"}
        self.assertEqual(science_checkpoint(p)["result"], "READY_FOR_SCIENTIFIC_REVIEW")

    def test_missing_recommendation_or_fallback_cannot_pass(self):
        p = self.sample_author_packet()
        del p["author_review"]["recommendation_rationale"]
        del p["author_review"]["single_option_reason"]
        p["author_review"]["selection"] = {"kind": "USER_CONFIRMED",
                                            "chosen_option_id": "A",
                                            "original_user_message_ref": "author"}
        self.assertEqual(science_checkpoint(p)["result"], "BLOCK_HANDOFF")

    def test_non_author_checkpoint_remains_autonomous(self):
        p = {"trigger": "NEW_ALGORITHM",
             "observed_bottleneck_or_hypothesis": "Weak contact boundary",
             "simple_alternative": "threshold baseline",
             "distinguishing_prediction": "failures vanish with state awareness"}
        self.assertEqual(science_checkpoint(p)["result"], "READY_FOR_SCIENTIFIC_REVIEW")

    def test_negative_results_are_not_dropped(self):
        p = {"trigger": "NEGATIVE_RESULT", "actual_evidence_ref_or_not_run": "runs/R1",
             "strongest_alternative_or_unknown": "UNKNOWN",
             "next_decisive_step": "check subject split"}
        self.assertIn("negative_evidence_or_none", science_checkpoint(p)["missing"])
        p["negative_evidence_or_none"] = "R1 has no gain"
        self.assertEqual(science_checkpoint(p)["result"], "READY_FOR_SCIENTIFIC_REVIEW")

    def test_claim_promotion_requires_author_claim_for_support(self):
        p = {"trigger": "CLAIM_PROMOTION", "route": "R5", "primary_type": "C09",
             "claim_or_question": "metric bias", "nearest_neighbor_or_unknown": "paper/a",
             "actual_evidence_ref_or_not_run": "runs/R2",
             "negative_evidence_or_none": "none",
             "strongest_alternative_or_unknown": "dataset issue",
             "next_decisive_step": "independent confirmation",
             "independent_validation_ref_or_unavailable": "UNAVAILABLE",
             "claim_status": "SUPPORTED"}
        self.assertIn("author_selected_main_claim_or_unchanged_legacy",
                      science_checkpoint(p)["missing"])
        p["h8_author_choice_ref"] = "user/original-H8-choice"
        self.assertEqual(science_checkpoint(p)["result"], "READY_FOR_SCIENTIFIC_REVIEW")
        p["claim_status"] = "CONFIRMED"
        self.assertIn("confirmed_needs_real_independent_evidence",
                      science_checkpoint(p)["missing"])

    def test_no_fake_supported_claim(self):
        p = {"trigger": "CLAIM_PROMOTION", "route": "R5", "primary_type": "C09",
             "claim_or_question": "metric bias", "nearest_neighbor_or_unknown": "UNKNOWN",
             "actual_evidence_ref_or_not_run": "NOT_RUN",
             "negative_evidence_or_none": "NONE",
             "strongest_alternative_or_unknown": "UNKNOWN",
             "next_decisive_step": "evaluate valid groups",
             "independent_validation_ref_or_unavailable": "UNAVAILABLE",
             "claim_status": "SUPPORTED"}
        self.assertIn("real_evidence_for_supported_claim", science_checkpoint(p)["missing"])
        p["claim_status"] = "HYPOTHESIZED"
        self.assertEqual(science_checkpoint(p)["result"], "READY_FOR_SCIENTIFIC_REVIEW")


if __name__ == "__main__":
    unittest.main()
