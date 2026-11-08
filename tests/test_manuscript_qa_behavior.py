"""Deterministic manuscript QA behavior tests; no Internet or real manuscripts."""
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from core.manuscript_style import scan_paragraphs, scan_file, compare_reports
from core.literature import verify_reference_metadata
from core.reference_audit import audit_batch


def fake_doi_fetch(url):
    if "crossref" not in url:
        raise ValueError("unreachable datacite")
    return {"message": {"DOI": "10.1234/test.2026", "title": ["Reliable Sensor Fusion"],
            "published": {"date-parts": [[2026, 10, 1]]},
            "author": [{"given": "Alice", "family": "Zhang"}],
            "container-title": ["Journal of Sensor Research"], "volume": "11",
            "issue": "2", "page": "12-24"}}


GOOD_REF = {"ref_id": "R1", "doi": "https://doi.org/10.1234/test.2026",
            "title": "Reliable Sensor Fusion", "year": 2026,
            "first_author": "Zhang", "container_title": "Journal of Sensor Research",
            "volume": "11", "issue": "2", "pages": "12-24"}


class ManuscriptStyleBehavior(unittest.TestCase):
    def test_detect_and_locate_style_issue(self):
        result = scan_paragraphs(["The proposed approach may potentially improve performance. "
                                  "It is worth noting that the method holds great promise.",
                                  "References", "[1] Placeholder."])
        self.assertGreater(result["style_flagged_word_coverage_percent"], 0)
        self.assertEqual(len(result["flagged_sentences"]), 2)
        self.assertEqual(result["flagged_sentences"][0]["paragraph"], 1)
        self.assertIsNone(result["external_ai_rate"])

    def test_compare_after_fix_and_non_ai_prose(self):
        old = scan_paragraphs(["Our approach may potentially improve accuracy."])
        new = scan_paragraphs(["Accuracy increased from 0.70 to 0.74 on the stated validation set."])
        self.assertLess(new["style_flagged_word_coverage_percent"],
                        old["style_flagged_word_coverage_percent"])
        change = compare_reports(old, new)
        self.assertLess(change["change_percentage_points"], 0)
        self.assertIn("separate review", change["note"])

    def test_repeated_openers_and_legitimate_single_use(self):
        result = scan_paragraphs(["Moreover, the sensor is calibrated.",
                                  "Moreover, the protocol is frozen.",
                                  "Moreover, the final evaluation is reserved."])
        self.assertEqual(len(result["flagged_sentences"]), 3)
        self.assertTrue(all("REPEATED_TRANSITION" in v["flags"] for v in result["flagged_sentences"]))
        single = scan_paragraphs(["Moreover, the protocol is frozen."])
        self.assertEqual(single["style_flagged_word_coverage_percent"], 0)

    def test_docx_extraction_with_stdlib(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "manuscript.docx"
            xml = ('<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                   '<w:body><w:p><w:r><w:t>It can be seen that this is repetitive.</w:t></w:r></w:p>'
                   '</w:body></w:document>')
            with zipfile.ZipFile(file, "w") as archive:
                archive.writestr("word/document.xml", xml)
            result = scan_file(file)
            self.assertEqual(len(result["flagged_sentences"]), 1)

    def test_reject_pdf_as_scan_source(self):
        with self.assertRaisesRegex(ValueError, "PDF"):
            scan_file("unread.pdf")


class ReferenceMetadataBehavior(unittest.TestCase):
    def test_matching_reference_is_not_full_text_certification(self):
        record = verify_reference_metadata(GOOD_REF, fetch=fake_doi_fetch)
        self.assertEqual(record["status"], "METADATA_MATCH")
        self.assertEqual(record["source_claim_support"], "NOT_CHECKED")
        self.assertEqual(record["publication_status"], "CHECK_OFFICIAL_PUBLISHER")
        self.assertEqual(record["checks"]["pages"], "MATCH")

    def test_real_doi_wrong_title_is_mismatch(self):
        ref = dict(GOOD_REF, title="Entirely different paper")
        record = verify_reference_metadata(ref, fetch=fake_doi_fetch)
        self.assertEqual(record["status"], "METADATA_MISMATCH")
        self.assertEqual(record["checks"]["title"], "MISMATCH")

    def test_missing_or_invalid_doi_is_not_fabricated(self):
        record = verify_reference_metadata({"title": "Some real non-DOI book"},
                                           fetch=fake_doi_fetch)
        self.assertEqual(record["status"], "NO_VALID_DOI_MANUAL_CHECK")

    def test_source_failure_is_not_inferred_not_found(self):
        def fail(_):
            raise ValueError("offline")
        record = verify_reference_metadata(GOOD_REF, fetch=fail)
        self.assertEqual(record["status"], "METADATA_UNAVAILABLE")

    def test_datacite_fallback_and_partial_fields(self):
        def datacite_fetch(url):
            if "crossref" in url:
                raise ValueError("not registered at Crossref")
            return {"data": {"attributes": {
                "doi": "10.1234/test.2026",
                "titles": [{"title": "Reliable Sensor Fusion"}],
                "creators": [{"familyName": "Zhang", "givenName": "Alice"}],
                "publicationYear": 2026,
            }}}
        expected = {k: GOOD_REF[k] for k in ("doi", "title", "year", "first_author")}
        record = verify_reference_metadata(expected, fetch=datacite_fetch)
        self.assertEqual(record["provider"], "datacite")
        self.assertEqual(record["status"], "METADATA_MATCH")
        # If the bibliography includes fields absent from the provider,
        # the correct result is partial verification, not a silent pass.
        detailed = verify_reference_metadata(GOOD_REF, fetch=datacite_fetch)
        self.assertEqual(detailed["status"], "METADATA_PARTIAL")
        self.assertEqual(detailed["checks"]["volume"], "METADATA_MISSING")

    def test_reference_set_count_and_duplicate(self):
        incomplete = audit_batch({"expected_count": 3, "references": [GOOD_REF]},
                                 fetch=fake_doi_fetch)
        self.assertEqual(incomplete["status"], "REFERENCE_SET_INCOMPLETE")
        full = audit_batch({"expected_count": 2, "references": [GOOD_REF, GOOD_REF]},
                           fetch=fake_doi_fetch)
        self.assertEqual(full["status"], "DOI_METADATA_AUDITED_NOT_CLAIMS")
        self.assertTrue(full["references"][1]["duplicate_doi"])
        self.assertEqual(full["extracted_count"], 2)


if __name__ == "__main__":
    unittest.main()
