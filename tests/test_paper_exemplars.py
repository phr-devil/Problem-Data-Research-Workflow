"""Static checks for the exemplar library; not a scientific quality certification."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "paper_exemplars"
IDS = tuple(f"EX{i:02d}" for i in range(1, 17))


class PaperExemplarTests(unittest.TestCase):
    def test_index_and_sixteen_fulltext_derived_cards(self):
        index = (DIR / "README.md").read_text(encoding="utf-8")
        cards = sorted((DIR / "cases").glob("*.md"))
        self.assertEqual(len(cards), 16)
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
        for ident in ("EX08", "EX09", "EX10", "EX11", "EX12", "EX13", "EX14", "EX15", "EX16"):
            self.assertIn(f"cases/{ident}_", route)
        self.assertIn("C05", route)
        self.assertIn("FULLTEXT_NOT_REVIEWED", route)
        self.assertIn("EX13–EX16", route)
        self.assertIn("不批准H3/H4/H5", route)
        self.assertNotIn("C01–C05", route)
        self.assertIn("不批准H3/H4/H5", route)

    def test_pdf_manifest_deduplicates_and_tracks_uploaded_fulltext(self):
        manifest = (DIR / "PDF_SOURCE_MANIFEST.md").read_text(encoding="utf-8")
        self.assertIn("10 份上传 PDF / 9 个不同 SHA-256", manifest)
        self.assertIn("不提交 PDF", manifest)
        for ident in ("EX08", "EX09", "EX10", "EX11", "EX12",
                      "EX13", "EX14", "EX15", "EX16"):
            self.assertIn(f"cases/{ident}_", manifest)
        rows = [line for line in manifest.splitlines() if line.startswith("| [EX")]
        self.assertEqual(len(rows), 10)
        self.assertEqual(len(set(row.split("`")[3] for row in rows)), 9)
        # The two uploaded conformal-PDF aliases share an exact content hash.
        conformal = [line for line in rows if "[EX12]" in line]
        self.assertEqual(len(conformal), 2)
        self.assertEqual(conformal[0].split("`")[3], conformal[1].split("`")[3])

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
