"""Static policy-regression checks for adaptive reporting and overall Token efficiency.

Not a live-agent benchmark or scientific-result validation.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def doc(name):
    return (ROOT / name).read_text(encoding="utf-8")


class AdaptiveOutputTokenPolicyTests(unittest.TestCase):
    def test_one_existing_output_owner_no_new_report_contract(self):
        agent = doc("AGENTS.md")
        policy = doc("NEXT_ACTION_POLICY.md")
        self.assertIn("NEXT_ACTION_POLICY.md", agent)
        self.assertIn("自适应 L1/L2/L3", agent)
        self.assertIn("唯一权威", policy)
        self.assertFalse((ROOT / "OUTPUT_CONTRACT.md").exists())
        self.assertLess(len(agent), 4500)

    def test_adaptive_levels_are_not_word_limits_or_required_templates(self):
        policy = doc("NEXT_ACTION_POLICY.md")
        for marker in ("\u0060L1\u0060", "\u0060L2\u0060", "\u0060L3\u0060",
                       "不统一版式", "不是固定标题", "只是指导"):
            self.assertIn(marker, policy)
        self.assertIn("不是固定标题", policy)
        self.assertIn("跨阶段自适应", policy)
        self.assertIn("科研正确性", policy)

    def test_results_distinct_from_next_instruction_and_user_choice(self):
        policy = doc("NEXT_ACTION_POLICY.md")
        self.assertIn("已执行结果与后续行动分开", policy)
        self.assertIn("NEXT_AGENT_INSTRUCTION", policy)
        self.assertIn("USER_DECISION_REQUIRED", policy)
        self.assertIn("NO_NEXT_ACTION", policy)
        self.assertIn("不提供依赖待决选择的执行命令", policy)
        self.assertIn("两种结果不可混淆", policy)

    def test_reuse_and_risk_sensitive_checks(self):
        policy = doc("NEXT_ACTION_POLICY.md")
        for marker in ("Token", "定向读取", "复用", "按风险", "多Agent",
                       "总成本", "真实Run", "全量", "返工"):
            self.assertIn(marker, policy)
        for gate in ("CPU/GPU", "SEALED", "写稿", "绘图", "权限"):
            self.assertIn(gate, policy)
        self.assertIn("不因省Token拒绝", policy)

    def test_md_persistence_is_event_driven_not_per_turn(self):
        docs = doc("DUAL_DOCUMENT_WORKFLOW.md")
        for marker in ("L1/L2/L3", "聊天简报", "RESEARCH_RECORD.md",
                       "PAPER_BLUEPRINT.md", "不新增第三份常设台账",
                       "普通Debug", "用户要求独立交付"):
            self.assertIn(marker, docs)
        self.assertIn("Token高效且证据可靠", docs)
        self.assertIn("原始失败与依据仍需可追溯", docs)

    def test_unchanged_human_and_figure_writing_gates(self):
        agent = doc("AGENTS.md")
        policy = doc("NEXT_ACTION_POLICY.md")
        for marker in ("H1–H10", "WRITING_LOCKED", "FIGURE_POLICY.md",
                       "SEALED"):
            self.assertIn(marker, agent)
        self.assertIn("USER_DECISION_REQUIRED", policy)
        self.assertIn("下载", policy)
        self.assertIn("WRITING_LOCKED", policy)


if __name__ == "__main__":
    unittest.main()
