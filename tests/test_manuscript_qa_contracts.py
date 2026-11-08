"""Static/fixture-level QA contract tests. No LLM, network, data, or manuscript is run."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evals" / "manuscript_qa_cases.json"


class ManuscriptQAContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qa = (ROOT / "MANUSCRIPT_QA.md").read_text(encoding="utf-8")
        cls.entry = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        cls.paper_index = (ROOT / "modules/paper/README.md").read_text(encoding="utf-8")
        cls.writing = (ROOT / "MANUSCRIPT_WRITING.md").read_text(encoding="utf-8")
        cls.data = json.loads(FIXTURES.read_text(encoding="utf-8"))

    def test_one_authoritative_route_and_handoff(self):
        self.assertIn("[MANUSCRIPT_QA.md](MANUSCRIPT_QA.md)", self.entry)
        self.assertIn("[MANUSCRIPT_QA.md](../../MANUSCRIPT_QA.md)", self.paper_index)
        self.assertIn("[MANUSCRIPT_QA.md](MANUSCRIPT_QA.md)", self.writing)
        self.assertIn("WRITING_GATE.md", self.qa)
        self.assertIn("PAPER_WORD_STYLE.md", self.qa)

    def test_five_rounds_ten_domains_three_gates(self):
        for n in range(1, 11):
            self.assertIn(f"| Q{n} |", self.qa)
        for n in range(1, 6):
            self.assertIn(f"| R{n} ", self.qa)
        for gate in ("G1 科学有效性", "G2 语义回归", "G3 投稿与交付"):
            self.assertIn(gate, self.qa)

    def test_permissions_and_reporting_are_explicit(self):
        for label in ("SEALED", "SOURCE_UNVERIFIED", "USER_DECISION",
                      "NOT_MEASURED", "RENDER_NOT_VERIFIED",
                      "OVERCLAIM", "UNDERCLAIM", "MANUSCRIPT_QA_REPORT.md"):
            self.assertIn(label, self.qa)
        self.assertIn("不将 AI 检测器数值当事实", self.qa)
        self.assertIn("修改只在用户明确要求修改时进行", self.qa)

    def test_fixture_integrity_and_adversarial_coverage(self):
        self.assertEqual(self.data["format"], "pdrw-manuscript-qa-cases-v1")
        self.assertEqual(self.data["scope"], "REGRESSION_ONLY")
        cases = self.data["cases"]
        self.assertGreaterEqual(len(cases), 10)
        self.assertEqual(len({x["id"] for x in cases}), len(cases))
        self.assertEqual({x["domain"] for x in cases}, {f"Q{n}" for n in range(1, 11)})
        for c in cases:
            self.assertTrue(c["manuscript"] and c["context"] and c["must_not"])
            self.assertIn(c["expected_severity"], {"BLOCKER", "MAJOR", "MINOR", "STYLE"})
            self.assertTrue(c["expected_action"])
        actions = {c["expected_action"] for c in cases}
        self.assertTrue({"NARROW_TO_DEV", "REVERT_SEMANTIC_DRIFT", "PRESERVE_VISION",
                         "REQUEST_STRUCTURE_CONFIRMATION", "REPORT_NOT_MEASURED",
                         "FLAG_MISSING_PANEL_NO_DRAW", "RENDER_NOT_VERIFIED"} <= actions)


if __name__ == "__main__":
    unittest.main()
