"""Static policy regression only: no Agent, network, training or manuscripts run."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


class ResearchToManuscriptContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.discovery = read("SEARCH_DISCOVERY.md")
        cls.algorithm = read("ALGORITHM_ENGINEERING.md")
        cls.harvest = read("SCIENCE_RESULT_HARVEST.md")
        cls.workflow = read("WORKFLOW.md")
        cls.blueprint = read("templates/PAPER_BLUEPRINT.md")
        cls.dual = read("DUAL_DOCUMENT_WORKFLOW.md")
        cls.paper = read("PAPER_FIRST.md")
        cls.writing = read("MANUSCRIPT_WRITING.md")
        cls.qa = read("MANUSCRIPT_QA.md")
        cls.agent = read("AGENTS.md")

    def test_science_problem_search_is_multi_source_and_permission_bounded(self):
        for term in ("实际需求/部署失败", "理论、物理或测量张力",
                     "已有合法 DEV 数据", "具名论文/方法之间的矛盾",
                     "不得为了选题自动下载", "COMPETING_CHOICE"):
            self.assertIn(term, self.discovery)
        self.assertIn("不新增", self.discovery)

    def test_algorithm_probes_competing_explanations_without_forcing_train(self):
        for term in ("COMPETING_EXPLANATIONS", "DISTINGUISHING_PROBE",
                     "强简单基线", "不以“尚不能证明机制”为由禁止"):
            self.assertIn(term, self.algorithm)
        self.assertIn("普通调参", self.algorithm)

    def test_claim_type_evidence_and_nonmetric_stop(self):
        for term in ("CAPABILITY/PERFORMANCE", "MECHANISM/CAUSAL",
                     "LAW/BOUNDARY", "ARTICULATION_GAP", "EVIDENCE_GAP"):
            self.assertIn(term, self.harvest)
        self.assertIn("科学机会型止损复核", self.workflow)
        self.assertIn("无限续投", self.workflow)
        self.assertIn("项目 STOP/PIVOT 仍归用户", self.workflow)

    def test_blueprint_thesis_is_revisable_not_a_causal_gate(self):
        for term in ("WORKING_THESIS", "不强制因果句式", "TENTATIVE/UNKNOWN"):
            self.assertIn(term, self.blueprint)
        for term in ("WORKING_THESIS", "允许修订/撤回", "不锁死第一版故事线"):
            self.assertIn(term, self.dual)
        self.assertIn("WRITING_GATE.md", self.blueprint)

    def test_journal_analogues_drive_only_relevant_evidence(self):
        self.assertIn("高水平期刊的科研设计反推", self.paper)
        self.assertIn("REQUIRED_DECISIVE_TEST", self.paper)
        self.assertIn("不机械移植", self.paper)

    def test_writing_builds_argument_chain_qa_finds_gaps(self):
        for term in ("IMPORTANT_QUESTION", "CLOSEST_PRIOR_LIMITATION",
                     "RESULTS_EVIDENCE", "INTERPRETATION+ALTERNATIVE"):
            self.assertIn(term, self.writing)
        for term in ("INTRODUCTION_QUESTION/GAP", "METHODS_DESIGN",
                     "RESULTS_EVIDENCE", "DISCUSSION_INTERPRETATION/ALTERNATIVE",
                     "INDEPENDENCE_NOT_MEASURED"):
            self.assertIn(term, self.qa)
        self.assertIn("不增加第六轮", self.qa)

    def test_about_thirty_references_is_soft_and_fabrication_forbidden(self):
        for term in ("约 30 篇", "不设最低数量", "宁少勿假",
                     "不得编造文献", "VERIFIED_REF_COUNT",
                     "不能在投稿可用的参考文献表中混入占位项"):
            self.assertIn(term, self.writing)
        self.assertIn("篇数少不等于审核 FAIL", self.qa)
        self.assertIn("绝不为补数量生成不存在或无关文献", self.qa)
        self.assertIn("支持该 Claim", self.writing)
        # No ungrounded reference-count pass/fail in canonical article policy.
        self.assertNotIn("至少30篇", self.writing)
        self.assertNotIn("必须达到30篇", self.qa)
        self.assertIn("WRITING_LOCKED", read("WRITING_GATE.md"))
        self.assertIn("图题格式精确固定", self.writing)

    def test_single_entry_and_existing_gate_are_preserved(self):
        self.assertIn("WORKFLOW.md", self.agent)
        self.assertIn("MANUSCRIPT_WRITING.md", self.agent)
        self.assertIn("MANUSCRIPT_QA.md", self.agent)
        self.assertIn("HIGH_VALUE_RESEARCH_DESIGN.md", self.workflow)
        self.assertIn("CONFIRMATION", self.workflow)
        self.assertIn("WRITING_LOCKED", self.workflow)


if __name__ == "__main__":
    unittest.main()
