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
        self.assertIn("real tool", read("EXECUTION_ASSURANCE.md").lower()
                      .replace("实际工具", "real tool"))

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
