"""Focused policy-routing regression; live Agent behavior requires blinded replay.

No model calls, research runs, external transfer, file creation, or SEALED reads.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(path):
    return (ROOT / path).read_text(encoding="utf-8")


class ThreeIssueRoutingTests(unittest.TestCase):
    def test_delivery_reuses_l1_l2_l3_and_has_real_completion_check(self):
        policy = text("NEXT_ACTION_POLICY.md")
        agent = text("AGENTS.md")
        for level in ("L1", "L2", "L3"):
            self.assertIn(level, policy)
        for required in (
            "DELIVERY_CHECK", "唯一首选最终成果", "实际存在",
            "SEALED", "NOT_RUN", "多文件整体交付", "而非第三本科研日志",
        ):
            with self.subTest(required=required):
                self.assertIn(required, policy)
        self.assertIn("DELIVERY_CHECK", agent)
        self.assertIn("NEXT_ACTION_POLICY.md", agent)
        self.assertIn("原L1/L2/L3做", agent)

    def test_falsification_stops_only_low_value_branch(self):
        loop = text("EXPERIMENT_LOOP.md")
        for required in (
            "RISK_TO_DECISION", "IF_POS/NEG/INVALID", "NEW_INFORMATION",
            "COST", "STOP_OR_CONTINUE", "BOUNDED_UNKNOWN",
            "泄漏", "SEALED污染", "当前细节分支",
            "不设固定失败次数", "不自动STOP项目",
        ):
            with self.subTest(required=required):
                self.assertIn(required, loop)
        self.assertIn("EXPERIMENT_LOOP.md", text("AGENTS.md"))

    def test_user_suggestion_is_not_approval_or_mandatory_disagreement(self):
        strategic = text("AUTHOR_STRATEGY_REVIEW.md")
        technical = text("ALGORITHM_ENGINEERING.md")
        for word in ("IDEA", "EXPLICIT_INSTRUCTION", "STRATEGIC_CHOICE",
                     "KEEP_CURRENT / ADOPT / LIMITED_PROBE / REJECT",
                     "机械反对", "不能为迎合用户"):
            with self.subTest(word=word):
                self.assertIn(word, strategic)
        for word in ("IDEA", "ADOPT / LIMITED_DEV_PROBE / NOT_RECOMMENDED",
                     "无新证据", "明确要求", "额外设审核"):
            with self.subTest(word=word):
                self.assertIn(word, technical)
        self.assertIn("AUTHOR_STRATEGY_REVIEW.md", text("AGENTS.md"))

    def test_checkpoints_are_positioned_before_the_decisions_they_guard(self):
        agent = text("AGENTS.md")
        workflow = text("WORKFLOW.md")
        loop = text("EXPERIMENT_LOOP.md")
        policy = text("NEXT_ACTION_POLICY.md")

        # A rule only added at the bottom of AGENTS is not a sufficient trigger.
        self.assertLess(agent.index("三个执行时点"), agent.index("## 0. 冷启动与版本"))
        self.assertIn("接收用户新建议时", agent.split("## 0. 冷启动与版本")[0])
        self.assertIn("决定下一项证伪/实验前", agent.split("## 0. 冷启动与版本")[0])
        self.assertIn("交付或结束任务前", agent.split("## 0. 冷启动与版本")[0])

        # Main scientific router and topic both gate probes BEFORE choosing one.
        self.assertLess(workflow.index("在产生下一项`NEXT_PROBE`"), workflow.index("1. **真实性/权限**"))
        self.assertLess(loop.index("NEXT_PROBE选择前的决策筛选"), loop.index("高价值机制实验选择"))
        self.assertEqual(loop.count("NEXT_PROBE选择前的决策筛选"), 1)
        self.assertIn("NO_DECISIVE_PROBE", loop)

        # User suggestion handling occurs before action ownership / A-B routing.
        self.assertLess(policy.index("用户新建议的入口分流"), policy.index("- `AGENT_DECIDABLE`"))
        self.assertLess(policy.index("返回结果前的实际检查顺序"), policy.index("**已执行结果与后续行动分开**"))
        self.assertIn("core.delivery_check", policy)

    def test_multifile_delivery_does_not_depend_on_l3_label(self):
        policy = text("NEXT_ACTION_POLICY.md")
        self.assertIn("L1/L2/L3仅决定回复深度", policy)
        self.assertIn("任何等级只要存在多个独立最终交付物", policy)
        self.assertNotIn("L3出现多个独立最终产物且没有清晰入口时才", policy)
        self.assertIn("多文件", text("AGENTS.md"))

    def test_agent_document_routes_are_real_table_rows(self):
        agent = text("AGENTS.md")
        self.assertNotIn(r"\\n|", agent)
        lines = agent.splitlines()
        blueprint = [i for i, line in enumerate(lines) if line.startswith(
            "| **按工作流生成/更新论文框架")]
        self.assertEqual(len(blueprint), 1)
        self.assertTrue(lines[blueprint[0]+1].startswith(
            "| 正文撰写/已有稿审核/Word |"))
        self.assertIn("WRITING_LOCKED", agent)

    def test_dev_entry_requires_strategy_and_separate_download_permission(self):
        loop = text("EXPERIMENT_LOOP.md")
        engineering = text("ALGORITHM_ENGINEERING.md")
        self.assertIn("作者已选/委托H6策略", loop)
        self.assertIn("独立取得对应下载许可", loop)
        self.assertIn("有效H5、作者已选/委托H6策略", engineering)
        self.assertNotIn("H5后的`AI_DEV_AUTONOMY`", engineering)

    def test_replay_spec_contains_positive_and_negative_controls(self):
        replay = text("REPLAY_PROTOCOL.md")
        for case in ("L1普通修复", "L3多文件任务", "非关键的重复疑点",
                     "真值/泄漏/确认污染", "用户暗示不必要的复杂模型",
                     "用户提出有价值新机制或明确合法技术指令"):
            with self.subTest(case=case):
                self.assertIn(case, replay)
        self.assertIn("NOT_MEASURED", replay)
        self.assertIn("实际响应与独立可核", replay)


if __name__ == "__main__":
    unittest.main()
