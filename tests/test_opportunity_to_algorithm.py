"""Offline structure and synthetic opportunity-to-algorithm policy regression.

No Agent, network, scientific execution, download, model fit or SEALED reading.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "evals/cases/opportunity_to_algorithm.json"
ROUTES = {"BOTTLENECK", "CONTRADICTION", "FAILURE_BOUNDARY",
          "DATA_EVALUATION", "CROSS_DOMAIN", "ANOMALY_NEGATIVE"}
CONTRIBUTIONS = {"BREAKTHROUGH", "PERFORMANCE", "DISCOVERY",
                 "INFRASTRUCTURE", "CORRECTION"}


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


class OpportunityToAlgorithmTests(unittest.TestCase):
    def test_case_catalog_covers_distinct_sources_and_contributions(self):
        packet = json.loads(DATA.read_text(encoding="utf-8"))
        self.assertEqual(packet["format"], "pd-rw-opportunity-to-algorithm-synthetic-v1")
        self.assertEqual(set(packet["source_routes"]), ROUTES)
        self.assertEqual(set(packet["contribution_routes"]), CONTRIBUTIONS)
        cases = packet["cases"]
        self.assertEqual(len({c["id"] for c in cases}), len(cases))
        self.assertTrue(ROUTES.issubset({c["source_route"] for c in cases}))
        self.assertTrue(CONTRIBUTIONS.issubset({c["contribution_route"] for c in cases}))
        for case in cases:
            with self.subTest(id=case["id"]):
                self.assertEqual(case["origin"], "SYNTHETIC")
                self.assertGreater(len(case["context"]), 20)
                self.assertGreater(len(case["preferred_action"]), 20)
                self.assertTrue(case["must_notice"])
                self.assertIn("NO_SEALED", case["authorization"])
                self.assertIn("NO_FIT", case["authorization"])

    def test_existing_owner_documents_contain_operational_rules(self):
        requirements = {
            "SEARCH_DISCOVERY.md": (
                "六类线索的可执行检索动作", "DISCOVERY_SOURCE", "DECISIVE_FALSIFIER",
                "NEIGHBOR_UNVERIFIED"),
            "HIGH_VALUE_RESEARCH_DESIGN.md": (
                "五种高水平贡献路线", "重大创新型", "性能突破型",
                "科学发现型", "基础设施型", "认知纠正型"),
            "DATA_INSIGHT.md": ("失败条件矩阵", "INDEPENDENT_GROUP_N", "PERFORMANCE_UNKNOWN"),
            "TASK_EXPLORATION.md": ("FALSIFIER", "MINIMUM_DISCRIMINATING_TEST"),
            "ALGORITHM_ENGINEERING.md": ("MISSING_ALGORITHMIC_CAPABILITY",
                "WHY_SIMPLE_BASELINE_FAILS", "DISTINCT_PREDICTION"),
            "EXPERIMENT_LOOP.md": ("SIMPLE_FIX", "INCONCLUSIVE", "SEALED"),
            "PAPER_FIRST.md": ("五类论文竞争力路线", "CLAIM_EVIDENCE_MAP"),
            "VENUE_STRATEGY.md": ("已发表论文成功机制对照", "READER_STAKE"),
        }
        for path, markers in requirements.items():
            doc = read(path)
            for marker in markers:
                with self.subTest(path=path, marker=marker):
                    self.assertIn(marker, doc)

    def test_no_new_permissions_states_or_parallel_logs(self):
        workflow = read("WORKFLOW.md")
        self.assertIn("三个决策循环（六项活动", workflow)
        self.assertIn("不新增 Claim 状态或阶段", workflow)
        self.assertIn("WRITING_LOCKED", workflow)
        self.assertIn("CONFIRMATION.md", workflow)
        self.assertIn("按需", read("SEARCH_DISCOVERY.md"))
        self.assertIn("不新增第三份科研日志", read("SCIENCE_RESULT_HARVEST.md"))
        self.assertIn("DATA_ACQUIRED_VERIFIED", read("DATA_INSIGHT.md"))
        self.assertIn("NEXT_ACTION_POLICY.md", read("AGENTS.md"))


if __name__ == "__main__":
    unittest.main()
