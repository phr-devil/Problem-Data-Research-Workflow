"""Static policy regression: Agent instructions must not turn evidence into writing permission."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def doc(path):
    return (ROOT / path).read_text(encoding="utf-8")


class ManuscriptWritingGateTests(unittest.TestCase):
    def test_entrypoints_point_to_lock(self):
        for path in ("AGENTS.md", "START.md", "WORKFLOW.md", "PAPER_FIRST.md",
                     "CONFIRMATION.md", "VENUE_STRATEGY.md", "README.md"):
            with self.subTest(path=path):
                self.assertIn("WRITING_GATE.md", doc(path))

    def test_two_independent_user_decisions(self):
        policy = doc("WRITING_GATE.md")
        self.assertIn("WRITING_LOCKED", policy)
        self.assertIn("用户审查", policy)
        self.assertIn("独立的明确写作授权", policy)
        self.assertIn("原始用户授权", policy)
        self.assertIn("不得为写作锁停止", policy)

    def test_persisted_state_defaults_to_locked(self):
        state = doc("templates/STATE.md")
        for field in ("RESEARCH_SUMMARY_REF", "SUMMARY_USER_REVIEW",
                      "MANUSCRIPT_WRITE_AUTH", "LOCKED"):
            self.assertIn(field, state)

    def test_early_outline_not_manuscript_draft(self):
        paper = doc("PAPER_FIRST.md")
        confirmation = doc("CONFIRMATION.md")
        self.assertNotIn("可先写标明证据缺口的论文框架", paper)
        self.assertNotIn("候选阶段写带**证据缺口标记**的提纲或初稿", paper)
        self.assertNotIn("`DRAFTABLE`允许写含缺口的初稿", confirmation)
        self.assertNotIn("允许提前写“计划验证的论文草稿”", confirmation)
        self.assertIn("不得写可投稿章节正文或初稿", paper)
        self.assertIn("PAPER_BLUEPRINT", paper)


if __name__ == "__main__":
    unittest.main()
