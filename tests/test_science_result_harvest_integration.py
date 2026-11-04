"""Verify the science harvest integrates existing stages without unlocking paper writing."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScienceResultHarvestIntegrationTests(unittest.TestCase):
    def test_policy_used_across_stages(self):
        paths = ("AGENTS.md", "WORKFLOW.md", "DATA_INSIGHT.md",
                 "EXPERIMENT_LOOP.md", "PAPER_FIRST.md",
                 "POST_ALGORITHM_SCIENCE_AUDIT.md", "CONFIRMATION.md",
                 "WRITING_GATE.md", "README.md",
                 "Q2_PUBLICATION_GOAL.md", "HIGH_VALUE_RESEARCH_DESIGN.md",
                 "core/README.md", "templates/STATE.md")
        for path in paths:
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn("SCIENCE_RESULT_HARVEST.md", text)

    def test_no_evidence_inflation(self):
        policy = (ROOT / "SCIENCE_RESULT_HARVEST.md").read_text(encoding="utf-8")
        for phrase in ("MISSED_SCIENTIFIC_INFORMATION",
                       "UNDERARTICULATED_CONTRIBUTION",
                       "ARTICULATION_GAP", "EVIDENCE_GAP", "BOTH", "NONE",
                       "EXPLORATORY", "WRITING_LOCKED",
                       "CONTRIBUTION_EVIDENCE_BRIEF"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, policy)
        self.assertIn("WRITING_LOCKED",
                      (ROOT / "WRITING_GATE.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
