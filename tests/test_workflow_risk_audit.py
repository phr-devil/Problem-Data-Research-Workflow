"""Focused negative regressions for evidence interpretation and provenance.

These are offline synthetic tests: not scientific validation or genuine agent evaluation.
"""
import unittest
from copy import deepcopy

from core.comparison import compare_runs
from core.contracts import ContractError, validate_run
from core.figure_change_scope import advise
from core.reference_audit import audit_batch


def run(run_id="a", metric=0.60):
    return {
        "run_id": run_id, "task_id": "T", "protocol_id": "P",
        "dataset_version": "D", "evaluator_version": "E",
        "group_split": "subjects_v1", "sample_ids_hash": "sample_hash",
        "legal_inputs": ["sensor"], "split": "dev", "status": "VALID",
        "metrics": {"error": metric},
        "artifact_refs": {"metrics": "metrics.json", "predictions": "pred.csv",
                          "code": "code.py"}, "budget_basis": "same_budget",
    }


def ref_fetch(url):
    return {"message": {"DOI": "10.1234/example", "title": ["Example Study"],
                        "published": {"date-parts": [[2026]]},
                        "author": [{"family": "Li"}]}}


GOOD_REF = {"ref_id": "R1", "doi": "10.1234/example",
            "title": "Example Study", "year": 2026, "first_author": "Li"}


class DirectionReviewTests(unittest.TestCase):
    def test_unspecified_direction_never_yields_interpreted_improvement(self):
        result = compare_runs(run(), run("b", 0.5), "error")
        self.assertAlmostEqual(result["delta"], -0.1)
        self.assertIsNone(result["improvement"])
        self.assertEqual(result["comparison_status"], "METRIC_DIRECTION_REVIEW_REQUIRED")
        self.assertTrue(result["metric_direction_review_required"])

    def test_caller_declared_min_direction(self):
        result = compare_runs(run(), run("b", 0.5), "error", lower_is_better=True)
        self.assertAlmostEqual(result["improvement"], 0.1)
        self.assertEqual(result["metric_direction"], "min")
        self.assertEqual(result["comparison_status"], "DEVELOPMENT_ONLY")

    def test_both_run_declared_min_direction(self):
        a, b = run(), run("b", 0.5)
        a["metric_direction"] = b["metric_direction"] = "min"
        result = compare_runs(a, b, "error")
        self.assertAlmostEqual(result["improvement"], 0.1)
        self.assertIn("NOT_INDEPENDENTLY_VERIFIED", result["metric_direction_source"])

    def test_mixed_or_conflicting_direction_rejected(self):
        a, b = run(), run("b")
        a["metric_direction"] = "min"
        with self.assertRaisesRegex(ContractError, "metric_direction"):
            compare_runs(a, b, "error")
        b["metric_direction"] = "max"
        with self.assertRaisesRegex(ContractError, "metric_direction"):
            compare_runs(a, b, "error")
        b["metric_direction"] = "min"
        with self.assertRaisesRegex(ContractError, "conflicts"):
            compare_runs(a, b, "error", lower_is_better=False)

    def test_invalid_direction_rejected_by_contract(self):
        x = run()
        x["metric_direction"] = "smaller"
        with self.assertRaisesRegex(ContractError, "metric_direction"):
            validate_run(x)

    def test_budget_and_holdout_remain_protected(self):
        a, b = run(), run("b")
        b["budget_basis"] = "other"
        result = compare_runs(a, b, "error")
        self.assertEqual(result["comparison_status"], "BUDGET_REVIEW_REQUIRED")
        self.assertTrue(result["metric_direction_review_required"])
        b["split"] = "sealed"
        b["frozen_protocol_ref"] = "frozen"
        b["authorization_ref"] = "user"
        with self.assertRaisesRegex(ContractError, "sealed"):
            compare_runs(a, b, "error", lower_is_better=True)


class FigureProvenanceTests(unittest.TestCase):
    def _spec(self, fingerprint):
        return {"schema_version": "pd-rw-figure-spec-v1",
                "figure_id": "F1", "scientific": {}, "sources": {"source_fingerprint": fingerprint},
                "design": {}, "outputs": {}, "qa": {"science_qa": "PASS",
                                                     "connectors_qa": "PASS",
                                                     "visual_qa": "PASS"}}

    def test_first_render_requires_real_source_check(self):
        result = advise(None, self._spec("sha256-manually-checked"))
        self.assertEqual(result["change_flags"], ["FIRST_RENDER"])
        self.assertIn("REAL_SOURCE_AND_CLAIMS", result["suggested_checks"])

    def test_unknown_source_cannot_be_treated_as_first_render_pass(self):
        result = advise(None, self._spec("UNKNOWN"))
        self.assertIn("SOURCE_UNVERIFIED", result["change_flags"])
        self.assertIn("REAL_SOURCE_AND_CLAIMS", result["suggested_checks"])

    def test_clean_cached_spec_retains_skip_behavior(self):
        spec = self._spec("sha256-manually-checked")
        result = advise(spec, deepcopy(spec))
        self.assertEqual(result["change_flags"], ["NO_SPEC_CHANGE"])
        self.assertEqual(result["suggested_checks"], [])


class ReferenceIntegrityTests(unittest.TestCase):
    def test_matching_metadata_is_not_source_claim_support(self):
        audit = audit_batch({"expected_count": 1, "references": [GOOD_REF]},
                            fetch=ref_fetch)
        self.assertEqual(audit["status"], "DOI_METADATA_AUDITED_NOT_CLAIMS")
        self.assertEqual(audit["metadata_integrity"], "ALL_MATCHED_NOT_CLAIM_VERIFIED")
        self.assertEqual(audit["source_claim_support"], "NOT_CHECKED")

    def test_duplicate_ref_id_and_doi_surface_in_summary(self):
        audit = audit_batch({"expected_count": 2, "references": [GOOD_REF, GOOD_REF]},
                            fetch=ref_fetch)
        self.assertEqual(audit["duplicate_ref_id_count"], 1)
        self.assertEqual(audit["duplicate_doi_count"], 1)
        self.assertEqual(audit["metadata_integrity"], "ISSUES_REQUIRE_MANUAL_REVIEW")

    def test_failed_metadata_record_prevents_all_matched(self):
        bad = dict(GOOD_REF, title="False study")
        audit = audit_batch({"expected_count": 1, "references": [bad]},
                            fetch=ref_fetch)
        self.assertEqual(audit["metadata_integrity"], "ISSUES_REQUIRE_MANUAL_REVIEW")
        self.assertEqual(audit["status_counts"]["METADATA_MISMATCH"], 1)

    def test_boolean_expected_count_rejected(self):
        with self.assertRaisesRegex(ValueError, "expected_count"):
            audit_batch({"expected_count": True, "references": [GOOD_REF]},
                        fetch=ref_fetch)


if __name__ == "__main__":
    unittest.main()
