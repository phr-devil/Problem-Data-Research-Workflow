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
        "templates/STATE.md","WRITING_GATE.md","NEXT_ACTION_POLICY.md",
        "Q2_PUBLICATION_GOAL.md","POST_ALGORITHM_SCIENCE_AUDIT.md")

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

    def test_q2_goal_writing_and_handoff_contract(self):
        """Check operative semantics, not obsolete headings or labels."""
        checks = {
            "START.md": ["Q2_PUBLICATION_GOAL.md", "WRITING_GATE.md",
                         "NEXT_ACTION_POLICY.md"],
            "WORKFLOW.md": ["Q2_PUBLICATION_GOAL.md", "NEXT_ACTION_POLICY.md",
                            "WRITING_GATE.md"],
            "PAPER_FIRST.md": ["Q2_PUBLICATION_GOAL.md", "WRITING_GATE.md"],
            "VENUE_STRATEGY.md": ["Q2_POTENTIAL_SUPPORTED", "Q2_UNCERTAIN",
                                  "Q3/Q4"],
            "EXPERIMENT_LOOP.md": ["Q2", "EVIDENCE_COMPLETION_PRIORITY"],
            "CONFIRMATION.md": ["Q2_PUBLICATION_GOAL.md", "WRITING_GATE.md"],
            "NEXT_ACTION_POLICY.md": ["AGENT_DECIDABLE",
                                      "USER_DECISION_REQUIRED",
                                      "NEXT_AGENT_INSTRUCTION"],
            "Q2_PUBLICATION_GOAL.md": ["Q2_POTENTIAL_SUPPORTED",
                                       "Q2_UPGRADE_POSSIBLE",
                                       "Q2_UNCERTAIN",
                                       "BELOW_Q2_TARGET",
                                       "WRITING_LOCKED"],
        }
        for filename, markers in checks.items():
            content = (ROOT / filename).read_text(encoding="utf-8")
            for marker in markers:
                with self.subTest(file=filename, marker=marker):
                    self.assertIn(marker, content)
        decision = (ROOT / "NEXT_ACTION_POLICY.md").read_text(encoding="utf-8")
        self.assertIn("禁止预先输出Agent执行指令", decision)
        self.assertIn("真实授权", decision)

    def test_permissions_and_core_rules(self):
        workflow = (ROOT / "WORKFLOW.md").read_text(encoding="utf-8")
        start = (ROOT / "START.md").read_text(encoding="utf-8")
        for marker in ("STATE","Run","授权","训练"):
            self.assertIn(marker, workflow + start)
        self.assertIn("NOT_RUN", workflow + start)
        self.assertNotIn("../08_算法检验与优化", workflow + start)
