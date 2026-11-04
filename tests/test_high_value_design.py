"""Static integration checks; not evidence of higher paper success rates."""
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


class HighValueDesignTests(unittest.TestCase):
    def test_existing_stages_link_high_value_design(self):
        for name in ("AGENTS.md", "START.md", "WORKFLOW.md", "SEARCH_DISCOVERY.md",
                     "DATA_DISCOVERY.md", "DATA_INSIGHT.md", "TASK_EXPLORATION.md",
                     "ALGORITHM_ENGINEERING.md", "EXPERIMENT_LOOP.md",
                     "PAPER_FIRST.md", "POST_ALGORITHM_SCIENCE_AUDIT.md", "README.md"):
            with self.subTest(name=name):
                self.assertIn("HIGH_VALUE_RESEARCH_DESIGN.md",
                              (ROOT / name).read_text(encoding="utf-8"))

    def test_rules_not_just_easy_performance(self):
        doc = (ROOT / "HIGH_VALUE_RESEARCH_DESIGN.md").read_text(encoding="utf-8")
        for marker in ("NAMED_NEAREST", "ALTERNATIVE", "CONFOUNDING",
                       "DISTINCT_PREDICTIONS", "Q2", "WRITING_GATE.md",
                       "NEXT_ACTION_POLICY.md", "Optuna"):
            with self.subTest(marker=marker):
                self.assertIn(marker, doc)
        self.assertIn("WRITING_LOCKED", (ROOT / "WRITING_GATE.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
