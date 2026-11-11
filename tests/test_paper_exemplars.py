"""Static checks for the exemplar library; not a scientific quality certification."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "paper_exemplars"
IDS = tuple(f"EX{i:02d}" for i in range(1, 13))


class PaperExemplarTests(unittest.TestCase):
    def test_index_and_twelve_fulltext_derived_cards(self):
        index = (DIR / "README.md").read_text(encoding="utf-8")
        cards = sorted((DIR / "cases").glob("*.md"))
        self.assertEqual(len(cards), 12)
        for ident in IDS:
            with self.subTest(case=ident):
                self.assertEqual(len([p for p in cards if p.name.startswith(ident + "_")]), 1)
                paper = next(p for p in cards if p.name.startswith(ident + "_"))
                self.assertIn("cases/" + paper.name, index)
                content = paper.read_text(encoding="utf-8")
                self.assertTrue(content.startswith("# " + ident))
                for marker in ("**Source:**", "**Status:**", "**Locators:**", "可迁移策略", "AVOID"):
                    self.assertIn(marker, content)
        self.assertIn("EXEMPLAR_NONE", index)
        self.assertIn("1–3篇", index)
        self.assertIn("预印本", index)

    def test_six_problem_sources_and_five_contribution_routes_in_separate_map(self):
        route = (DIR / "RESEARCH_OPPORTUNITY_MAP.md").read_text(encoding="utf-8")
        source = (ROOT / "contracts/human_review_protocol.v1.json").read_text(encoding="utf-8")
        import json
        contract = json.loads(source)
        for key in contract["vocabularies"]["question_sources"]:
            self.assertIn(key, route)
        for key in contract["vocabularies"]["contribution_routes"]:
            self.assertIn(key, route)
        for ident in ("EX08", "EX09", "EX10", "EX11", "EX12"):
            self.assertIn(f"cases/{ident}_", route)
        for identifier in ("C01", "C02", "C03", "C04", "C05"):
            self.assertIn(identifier, route)
        self.assertIn("未在本次生成全文策略卡", route)
        self.assertIn("不批准H3/H4/H5", route)

    def test_no_pdf_redistribution(self):
        self.assertFalse(list(DIR.rglob("*.pdf")))
        self.assertFalse(list(DIR.rglob("*.png")))

    def test_connected_to_writing_routing(self):
        for path in ("MANUSCRIPT_WRITING.md", "AGENTS.md", "modules/paper/README.md", "README.md"):
            with self.subTest(path=path):
                self.assertIn("paper_exemplars/README.md", (ROOT / path).read_text(encoding="utf-8"))
        flow = (ROOT / "MANUSCRIPT_WRITING.md").read_text(encoding="utf-8")
        self.assertIn("EXEMPLAR_IDS", flow)
        self.assertIn("R1 证据与论证", flow)
        self.assertIn("WRITING_GATE.md", flow)


if __name__ == "__main__":
    unittest.main()
