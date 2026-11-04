"""Static regression: completed algorithms can be scientifically audited without drafting papers."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


class PostAlgorithmScienceAuditTests(unittest.TestCase):
    def test_optional_route_is_discoverable(self):
        for name in ("README.md", "AGENTS.md", "START.md", "WORKFLOW.md",
                     "PAPER_FIRST.md", "ALGORITHM_ENGINEERING.md",
                     "FEASIBILITY_ENVELOPE.md", "REFERENCES.md"):
            with self.subTest(file=name):
                self.assertIn("POST_ALGORITHM_SCIENCE_AUDIT.md", read(name))

    def test_distinct_predication_and_baseline(self):
        policy = read("POST_ALGORITHM_SCIENCE_AUDIT.md")
        for phrase in ("最近邻", "竞争解释", "独立", "成本",
                       "UPGRADE_PILOT", "EVIDENCE_ONLY",
                       "KEEP_ORIGINAL", "UNKNOWN",
                       "WRITING_GATE.md"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, policy)

    def test_no_unapproved_drafting_or_fit(self):
        policy = read("POST_ALGORITHM_SCIENCE_AUDIT.md")
        self.assertIn("不得自动写论文", policy)
        self.assertIn("没有训练授权", policy)
        self.assertNotIn("优先补证据、准备初稿", read("ALGORITHM_ENGINEERING.md"))
        self.assertIn("MANUSCRIPT_WRITE_AUTH", read("templates/STATE.md"))
        self.assertIn("WRITING_LOCKED", read("WRITING_GATE.md"))


if __name__ == "__main__":
    unittest.main()
