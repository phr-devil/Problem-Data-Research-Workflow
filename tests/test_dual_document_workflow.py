"""Static tests of the two-file research memory and manuscript planning boundary."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def doc(path):
    return (ROOT / path).read_text(encoding="utf-8")


class DualDocumentTests(unittest.TestCase):
    def test_template_coverage(self):
        research = doc("templates/RESEARCH_RECORD.md")
        blueprint = doc("templates/PAPER_BLUEPRINT.md")
        for marker in ("当前快照", "EXP-001", "已完成", "失败复盘", "下一步", "NOT_RUN"):
            self.assertIn(marker, research)
        for marker in ("# 1. Introduction", "## 1.1", "## 4.2",
                       "Claim", "拟写", "NOT_RUN", "非正文"):
            self.assertIn(marker, blueprint)

    def test_entrypoint_and_state_links(self):
        for path in ("AGENTS.md", "START.md", "README.md", "WORKFLOW.md",
                     "WRITING_GATE.md", "NEXT_ACTION_POLICY.md"):
            with self.subTest(path=path):
                self.assertIn("DUAL_DOCUMENT_WORKFLOW.md", doc(path))
        state = doc("templates/STATE.md")
        self.assertIn("RESEARCH_RECORD_REF", state)
        self.assertIn("PAPER_BLUEPRINT_REF", state)

    def test_planning_is_not_drafting_authorization(self):
        gate = doc("WRITING_GATE.md")
        for word in ("H1/H2", "用户审查", "独立的明确写作授权",
                     "原始用户授权", "WRITING_LOCKED",
                     "不得为写作锁停止", "明确要求", "初稿"):
            with self.subTest(word=word):
                self.assertIn(word, gate)
        policy = doc("DUAL_DOCUMENT_WORKFLOW.md")
        for word in ("只修订相关节", "不强制迁移", "失败",
                     "恢复条件", "用户明确"):
            with self.subTest(word=word):
                self.assertIn(word, policy)


if __name__ == "__main__":
    unittest.main()
