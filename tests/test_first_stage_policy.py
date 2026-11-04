"""Stage-01 policy integration: cheap-but-early decisions must face alternatives."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FirstStagePolicyTests(unittest.TestCase):
    def test_entrypoints_and_discovery_link_comparison(self):
        for path in ("AGENTS.md", "START.md", "WORKFLOW.md",
                     "SEARCH_DISCOVERY.md", "HIGH_VALUE_RESEARCH_DESIGN.md"):
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn("COMPETING_CHOICE", text)

    def test_early_data_review_and_recovery(self):
        self.assertIn("PRE_DOWNLOAD_SCIENCE_FIT",
                      (ROOT / "DATA_DISCOVERY.md").read_text(encoding="utf-8"))
        self.assertIn("PREDOWNLOAD_ASSUMPTION_REFUTED",
                      (ROOT / "DATA_INSIGHT.md").read_text(encoding="utf-8"))
        self.assertIn("SEARCH_CHOICE_REVIEW",
                      (ROOT / "templates/STATE.md").read_text(encoding="utf-8"))

    def test_original_sealed_and_writing_guards_remain(self):
        files = {p: (ROOT / p).read_text(encoding="utf-8") for p in
                 ("START.md", "WORKFLOW.md", "DATA_DISCOVERY.md",
                  "NEXT_ACTION_POLICY.md", "WRITING_GATE.md")}
        self.assertIn("WAITING_FOR_DOWNLOAD_AUTH", files["START.md"])
        self.assertIn("SEALED_CONFIRM", files["DATA_DISCOVERY.md"])
        self.assertIn("USER_DECISION_REQUIRED", files["NEXT_ACTION_POLICY.md"])
        self.assertIn("WRITING_LOCKED", files["WRITING_GATE.md"])


if __name__ == "__main__":
    unittest.main()
