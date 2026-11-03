"""Standalone PD-RW offline contract checks. No training or network."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ("AGENTS.md","START.md","WORKFLOW.md","README.md","DATA_DISCOVERY.md",
        "SEARCH_DISCOVERY.md","DATA_INSIGHT.md","TASK_EXPLORATION.md","TASK_LADDER.md",
        "EXPERIMENT_LOOP.md","IMPLEMENTATION_GUIDE.md","ALGORITHM_ENGINEERING.md","PAPER_FIRST.md",
        "CONFIRMATION.md","VENUE_STRATEGY.md","REPLAY_PROTOCOL.md","REFERENCES.md","EXAMPLE_SENSOR.md",
        "templates/STATE.md")

class WorkflowContracts(unittest.TestCase):
    def test_required_files(self):
        for file in DOCS + ("SCENARIOS.json","chapter10_replay.py"):
            self.assertTrue((ROOT / file).is_file(), file)

    def test_local_markdown_links(self):
        for name in DOCS:
            path = ROOT / name
            for dest in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if dest.startswith(("http:","https:","mailto:","#")):
                    continue
                relative = dest.split("#", 1)[0]
                self.assertTrue((path.parent / relative).exists(), f"{name} -> {dest}")

    def test_scenarios_have_unique_ids_and_contract(self):
        suite = json.loads((ROOT / "SCENARIOS.json").read_text(encoding="utf-8"))
        cases = suite["cases"]
        self.assertGreaterEqual(len(cases), 50)
        ids = [c["id"] for c in cases]
        self.assertEqual(len(ids), len(set(ids)))
        for case in cases:
            self.assertTrue(all(k in case for k in ("id","event","situation","should","must_not")))

    def test_algorithm_decision_scenarios_are_preserved(self):
        cases = {x["id"]: x for x in json.loads((ROOT / "SCENARIOS.json").read_text(encoding="utf-8"))["cases"]}
        for cid, expected_scope in (("D10-58", "MECHANISM"), ("D10-59", "EVIDENCE"), ("D10-60", "RUN")):
            with self.subTest(case=cid):
                self.assertEqual(cases[cid]["expected_route"], "ALGORITHM_ENGINEERING.md")
                self.assertEqual(cases[cid]["decision_scope"], expected_scope)
                self.assertTrue(cases[cid]["should"] and cases[cid]["must_not"])

    def test_algorithm_engineering_contract(self):
        guide = (ROOT / "ALGORITHM_ENGINEERING.md").read_text(encoding="utf-8")
        for marker in ("REPAIR_EVALUATION", "SIMPLE_IMPROVEMENT", "MECHANISM_CANDIDATE",
                       "PAPER_EVIDENCE", "LEGAL_LEVER", "Champion", "逐样本预测", "NOT_RUN"):
            with self.subTest(marker=marker):
                self.assertIn(marker, guide)
        for filename in ("START.md", "AGENTS.md", "WORKFLOW.md",
                         "EXPERIMENT_LOOP.md", "IMPLEMENTATION_GUIDE.md", "README.md"):
            with self.subTest(link=filename):
                self.assertIn("ALGORITHM_ENGINEERING.md",
                              (ROOT / filename).read_text(encoding="utf-8"))

    def test_publication_first_contract(self):
        files = {
            "START.md": ["论文优先触发", "PAPER_FIRST.md"],
            "WORKFLOW.md": ["PAPER_COMPLETION_REVIEW", "PAPER_COMPLETION_PRIORITY"],
            "PAPER_FIRST.md": ["最小可投稿论文路线", "最小论文成稿合同"],
            "VENUE_STRATEGY.md": ["提前进行轻量论文参照", "以稿件完成难度决定下一步"],
            "EXPERIMENT_LOOP.md": ["论文完成列为优先实验目标"],
            "CONFIRMATION.md": ["最小完整稿件检查"],
        }
        for filename, markers in files.items():
            content = (ROOT / filename).read_text(encoding="utf-8")
            for marker in markers:
                with self.subTest(file=filename, marker=marker):
                    self.assertIn(marker, content)

    def test_permissions_and_core_rules(self):
        workflow = (ROOT / "WORKFLOW.md").read_text(encoding="utf-8")
        start = (ROOT / "START.md").read_text(encoding="utf-8")
        for marker in ("STATE","Run","授权","训练"):
            self.assertIn(marker, workflow + start)
        self.assertIn("NOT_RUN", workflow + start)
        self.assertNotIn("../08_算法检验与优化", workflow + start)
