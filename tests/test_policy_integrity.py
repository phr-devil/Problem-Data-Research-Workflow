"""Cross-layer policy invariants: prevents rule drift, NOT real Agent compliance."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class PolicyIntegrityTests(unittest.TestCase):
    def test_h_node_owner_and_version_stay_aligned(self):
        review = json.loads(read("contracts/human_review_protocol.v1.json"))
        self.assertEqual(review["protocol_version"], "pd-rw-human-review-v1.3")
        self.assertEqual(list(review["steps"]), [f"H{i}" for i in range(1, 11)])
        for node in ("H6", "H8"):
            self.assertEqual(review["steps"][node]["decision_owner"], "USER")
        self.assertEqual(review["steps"]["H7"]["decision_owner"], "AGENT")
        self.assertIn("pd-rw-human-review-v1.2", review["legacy_protocol_versions"])
        self.assertIn("AUTHOR_STRATEGY_REVIEW.md", read("WORKFLOW.md"))
        self.assertEqual(review["new_project_interaction"]["single_author_card"], "H6")
        self.assertEqual(review["new_project_interaction"]["agent_candidate_preparation"], ["H3", "H4", "H5"])
        self.assertFalse(review["new_project_interaction"]["generic_continue_is_choice"])
        self.assertIn("单次方案选择", read("WORKFLOW.md"))

    def test_h6_bundled_choice_declares_one_author_message_not_four(self):
        from core.human_decision_review import review

        def user(ref):
            return {"kind": "USER_CONFIRMED",
                    "original_user_message_ref": ref, "chosen_option": "A"}

        entries = {"H1": user("launch"), "H2": user("launch")}
        entries.update({node: {**user("h6-reply"), "plan_sha256": "a" * 64}
                        for node in ("H3", "H4", "H5", "H6")})
        packet = {"format": "pd-rw-human-review-v1",
                  "target": "H6", "decisions": entries,
                  "new_project_h6_bundle": True}
        ok = review(packet)
        self.assertTrue(ok["can_advance_declarations_only"])
        self.assertFalse(ok["allows_download_training_sealed_or_writing"])
        packet["decisions"]["H4"] = user("agent-invented-ref")
        bad = review(packet)
        self.assertFalse(bad["can_advance_declarations_only"])
        self.assertIn("H4", bad["malformed_declarations"])

    def test_canonical_new_project_h6_entry_cannot_be_skipped_by_packet_omission(self):
        from core.human_decision_review import CONTRACT, review_new_project_h6

        def declared(node, reply):
            spec = CONTRACT["steps"][node]
            row = {"kind": "USER_CONFIRMED", "original_user_message_ref": reply,
                   "chosen_option": "A",
                   "dimension_decisions": {x: "CHOICE_A" for x in spec["required_dimensions"]},
                   "evidence_refs": {x: "source/a" for x in spec["evidence_minimum"]}}
            if node in {"H3", "H4", "H5", "H6"}:
                row["plan_sha256"] = "f" * 64
            return row

        rows = {node: declared(node, "launch" if node in {"H1", "H2"} else "reply")
                for node in ("H1", "H2", "H3", "H4", "H5", "H6")}
        packet = {"format": "pd-rw-human-review-v1",
                  "protocol_version": CONTRACT["protocol_version"],
                  "target": "H6", "decisions": rows}
        valid = review_new_project_h6(packet)
        self.assertTrue(valid["can_advance_declarations_only"])
        self.assertIsNone(valid["next_user_interaction"])
        self.assertFalse(valid["allows_download_training_sealed_or_writing"])

        for change in ("missing_h6", "wrong_option", "wrong_hash", "wrong_reply"):
            altered = json.loads(json.dumps(packet))
            if change == "missing_h6":
                del altered["decisions"]["H6"]
            elif change == "wrong_option":
                altered["decisions"]["H4"]["chosen_option"] = "B"
            elif change == "wrong_hash":
                altered["decisions"]["H5"]["plan_sha256"] = "b" * 64
            else:
                altered["decisions"]["H3"]["original_user_message_ref"] = "different"
            reviewed = review_new_project_h6(altered)
            self.assertFalse(reviewed["can_advance_declarations_only"], change)
            self.assertEqual(reviewed["next_user_interaction"], "H6")

    def test_new_project_dev_preflight_cannot_use_legacy_scope_as_h6(self):
        from core.execution_preflight import action_preflight
        packet = {"action": "DEV_TRAIN",
                  "h5_scope_confirmed": True, "dev_inputs_verified": True,
                  "within_h5_scope": True, "safe_local_nonpaid": True,
                  "no_project_specific_prohibition": True,
                  "within_author_selected_strategy": True,
                  "legacy_unchanged_scope_confirmed": True,
                  "h6_author_strategy_confirmed": False}
        new = action_preflight(packet, independently_authorized=True, new_project=True)
        self.assertEqual(new["reason"], "NEW_PROJECT_H6_CHOICE_REQUIRED")
        old = action_preflight(packet, independently_authorized=True, new_project=False)
        self.assertEqual(old["decision"], "ALLOW")

    def test_six_activities_preserved_and_joined_review_declared(self):
        activities = json.loads(read("contracts/research_activity_protocol.v1.json"))
        self.assertEqual(list(activities["activities"]), [f"0{i}" for i in range(1, 7)])
        for activity, trigger in (("03", "H6_TASK"), ("05", "H8_CLAIM")):
            spec = activities["activities"][activity]["strategy_checkpoint"]
            self.assertEqual(spec["trigger"], trigger)
            self.assertEqual(spec["packet_key"], "strategy_checkpoint_packet")
        source = read("core/contracts.py")
        self.assertIn("strategy_review_ready", source)
        self.assertIn("author_strategy_selection_mismatch", source)

    def test_preflight_keeps_protected_actions_advisory(self):
        code = read("core/execution_preflight.py")
        for label in ("independently_authorized", "READ_SEALED", "WRITE_MANUSCRIPT",
                      "AUTHOR_CHOICE_REQUIRED", "legacy_unchanged_scope_confirmed"):
            self.assertIn(label, code)
        self.assertIn("宿主", read("EXECUTION_ASSURANCE.md"))
        self.assertIn("尚未", read("EXECUTION_ASSURANCE.md"))

    def test_h7_is_not_a_per_run_human_gate(self):
        for filename in ("WORKFLOW.md", "AGENTS.md", "AUTHOR_STRATEGY_REVIEW.md",
                         "EXPERIMENT_LOOP.md", "NEXT_ACTION_POLICY.md"):
            body = read(filename)
            self.assertIn("H7", body)
        self.assertIn("不逐次", read("WORKFLOW.md"))
        self.assertIn("WRITING_LOCKED", read("WRITING_GATE.md"))
        self.assertIn("SEALED", read("CONFIRMATION.md"))

    def test_contribution_vocabulary_distinct(self):
        import core.execution_preflight as preflight
        self.assertEqual(len(preflight.TYPES), 12)
        self.assertEqual(len(preflight.ROUTES), 6)
        self.assertEqual(len(preflight.P_ORIENTATIONS), 5)
        self.assertIn("C12", preflight.TYPES)
        self.assertIn("R6", preflight.ROUTES)

    def test_ci_compiles_before_executing_tests_without_repeats(self):
        ci = read(".github/workflows/ci.yml")
        self.assertIn("compileall -q core evals tests", ci)
        self.assertEqual(ci.count("unittest discover -s tests -v"), 1)


if __name__ == "__main__":
    unittest.main()
