"""Synthetic offline regression: manuscript guard is a warning aid, not scientific proof."""
import tempfile
import unittest
from pathlib import Path

from core.manuscript_claim_guard import check_provenance, compare_manuscripts


def provenance_case(**changes):
    item = {
        "claim_id": "C01",
        "text_anchor": "Independently confirmed on the held-out cohort",
        "asserted_role": "INDEPENDENT_CONFIRMATION",
        "source_role": "CONFIRMATION",
        "split_id": "CONFIRM-01",
        "development_split_ids": ["DEV-01"],
        "selected_on_source": False,
        "protocol_frozen": True,
        "evidence_ref": "runs/confirm-01",
    }
    item.update(changes)
    return check_provenance({"claims": [item]})


class ManuscriptClaimGuardTests(unittest.TestCase):
    def compare(self, before, after):
        with tempfile.TemporaryDirectory() as root:
            p, q = Path(root) / "before.md", Path(root) / "after.md"
            p.write_text("# Results\n\n" + before + "\n", encoding="utf-8")
            q.write_text("# Results\n\n" + after + "\n", encoding="utf-8")
            return compare_manuscripts(str(p), str(q))

    def test_identical_manuscript_is_not_claimed_semantically_verified(self):
        r = self.compare("The mean score was 0.81.", "The mean score was 0.81.")
        self.assertEqual(r["result"], "NO_HEURISTIC_ALERT_NOT_PROOF")

    def test_changed_p_value_is_flagged(self):
        r = self.compare("We observed p=0.08.", "We observed p=0.008.")
        self.assertIn("NUMERIC_OR_STATISTIC_CHANGED", r["flagged_changed_blocks"][0]["flags"])

    def test_association_to_cause_is_flagged(self):
        r = self.compare("Motion was associated with error.", "Motion caused error.")
        flags = r["flagged_changed_blocks"][0]["flags"]
        self.assertIn("CAUSAL_LANGUAGE_ADDED", flags)
        self.assertIn("ASSOCIATION_TO_CAUSAL_POSSIBLE", flags)

    def test_negation_or_significance_changes_flagged(self):
        r = self.compare("The effect was not significant.", "The effect was significant.")
        self.assertIn("NEGATION_CHANGED", r["flagged_changed_blocks"][0]["flags"])

    def test_data_role_changed_is_flagged(self):
        r = self.compare("Performance on DEV was 0.7.", "Performance on TEST was 0.7.")
        self.assertIn("DATA_ROLE_WORD_CHANGED", r["flagged_changed_blocks"][0]["flags"])

    def test_figure_or_reference_only_changes_are_not_proven_safe(self):
        r = self.compare("The result was limited.", "The result was limited to cohort A.")
        self.assertEqual(r["result"], "NO_HEURISTIC_ALERT_NOT_PROOF")
        self.assertIn("not semantic equivalence", r["limitations"])

    def test_development_split_cannot_be_independent_confirmation(self):
        r = provenance_case(source_role="DEV", split_id="DEV-01")
        self.assertEqual(r["result"], "BLOCK")
        self.assertIn("DEVELOPMENT_OR_VALIDATION_MISLABELED_INDEPENDENT", r["items"][0]["reasons"])

    def test_reused_split_even_if_labelled_confirmation_is_blocked(self):
        r = provenance_case(split_id="DEV-01")
        self.assertIn("SPLIT_REUSED_FOR_DEVELOPMENT", r["items"][0]["reasons"])

    def test_selection_on_confirmation_source_is_blocked(self):
        r = provenance_case(selected_on_source=True)
        self.assertIn("SELECTION_USED_CONFIRMATION_SOURCE", r["items"][0]["reasons"])

    def test_unfrozen_protocol_is_blocked(self):
        r = provenance_case(protocol_frozen=False)
        self.assertIn("CONFIRMATION_PROTOCOL_NOT_FROZEN", r["items"][0]["reasons"])

    def test_missing_claim_provenance_is_review_required(self):
        r = provenance_case(evidence_ref=None)
        self.assertEqual(r["result"], "REVIEW_REQUIRED")
        self.assertIn("MISSING_EVIDENCE_REF", r["items"][0]["reasons"])

    def test_complete_declared_metadata_is_not_verification(self):
        r = provenance_case()
        self.assertEqual(r["result"], "DECLARED_METADATA_NO_CONFLICT_NOT_PROOF")

    def test_empty_packet_is_not_checked(self):
        self.assertEqual(check_provenance({"claims": []})["result"], "NOT_CHECKED")


if __name__ == "__main__":
    unittest.main()
