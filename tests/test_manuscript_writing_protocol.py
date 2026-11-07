"""Regression checks for the manuscript execution contract (policy-only, not scientific QA)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


class ManuscriptWritingProtocolTests(unittest.TestCase):
    def test_authority_routes_and_existing_lock_preserved(self):
        for path in ("AGENTS.md", "WRITING_GATE.md", "DUAL_DOCUMENT_WORKFLOW.md",
                     "modules/paper/README.md", "README.md", "docs/STRUCTURE.md"):
            with self.subTest(path=path):
                self.assertIn("MANUSCRIPT_WRITING.md", read(path))
        gate = read("WRITING_GATE.md")
        self.assertIn("用户审查", gate)
        self.assertIn("独立的明确写作授权", gate)
        self.assertIn("WRITING_LOCKED", gate)
        self.assertIn("不得为写作锁停止", gate)

    def test_modules_rounds_and_no_new_gates(self):
        text = read("MANUSCRIPT_WRITING.md")
        for marker in ("M1 Evidence Contract", "M2 Argument Architecture",
                       "M3 Evidence-to-Prose", "M4 Source & Placeholder",
                       "M5 Scientific Audit", "M6 Prose & Delivery",
                       "R1 证据与论证", "R2 核心正文",
                       "R3 其余正文", "R4 科学与文字闭环",
                       "不额外要求四次用户确认", "独立明确正文写作授权"):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_scientific_integrity_and_scope(self):
        text = read("MANUSCRIPT_WRITING.md")
        for marker in ("SOURCE_CONFLICT", "denominator", "independent_unit",
                       "confirmatory/descriptive/exploratory", "Method ↔ Result",
                       "SOURCE_UNVERIFIED", "BLOCKER", "SEALED/CONFIRMATION",
                       "六章", "科学正确性 > 推理逻辑"):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_placeholders_and_single_source(self):
        text = read("MANUSCRIPT_WRITING.md")
        for marker in ("MANUSCRIPT_TEXT.md", "MANUSCRIPT_OPEN_ITEMS.md",
                       "[REF:R01", "[EQ:E01", "[FIG:F01",
                       "不使用虚构 [1]/DOI", "精修后再次核查"):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
