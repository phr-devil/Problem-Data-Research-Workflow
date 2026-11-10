"""Static checks for the single PD-RW Word review/manuscript style contract."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PaperWordStyleTests(unittest.TestCase):
    def test_style_table_zero_spacing_except_title(self):
        style = (ROOT / "PAPER_WORD_STYLE.md").read_text(encoding="utf-8")
        rows = {}
        for line in style.splitlines():
            if not line.startswith("| `"):
                continue
            cells = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(cells) == 7:
                rows[cells[0].strip("`")] = {
                    "font": cells[1], "before": cells[3],
                    "after": cells[4], "indent": cells[6]
                }
        expected = ("Title", "Heading 1", "Heading 2", "Heading 3",
                    "Normal", "Blueprint Meta", "Blueprint Note",
                    "Unnumbered Heading", "List Paragraph",
                    "Figure Caption", "Table Caption", "Table Text", "Equation", "Reference")
        self.assertEqual(set(rows), set(expected))
        for name in expected:
            with self.subTest(style=name):
                self.assertEqual((rows[name]["before"], rows[name]["after"]), ("0", "0"))
                self.assertIn("Times New Roman", rows[name]["font"])
                self.assertEqual(rows[name]["indent"], "0 / 0.5 in" if name == "Normal" else "0 / 0")

    def test_dimensions_and_heading_mapping(self):
        style = (ROOT / "PAPER_WORD_STYLE.md").read_text(encoding="utf-8")
        for s in ("A4", "2.5 cm", "Times New Roman",
                  "11 pt", "1.15 倍行距", "首行缩进 `0.5 in`",
                  "1.27 cm", "标题不设左缩进或首行缩进", "全部样式", "真实标题样式",
                  "3.2.1", "PAGE", "Fig. 1.", "Table 1.", "自动序号",
                  "不能只用默认的 Pandoc"):
            with self.subTest(marker=s):
                self.assertIn(s, style)

    def test_on_demand_writing_and_figure_gates(self):
        style = (ROOT / "PAPER_WORD_STYLE.md").read_text(encoding="utf-8")
        for s in ("WRITING_LOCKED", "不自动输出", "FIGURE_POLICY.md",
                  "投稿格式版本", "用户明确 Word 导出请求", "正式稿件须先通过",
                  "每个正文自然段", "不是添加空格或 Tab"):
            with self.subTest(marker=s):
                self.assertIn(s, style)
        for p in ("AGENTS.md", "WORKFLOW.md", "DUAL_DOCUMENT_WORKFLOW.md",
                  "WRITING_GATE.md", "templates/PAPER_BLUEPRINT.md"):
            with self.subTest(path=p):
                self.assertIn("PAPER_WORD_STYLE.md", (ROOT / p).read_text(encoding="utf-8"))

    def test_local_style_markdown_links(self):
        path = ROOT / "PAPER_WORD_STYLE.md"
        for dest in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if dest.startswith(("https:", "http:", "mailto:", "#")):
                continue
            self.assertTrue((path.parent / dest.split("#", 1)[0]).exists(), dest)


if __name__ == "__main__":
    unittest.main()
