"""Read-only tests for two-file cold-start navigation, outline hierarchy and preserved gates."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def doc(path):
    return (ROOT / path).read_text(encoding="utf-8")


class DualDocumentTests(unittest.TestCase):
    def test_template_coverage_and_history_last(self):
        research = doc("templates/RESEARCH_RECORD.md")
        for marker in ("当前快照", "EXP-001", "已完成", "失败复盘", "下一步", "NOT_RUN", "SOURCE_CONFLICT"):
            self.assertIn(marker, research)
        self.assertLess(research.index("## 0. 当前快照"),
                        research.index("## 2. 已完成工作"))
        self.assertLess(research.index("## 4. 下一步任务"),
                        research.index("## 5. 重要尝试与决策历史"))
        self.assertLess(research.index("## 5. 重要尝试与决策历史"),
                        research.index("### EXP-001"))

    def test_blueprint_has_unambiguous_heading_tree_and_ids(self):
        blueprint = doc("templates/PAPER_BLUEPRINT.md")
        h1 = re.findall(r"(?m)^# (?!#).+$", blueprint)
        chapters = re.findall(r"(?m)^## ([1-6])\. (.+)$", blueprint)
        subheads = re.findall(r"(?m)^### ([1-6])\.(\d+) (.+)$", blueprint)
        ids = re.findall(r"(?m)^- SEC_ID: (SEC-[A-Z0-9-]+)$", blueprint)
        self.assertEqual(len(h1), 1)
        self.assertEqual([int(n) for n, _ in chapters], list(range(1, 7)))
        self.assertEqual(len(ids), len(subheads))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(any(int(chap) == int(n) for n, _ in chapters)
                            for chap, _, _ in subheads))
        for marker in ("Claim", "拟写", "NOT_RUN", "非正文", "RESEARCH_RECORD.md"):
            self.assertIn(marker, blueprint)

    def test_entrypoint_and_state_links(self):
        for path in ("AGENTS.md", "START.md", "README.md", "WORKFLOW.md",
                     "WRITING_GATE.md", "NEXT_ACTION_POLICY.md"):
            with self.subTest(path=path):
                self.assertIn("DUAL_DOCUMENT_WORKFLOW.md", doc(path))
        state = doc("templates/STATE.md")
        self.assertIn("RESEARCH_RECORD_REF", state)
        self.assertIn("PAPER_BLUEPRINT_REF", state)
        agent = doc("AGENTS.md")
        self.assertIn("唯一默认入口", agent)
        self.assertIn("当前快照", agent)
        self.assertIn("按实际阻碍", agent)
        self.assertIn("原始", agent)
        self.assertIn("WORKFLOW.md", agent)

    def test_preserved_science_and_authorization(self):
        workflow = doc("WORKFLOW.md")
        self.assertIn("三个决策循环（六项活动", workflow)
        for stage in ("01", "02", "03", "04", "05", "06"):
            self.assertIn(stage, workflow)
        gate = doc("WRITING_GATE.md")
        for word in ("H1/H2", "用户审查", "独立的明确写作授权",
                     "原始用户授权", "WRITING_LOCKED",
                     "不得为写作锁停止", "明确要求", "初稿"):
            self.assertIn(word, gate)
        agent = doc("AGENTS.md")
        for term in ("COMPETING_CHOICE", "HIGH_VALUE_RESEARCH_DESIGN.md",
                     "SCIENCE_RESULT_HARVEST.md", "POST_ALGORITHM_SCIENCE_AUDIT.md",
                     "FIGURE_POLICY.md", "SEALED", "Q2", "WRITING_LOCKED"):
            self.assertIn(term, agent)
        policy = doc("DUAL_DOCUMENT_WORKFLOW.md")
        for word in ("只修订相关节", "不强制迁移", "失败", "恢复条件", "用户明确",
                     "SEC_ID", "SOURCE_CONFLICT"):
            self.assertIn(word, policy)


if __name__ == "__main__":
    unittest.main()
