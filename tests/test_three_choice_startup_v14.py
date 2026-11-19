"""Synthetic v1.4 H3/H4/H6 choice chain; no authentication is implied."""
import copy
import unittest

from core.human_decision_review import CONTRACT, review_new_project_choices, review_new_project_h6
from core.execution_preflight import action_preflight


def row(step, choice="option", ref=None, digest=None):
    spec = CONTRACT["steps"][step]
    item = {
        "kind": "USER_CONFIRMED",
        "chosen_option": choice,
        "original_user_message_ref": ref or f"original-{step}",
        "dimension_decisions": {k: "declared-value" for k in spec["required_dimensions"]},
        "evidence_refs": {k: "synthetic-source-ref" for k in spec["evidence_minimum"]},
    }
    if digest:
        item["plan_sha256"] = digest
    return item


def packet():
    decisions = {s: row(s) for s in ("H1", "H2", "H3", "H4", "H5", "H6")}
    for step, digest in (("H3", "a"*64), ("H4", "b"*64), ("H6", "c"*64)):
        decisions[step]["plan_sha256"] = digest
    decisions["H5"]["plan_sha256"] = decisions["H6"]["plan_sha256"]
    decisions["H5"]["original_user_message_ref"] = decisions["H6"]["original_user_message_ref"]
    decisions["H5"]["chosen_option"] = decisions["H6"]["chosen_option"]
    h3, h4, h6 = (decisions[s] for s in ("H3", "H4", "H6"))
    def link(s):
        return {"plan_sha256": s["plan_sha256"],
                "original_user_message_ref": s["original_user_message_ref"],
                "choice": s["chosen_option"]}
    h4["upstream_h3"] = link(h3)
    h6["upstream_choices"] = {"H3": link(h3), "H4": link(h4)}
    return {
        "format": "pd-rw-human-review-v1",
        "protocol_version": "pd-rw-human-review-v1.4",
        "target": "H6", "decisions": decisions, "invalidated_decisions": [],
    }


class ThreeChoiceTests(unittest.TestCase):
    def test_three_distinct_replies_and_h5_h6_binding(self):
        result = review_new_project_choices(packet())
        self.assertTrue(result["can_advance_declarations_only"])
        self.assertTrue(result["new_project_three_choices_checked"])
        self.assertIsNone(result["next_user_interaction"])
        self.assertFalse(result["allows_download_training_sealed_or_writing"])

    def test_missing_h3_routes_to_first_choice(self):
        p = packet()
        del p["decisions"]["H3"]
        result = review_new_project_choices(p)
        self.assertFalse(result["can_advance_declarations_only"])
        self.assertEqual(result["next_user_interaction"], "H3")

    def test_missing_h4_or_stale_h4_link_rejected(self):
        p = packet()
        del p["decisions"]["H4"]
        self.assertFalse(review_new_project_choices(p)["can_advance_declarations_only"])
        p = packet()
        p["decisions"]["H4"]["upstream_h3"]["plan_sha256"] = "f"*64
        result = review_new_project_choices(p)
        self.assertIn("H4", result["malformed_declarations"])

    def test_reusing_one_reply_for_h3_h4_is_not_three_choices(self):
        p = packet()
        p["decisions"]["H4"]["original_user_message_ref"] = p["decisions"]["H3"]["original_user_message_ref"]
        p["decisions"]["H6"]["upstream_choices"]["H4"]["original_user_message_ref"] = p["decisions"]["H3"]["original_user_message_ref"]
        result = review_new_project_choices(p)
        self.assertFalse(result["can_advance_declarations_only"])
        self.assertIn("H4", result["malformed_declarations"])

    def test_changed_h3_invalidates_h4_h6(self):
        p = packet()
        p["invalidated_decisions"] = ["H3"]
        result = review_new_project_choices(p)
        self.assertIn("H4", result["stale_declarations"])
        self.assertIn("H6", result["stale_declarations"])
        self.assertFalse(result["can_advance_declarations_only"])

    def test_old_single_h6_historical_bundle_retained(self):
        p = packet()
        p["protocol_version"] = "pd-rw-human-review-v1.3"
        p["new_project_h6_bundle"] = True
        h6 = p["decisions"]["H6"]
        for name in ("H3", "H4", "H5"):
            p["decisions"][name]["kind"] = h6["kind"]
            p["decisions"][name]["original_user_message_ref"] = h6["original_user_message_ref"]
            p["decisions"][name]["chosen_option"] = h6["chosen_option"]
            p["decisions"][name]["plan_sha256"] = h6["plan_sha256"]
        result = review_new_project_h6(p)
        self.assertTrue(result["can_advance_declarations_only"])
        self.assertFalse(result["new_project_three_choices_checked"])

    def test_dev_gate_requires_chain_even_with_h6_flag(self):
        base = {"action":"DEV_TRAIN", "h5_scope_confirmed":True,
                "dev_inputs_verified":True, "within_h5_scope":True,
                "safe_local_nonpaid":True, "no_project_specific_prohibition":True,
                "within_author_selected_strategy":True,
                "h6_author_strategy_confirmed":True}
        denied = action_preflight(base, new_project=True, independently_authorized=True)
        self.assertEqual(denied["decision"], "BLOCK")
        self.assertEqual(denied["reason"], "NEW_PROJECT_THREE_CHOICES_REQUIRED")
        base["new_project_three_choices_confirmed"] = True
        allowed = action_preflight(base, new_project=True, independently_authorized=True)
        self.assertEqual(allowed["decision"], "ALLOW")


if __name__ == "__main__":
    unittest.main()
