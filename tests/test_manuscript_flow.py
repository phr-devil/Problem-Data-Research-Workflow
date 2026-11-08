"""Offline tests for structural Introduction diagnostics, not prose-quality scoring."""
import tempfile
import unittest
import zipfile
from pathlib import Path

from core.manuscript_flow import scan_file


class ManuscriptFlowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def paper(self, content, name="paper.md"):
        path = self.root / name
        path.write_text(content, encoding="utf-8")
        return scan_file(path)

    def test_continuous_prose_and_natural_paragraph_variability(self):
        result = self.paper(
            "# Paper\n\n## 1. Introduction\n\n"
            "Important problem requires explanation.\n\n"
            "Prior methods have unresolved constraints that make the present question meaningful and precise.\n\n"
            "This study tests the prediction under bounded conditions.\n\n"
            "## 2. Related Work\n\n- A list allowed outside introduction.\n")
        self.assertEqual(result["status"], "INTRO_NO_STRUCTURAL_FLAGS")
        self.assertEqual(result["intro_paragraph_count"], 3)
        self.assertEqual(len(set(result["intro_paragraph_word_counts"])), 3)
        self.assertEqual(result["findings"], [])

    def test_intro_subheadings_and_lists_flagged_but_not_rewritten(self):
        result = self.paper(
            "## 1. Introduction\n\n### 1.1 Background\n\nResearch context.\n\n"
            "### 1.2 Contributions\n\n1. First idea.\n2. Second idea.\n"
            "## 2. Related Work\n\n### 2.1 Baselines\n- Outside intro.\n")
        self.assertEqual(result["status"], "INTRO_FORMAT_REVIEW_REQUIRED")
        self.assertEqual([x["code"] for x in result["findings"]],
                         ["INTRO_SUBHEADING", "INTRO_SUBHEADING",
                          "INTRO_LIST_ITEM", "INTRO_LIST_ITEM"])

    def test_no_introduction_is_not_reported_as_pass(self):
        result = self.paper("## 3. Methods\n\nOnly methods.")
        self.assertEqual(result["status"], "INTRO_NOT_IDENTIFIED")
        self.assertFalse(result["intro_identified"])

    def test_never_flags_only_due_to_similar_paragraph_lengths(self):
        result = self.paper(
            "## Introduction\n\nFirst brief sentence.\n\n"
            "Third brief sentence.\n\nFourth brief sentence.\n\n"
            "## Methods\n\nAnother section.")
        self.assertEqual(result["status"], "INTRO_NO_STRUCTURAL_FLAGS")
        self.assertEqual(result["word_counts_are"],
                         "DESCRIPTIVE_ONLY_NOT_LENGTH_TARGETS")

    def test_plain_text_numbered_sections(self):
        result = self.paper(
            "1. Introduction\n\nIntroduction prose.\n\n"
            "1.1 Motivation\n\nMore prose.\n\n"
            "2. Methods\n\nOnly later materials.",
            "draft.txt")
        self.assertEqual(result["status"], "INTRO_FORMAT_REVIEW_REQUIRED")
        self.assertEqual(result["findings"][0]["code"], "INTRO_SUBHEADING")

    def test_word_style_subheading_and_numbered_list(self):
        ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        def p(text, style, numbered=False):
            prop = f'<w:pPr><w:pStyle w:val="{style}"/>' + (
                '<w:numPr><w:numId w:val="1"/></w:numPr>' if numbered else "") + '</w:pPr>'
            return f"<w:p>{prop}<w:r><w:t>{text}</w:t></w:r></w:p>"
        xml = (f'<w:document xmlns:w="{ns}"><w:body>' +
               p("1. Introduction", "Heading1") +
               p("Opening prose.", "Normal") +
               p("1.1 Background", "Heading2") +
               p("Bullet point.", "ListParagraph", True) +
               p("2. Methods", "Heading1") +
               p("Method text.", "Normal") +
               "</w:body></w:document>")
        filename = self.root / "draft.docx"
        with zipfile.ZipFile(filename, "w") as archive:
            archive.writestr("word/document.xml", xml.encode("utf-8"))
        result = scan_file(filename)
        self.assertEqual([x["code"] for x in result["findings"]],
                         ["INTRO_SUBHEADING", "INTRO_LIST_ITEM"])
        self.assertEqual(result["intro_paragraph_count"], 1)

    def test_unsupported_format_rejected(self):
        path = self.root / "fake.pdf"
        path.write_bytes(b"not a real PDF")
        with self.assertRaisesRegex(ValueError, "PDF"):
            scan_file(path)


class NarrativeWorkflowContracts(unittest.TestCase):
    """Cross-file policy regression, not evidence of actual LLM writing quality."""

    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]

    def read(self, name):
        return (self.root / name).read_text(encoding="utf-8")

    def test_new_empirical_blueprint_has_no_intro_subheadings(self):
        text = self.read("templates/PAPER_BLUEPRINT.md")
        introduction = text.split("## 1. Introduction\n", 1)[1].split("## 2. Related Work", 1)[0]
        self.assertNotIn("### ", introduction)
        self.assertNotIn("### 1.1", text)
        self.assertIn("SEC-INTRO-01", introduction)
        self.assertIn("SEC-INTRO-02", introduction)
        self.assertIn("连续英文段落", introduction)

    def test_conclusion_not_forced_into_single_subsection(self):
        text = self.read("templates/PAPER_BLUEPRINT.md")
        conclusion = text.split("## 6. Conclusion\n", 1)[1].split("## Planning Change Notes", 1)[0]
        self.assertNotIn("### ", conclusion)
        self.assertIn("SEC-CONCLUSION-01", conclusion)

    def test_writing_and_qa_both_cover_depth_and_intro(self):
        writing = self.read("MANUSCRIPT_WRITING.md")
        qa = self.read("MANUSCRIPT_QA.md")
        for word in ("连续引言", "核心创新", "不强制五段", "不强求所有贡献", "core.manuscript_flow"):
            self.assertIn(word, writing)
        for word in ("INTRO_SUBHEADING", "UNDERDEVELOPED", "OVEREXPANDED",
                     "REPETITIVE_TEMPLATE", "SUBSTANTIVE_EXPANSION", "core.manuscript_flow"):
            if word == "INTRO_SUBHEADING":
                self.assertIn(word, self.read("core/manuscript_flow.py"))
            else:
                self.assertIn(word, qa)

    def test_authorization_and_publisher_override_survive(self):
        for name in ("MANUSCRIPT_WRITING.md", "MANUSCRIPT_QA.md",
                     "DUAL_DOCUMENT_WORKFLOW.md", "WRITING_GATE.md"):
            self.assertIn("确认", self.read(name))
        self.assertIn("WRITING_LOCKED", self.read("WRITING_GATE.md"))
        self.assertIn("FIGURE_POLICY.md", self.read("MANUSCRIPT_WRITING.md"))
        self.assertIn("Heading 2", self.read("PAPER_WORD_STYLE.md"))
        self.assertIn("Introduction", self.read("PAPER_WORD_STYLE.md"))


if __name__ == "__main__":
    unittest.main()
