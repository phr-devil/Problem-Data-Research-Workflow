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

    def test_optional_check_documented_without_new_gate(self):
        guide = (ROOT / "DUAL_DOCUMENT_WORKFLOW.md").read_text(encoding="utf-8")
        self.assertIn("python -m core.doc_integrity --project PROJECT_DIR", guide)
        self.assertIn("不新增审批", guide)
        self.assertIn("不是科学真实性", guide)

    def test_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                check_project(Path(temp), "../other.md")
            with self.assertRaises(ValueError):
                check_project(Path(temp), "/tmp/other.md")


    def test_material_events_need_traceable_blueprint_check(self):
        pap = "# Paper\n## 4. Experiments\n### 4.1 Results\n- SEC_ID: SEC-RESULT-01\n"
        for kind in ("DIRECTION_SET", "IMPORTANT_RUN", "NEGATIVE_RESULT",
                     "CLAIM_CHANGE", "ROUTE_CHANGE", "HANDOFF"):
            with self.subTest(kind=kind):
                rec = "# Record\n## 0. Now\n## 5. History\n### EXP-2｜event\n- EVENT_KIND: " + kind
                codes = {v["code"] for v in inspect_text(rec, pap)}
                for code in ("BLUEPRINT_CHECK_MISSING_OR_INVALID",
                             "BLUEPRINT_AFFECTED_SECTIONS_MISSING",
                             "BLUEPRINT_EVIDENCE_MISSING", "BLUEPRINT_REASON_MISSING"):
                    self.assertIn(code, codes)

    def test_update_and_no_change_in_events(self):
        pap = "# Paper\n## 4. Experiments\n### 4.1 Results\n- SEC_ID: SEC-RESULT-01\n"
        for status, sec in (("UPDATED", "SEC-RESULT-01"),
                            ("NO_CHANGE_NEEDED", "NONE"),
                            ("NO_CHANGE_NEEDED", "SEC-RESULT-01")):
            with self.subTest(status=status, sec=sec):
                rec = ("# Record\n## 0. Now\n## 5. History\n### EXP-2｜event\n"
                       "- EVENT_KIND: NEGATIVE_RESULT\n"
                       f"- BLUEPRINT_CHECK: {status}\n- BLUEPRINT_SECTIONS: {sec}\n"
                       "- BLUEPRINT_EVIDENCE: results/run-2.json#table3\n"
                       "- BLUEPRINT_REASON: This result is already handled in the existing plan.\n")
                self.assertFalse([v for v in inspect_text(rec, pap) if v["level"] == "ERROR"])

    def test_routine_and_legacy_events_do_not_trigger(self):
        for meta in ("- EVENT_KIND: ROUTINE", "- outcome: unchanged"):
            rec = "# Record\n## 0. Now\n## 5. History\n### EXP-2｜debug\n" + meta
            self.assertNotIn("BLUEPRINT_CHECK_MISSING_OR_INVALID",
                             {v["code"] for v in inspect_text(rec, None)})

    def test_missing_blueprint_and_invalid_section(self):
        rec = ("# Record\n## 0. Now\n## 5. History\n### EXP-2｜event\n"
               "- EVENT_KIND: DIRECTION_SET\n- BLUEPRINT_CHECK: UPDATED\n"
               "- BLUEPRINT_SECTIONS: SEC-MISSING\n- BLUEPRINT_EVIDENCE: UNKNOWN\n"
               "- BLUEPRINT_REASON: Material change requires an identified section.\n")
        pap = "# Paper\n## 3. Method\n### 3.1 Task\n- SEC_ID: SEC-METHOD-01\n"
        self.assertIn("BLUEPRINT_AFFECTED_SECTION_UNKNOWN",
                      {v["code"] for v in inspect_text(rec, pap)})
        self.assertIn("BLUEPRINT_EVIDENCE_MISSING",
                      {v["code"] for v in inspect_text(rec, pap)})
        self.assertIn("BLUEPRINT_REQUIRED_FOR_EVENT",
                      {v["code"] for v in inspect_text(rec, None)})

    def test_default_chapters_and_missing_claim_source(self):
        pap = ("# PAPER_BLUEPRINT\n## Claim–Evidence–Section Index\n"
               "| Claim ID | Section ID | Evidence | Status |\n"
               "| --- | --- | --- | --- |\n"
               "| C01 | SEC-NOT-PRESENT | NOT_RUN | SUPPORTED |\n"
               "## 1. Introduction\n### 1.1 Invalid\n- SEC_ID: SEC-INTRO-01\n")
        codes = {v["code"] for v in inspect_text(None, pap)}
        for code in ("BLUEPRINT_SIX_CHAPTER_DEVIATION",
                     "BLUEPRINT_INTRO_CONCLUSION_SUBSECTION",
                     "CLAIM_SECTION_MAPPING_UNKNOWN", "SUPPORTED_CLAIM_WITHOUT_EVIDENCE"):
            self.assertIn(code, codes)


if __name__ == "__main__":
    unittest.main()
