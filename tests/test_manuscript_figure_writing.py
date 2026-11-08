"""Offline writing-stage figure layout contract; no images or DOCX are generated."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ManuscriptFigureWritingContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.writing = (ROOT / "MANUSCRIPT_WRITING.md").read_text(encoding="utf-8")
        cls.word = (ROOT / "PAPER_WORD_STYLE.md").read_text(encoding="utf-8")
        cls.agent = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        cls.qa = (ROOT / "MANUSCRIPT_QA.md").read_text(encoding="utf-8")

    def test_rule_is_owned_by_writing_and_word_export(self):
        self.assertIn("正文生成阶段的图片位置与 Fig. 图题", self.writing)
        self.assertIn("正文生成阶段的图片位置与 Fig. 图题", self.agent)
        self.assertIn("全部正文文字", self.word)
        self.assertIn("References", self.writing)
        self.assertIn("References", self.word)
        self.assertIn("不属于 [MANUSCRIPT_QA.md]", self.writing)
        self.assertNotIn("正文生成阶段的图片位置与 Fig. 图题", self.qa)

    def test_figure_blocks_only_in_tail_and_no_implicit_drawing(self):
        for term in ("Figures", "图题紧随各自图片下方", "正文中间不嵌入图片",
                     "MISSING_FIGURE", "不会因为正文引用图号或写图题而自动绘图"):
            self.assertIn(term, self.writing)
        self.assertIn("图题紧跟对应图片下方", self.word)
        self.assertIn("FIGURE_POLICY.md", self.word)

    def test_exact_single_and_multi_panel_examples(self):
        self.assertIn("Fig.1 Main description.", self.writing)
        self.assertIn("Fig.1 Main description. (a) Description of panel a. (b) Description of panel b.", self.writing)
        self.assertIn("Fig.1 Overall description.", self.word)
        self.assertIn("Fig.1 Overall description. (a) Panel a description. (b) Panel b description.", self.word)
        single = "Fig.1 Overall description."
        multi = "Fig.1 Overall description. (a) Panel a description. (b) Panel b description."
        self.assertRegex(single, r"^Fig\.[1-9]\d* [^(]+\.$")
        self.assertRegex(multi, r"^Fig\.[1-9]\d* .+\. \(a\) .+\. \(b\) .+\.$")
        self.assertNotIn("(a)", single)
        self.assertNotIn("编号使用 `Fig. 1. ...`", self.word)
        self.assertIn("SEQ Figure", self.word)

    def test_no_structural_or_permission_expansion(self):
        self.assertIn("独立", (ROOT / "FIGURE_POLICY.md").read_text(encoding="utf-8"))
        self.assertIn("WRITING_LOCKED", (ROOT / "WRITING_GATE.md").read_text(encoding="utf-8"))
        self.assertIn("先向用户说明冲突", self.writing)
        self.assertIn("经用户确认", self.word)


if __name__ == "__main__":
    unittest.main()
