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
             "safe_local_nonpaid": True, "no_project_specific_prohibition": True}
        self.assertEqual(action_preflight(p)["decision"], "UNKNOWN")
        self.assertEqual(action_preflight(p, independently_authorized=True)["decision"], "ALLOW")
        p["within_h5_scope"] = False
        self.assertEqual(action_preflight(p, independently_authorized=True)["decision"], "BLOCK")

    def test_protected_action_requires_host_attestation(self):
        self.assertEqual(action_preflight({"action": "READ_SEALED"},
                                          independently_authorized=True)["decision"], "ALLOW")


class ScienceTests(unittest.TestCase):
    def test_new_task_needs_contribution_route_not_only_algorithm(self):
        p = {"trigger": "H6_TASK", "claim_or_question": "When can contact fail?",
             "nearest_neighbor_or_unknown": "UNKNOWN"}
        self.assertEqual(science_checkpoint(p)["result"], "BLOCK_HANDOFF")
        p.update(route="R4", primary_type="C11")
        self.assertEqual(science_checkpoint(p)["result"], "READY_FOR_SCIENTIFIC_REVIEW")

    def test_negative_results_are_not_dropped(self):
        p = {"trigger": "NEGATIVE_RESULT", "actual_evidence_ref_or_not_run": "runs/R1",
             "strongest_alternative_or_unknown": "UNKNOWN",
             "next_decisive_step": "check subject split"}
        self.assertIn("negative_evidence_or_none", science_checkpoint(p)["missing"])
        p["negative_evidence_or_none"] = "R1 has no gain"
        self.assertEqual(science_checkpoint(p)["result"], "READY_FOR_SCIENTIFIC_REVIEW")

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
