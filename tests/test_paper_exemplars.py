"""Static checks for the exemplar library; not a scientific quality certification."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "paper_exemplars"
IDS = ("EX01", "EX02", "EX03", "EX04", "EX05", "EX06", "EX07")


class PaperExemplarTests(unittest.TestCase):
    def test_index_and_seven_fulltext_derived_cards(self):
        index = (DIR / "README.md").read_text(encoding="utf-8")
        cards = sorted((DIR / "cases").glob("*.md"))
        self.assertEqual(len(cards), 7)
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
