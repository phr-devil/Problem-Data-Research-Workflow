"""Static regression: Q2+ publication potential is research success, not acceptance or writing approval."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class Q2PublicationGoalTests(unittest.TestCase):
    def test_goal_and_outcomes(self):
        goal = read("Q2_PUBLICATION_GOAL.md")
        for phrase in ("Q2_POTENTIAL_SUPPORTED", "Q2_UPGRADE_POSSIBLE",
                       "Q2_UNCERTAIN", "BELOW_Q2_TARGET", "Q1",
                       "实际录用/发表不是科研项目成功的必要条件",
                       "WRITING_LOCKED", "JCR_EDITION", "CATEGORY"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, goal)

    def test_entrypoints_and_scientific_stages(self):
        for path in ("README.md", "AGENTS.md", "START.md", "WORKFLOW.md",
                     "PAPER_FIRST.md", "SEARCH_DISCOVERY.md",
                     "TASK_EXPLORATION.md", "ALGORITHM_ENGINEERING.md",
                     "VENUE_STRATEGY.md", "POST_ALGORITHM_SCIENCE_AUDIT.md",
                     "CONFIRMATION.md", "templates/STATE.md"):
            with self.subTest(path=path):
                self.assertIn("Q2_PUBLICATION_GOAL.md", read(path))

    def test_venue_selection_cannot_substitute_q3_q4(self):
        venue = read("VENUE_STRATEGY.md")
        self.assertIn("FALLBACK", venue)
        self.assertIn("Q3/Q4", venue)
        self.assertIn("不要求实际", read("PAPER_FIRST.md"))
        self.assertIn("MANUSCRIPT_WRITE_AUTH", read("templates/STATE.md"))
        self.assertIn("WRITING_LOCKED", read("WRITING_GATE.md"))


if __name__ == "__main__":
    unittest.main()
