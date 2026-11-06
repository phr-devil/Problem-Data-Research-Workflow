"""Synthetic regression tests for optional read-only project-document integrity."""
import tempfile
import unittest
from pathlib import Path
from core.doc_integrity import inspect_text, check_project, main

ROOT = Path(__file__).resolve().parents[1]


class DocIntegrityTests(unittest.TestCase):
    def test_current_templates_have_no_errors(self):
        rec = (ROOT / "templates/RESEARCH_RECORD.md").read_text(encoding="utf-8")
        pap = (ROOT / "templates/PAPER_BLUEPRINT.md").read_text(encoding="utf-8")
        self.assertEqual([x for x in inspect_text(rec, pap) if x["level"] == "ERROR"], [])

    def test_missing_docs_do_not_break_legacy_projects(self):
        self.assertFalse(any(x["level"] == "ERROR" for x in inspect_text(None, None)))

    def test_duplicate_event_and_section_ids(self):
        rec = "# Record\n## 0. Now\n## 5. History\n### EXP-1｜X\n### EXP-1｜Y"
        pap = "# Paper\n## 1. Intro\n### 1.1 A\n- SEC_ID: SEC-A\n### 1.2 B\n- SEC_ID: SEC-A\n"
        codes = {x["code"] for x in inspect_text(rec, pap)}
        self.assertIn("DUPLICATE_EXP_ID", codes)
        self.assertIn("DUPLICATE_SEC_ID", codes)

    def test_wrong_parent_and_missing_section_id(self):
        codes = {x["code"] for x in inspect_text(None, "# Paper\n## 1. Intro\n### 2.1 Wrong")}
        self.assertIn("SUBSECTION_PARENT_MISMATCH", codes)
        self.assertIn("SECTION_WITHOUT_ID", codes)

    def test_unresolved_exp_is_warning_not_false_scientific_failure(self):
        rec = "# Record\n## 0. Now\n## 5. History\n### EXP-1｜Valid"
        pap = "# Paper\n## 1. Intro\n### 1.1 Gap\n- SEC_ID: SEC-GAP\n- ref: EXP-9\n"
        findings = inspect_text(rec, pap)
        self.assertIn("EXP_NOT_IN_RECORD", {x["code"] for x in findings})
        self.assertFalse(any(x["level"] == "ERROR" for x in findings))

    def test_code_fences_are_not_document_headings(self):
        pap = ("# Paper\n~~~markdown\n# Fake\n### 2.1 Fake\n"
               "~~~\n## 1. Intro\n### 1.1 Valid\n- SEC_ID: SEC-REAL\n")
        self.assertFalse(any(x["level"] == "ERROR" for x in inspect_text(None, pap)))

    def test_cli_does_not_write_or_create_missing_docs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(main(["--project", str(root)]), 0)
            self.assertEqual(list(root.iterdir()), [])
            (root / "RESEARCH_RECORD.md").write_text(
                "# Record\n## 0. Now\n## 5. History\n", encoding="utf-8")
            (root / "PAPER_BLUEPRINT.md").write_text(
                "# Paper\n## 1. Intro\n### 1.1 A\n- SEC_ID: SEC-A\n",
                encoding="utf-8")
            self.assertEqual(main(["--project", str(root), "--json"]), 0)
            self.assertEqual(len(list(root.iterdir())), 2)

    def test_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                check_project(Path(temp), "../other.md")
            with self.assertRaises(ValueError):
                check_project(Path(temp), "/tmp/other.md")


if __name__ == "__main__":
    unittest.main()
