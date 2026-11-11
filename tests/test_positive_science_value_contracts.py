"""Static evidence-policy regression. Does not execute any research Agent or claim scientific performance."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class PositiveScientificValueContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.high = read("HIGH_VALUE_RESEARCH_DESIGN.md")
        cls.paper = read("PAPER_FIRST.md")
        cls.workflow = read("WORKFLOW.md")
        cls.confirm = read("CONFIRMATION.md")
        cls.search = read("SEARCH_DISCOVERY.md")
        cls.algorithm = read("ALGORITHM_ENGINEERING.md")
        cls.writing = read("MANUSCRIPT_WRITING.md")
        cls.qa = read("MANUSCRIPT_QA.md")
        cls.q2 = read("Q2_PUBLICATION_GOAL.md")
        cls.replay = read("REPLAY_PROTOCOL.md")
        cls.agents = read("AGENTS.md")

    def test_value_judgment_not_just_cheap_pilots(self):
        for label in ("SCIENTIFIC_CONSEQUENCE", "DISCRIMINATING_VALUE",
                      "TRANSFER_SCOPE_OR_JUSTIFIED_NARROWNESS",
                      "科学重要性与实验成本分开决策"):
            self.assertIn(label, self.high)

    def test_performance_free_insight_is_existing_claim_path(self):
        for label in ("无性能提升的科学洞见出口", "LAW_BOUNDARY_CLAIM",
                      "PAPER_PATH_CANDIDATE", "不新增 `INSIGHT_ESTABLISHED` 状态"):
            self.assertIn(label, self.paper)
        self.assertIn("即使没有算法性能改善", self.paper)
        self.assertNotIn("- `INSIGHT_ESTABLISHED`：", self.paper)

    def test_benchmark_and_system_contributions_are_not_guaranteed_novelty(self):
        self.assertIn("新基准、测量协议与系统级能力", self.paper)
        self.assertIn("只整理旧数据或拼接组件不自动成为新颖性", self.paper)
        self.assertIn("基准/任务/系统级路线", self.algorithm)
        self.assertIn("不能静默改变既有冻结评价器", self.algorithm)

    def test_science_upgrades_and_respects_authorization(self):
        for label in ("高价值实验的升级条件", "CLAIM_EVIDENCE_PACKAGE",
                      "新基准或实验范式", "AI_DEV_AUTONOMY",
                      "新增数据库下载", "付费/云资源", "SEALED仍独立许可"):
            self.assertIn(label, self.workflow)
        self.assertIn("H6–H8 是 AI 自主科学决策", self.workflow)
        self.assertIn("H5内DEV Task/算法/评价方案由AI版本化调整", self.workflow)
        self.assertIn("FIGURE_POLICY.md", self.workflow)

    def test_cross_paradigm_evidence_is_not_falsely_equated(self):
        for label in ("不同实验范式的独立支持", "三角互证", "不等于自动替代 SEALED 确认",
                      "理论定理", "统计总体", "用户授权"):
            self.assertIn(label, self.confirm)
        self.assertIn("封存holdout", self.confirm)

    def test_neighbor_coverage_is_decision_based_not_fake_number(self):
        self.assertIn("直接近邻原文覆盖的最小可信标准", self.search)
        self.assertIn("NEIGHBOR_UNVERIFIED", self.search)
        self.assertIn("PREFERRED_PROVISIONAL", self.search)
        self.assertIn("不相关原文", self.search)

    def test_paper_plan_depends_on_contribution_type(self):
        for label in ("规律/边界/测量 Claim", "系统/benchmark/部署能力 Claim",
                      "算法/方法 Claim", "不制作新的长期写作账本"):
            self.assertIn(label, self.writing)
        for label in ("对照文献覆盖按科学主张扩展", "QA 深度跟随作者实际任务",
                      "约30篇软目标、宁少勿假"):
            self.assertIn(label, self.qa)
        self.assertIn("宁少勿假", self.writing)

    def test_publication_readiness_requires_positive_scientific_case(self):
        for label in ("READER_STAKE", "INDEPENDENT_DELTA", "DECISIVE_EVIDENCE",
                      "STRONGEST_REVIEWER_OBJECTION", "同类型论文先例仅支持"):
            self.assertIn(label, self.q2)

    def test_agent_replay_is_unmeasured_not_ci_success(self):
        for label in ("BASELINE_NO_PDRW", "PDRW_CURRENT",
                      "PDRW_PREVIOUS", "NOT_REPLAYABLE", "NOT_MEASURED"):
            self.assertIn(label, self.replay)
        self.assertIn("CI 仅证明规则/程序行为", self.agents)


if __name__ == "__main__":
    unittest.main()
