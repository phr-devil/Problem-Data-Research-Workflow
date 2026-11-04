"""Synthetic behavior checks for early-stop, counterevidence and pre-D1 data fit."""
import copy
import unittest

from core.search_choice_review import review_choice


def packet():
    return {
        "format": "pd-rw-search-choice-v1",
        "user_scope": "specified field, public datasets only",
        "coverage": {"query_families_ref": "search/keywords.md",
                     "source_families_ref": "search/sources.md",
                     "critical_coverage_gaps": []},
        "candidates": [
            {"id": "A", "scientific_question": "Important unanswered boundary?",
             "importance_basis": "real deployment consequences",
             "knowledge_delta_or_unknown": "difference from DOI",
             "decisive_unknown": "can independent environments separate causes?",
             "nearest_original_status": "ORIGINAL_CHECKED",
             "nearest_original_ref": "doi:synthetic-not-real",
             "counterevidence_status": "CHECKED"},
            {"id": "B", "scientific_question": "Alternative failure mechanism?",
             "importance_basis": "distinct practical failure",
             "knowledge_delta_or_unknown": "unverified alternative",
             "decisive_unknown": "signal before decision"},
        ],
        "preferred_id": "A",
        "why_preferred_over_competitor": "A offers a cleaner legal comparison",
        "contrasting_opportunity_search": {
            "status": "ALTERNATIVE_FOUND",
            "different_premise_or_query": "different failure premise",
            "source_or_query_ref": "search/alternatives.md"},
        "pre_download_data_fit": {
            "status": "OFFICIAL_METADATA_SUPPORTS",
            "official_source_ref": "official:dataset-description",
            "needed_factors_and_truth": "group × condition, measured truth",
            "independent_group_unit": "person",
            "confounding_or_unknown": "device/person nesting remains unknown",
            "legal_input_and_confirmation": "legal features with reserved groups"},
        "next_discriminating_check": "read original dataset protocol",
    }


class SearchChoiceReviewTests(unittest.TestCase):
    def test_comparative_preflight_does_not_certify_science(self):
        x = review_choice(packet())
        self.assertEqual(x["decision"], "STRUCTURALLY_READY_FOR_D1_PLANNING_ONLY")
        self.assertFalse(x["science_value_ranked"])
        self.assertFalse(x["download_authorized"])
        self.assertFalse(x["q2_potential_verified"])

    def test_first_satisficing_single_choice_is_flagged(self):
        p = packet()
        p["candidates"] = p["candidates"][:1]
        p["contrasting_opportunity_search"]["status"] = "NOT_CHECKED"
        x = review_choice(p)
        self.assertEqual(x["decision"], "REASSESS_OR_COMPARE_BEFORE_D1")
        self.assertIn("FIRST_SATISFICING_RISK", x["flags"])

    def test_single_strong_candidate_after_genuine_contrast_is_allowed(self):
        p = packet()
        p["candidates"] = p["candidates"][:1]
        p["contrasting_opportunity_search"]["status"] = "NO_BETTER_ALTERNATIVE_WITH_LIMITS"
        x = review_choice(p)
        self.assertEqual(x["decision"], "STRUCTURALLY_READY_FOR_D1_PLANNING_ONLY")

    def test_competitor_exists_but_not_compared(self):
        p = packet()
        p["candidates"] = p["candidates"][:1]
        x = review_choice(p)
        self.assertIn("UNEXAMINED_COMPETING_OPPORTUNITY", x["flags"])
        p = packet()
        p["why_preferred_over_competitor"] = ""
        self.assertIn("COMPARATIVE_REASON_MISSING", review_choice(p)["flags"])

    def test_missing_nearest_paper_and_confounding_are_not_success(self):
        p = packet()
        p["candidates"][0]["nearest_original_status"] = "UNKNOWN"
        p["pre_download_data_fit"]["status"] = "UNKNOWN"
        x = review_choice(p)
        self.assertIn("NEAREST_ORIGINAL_NOT_VERIFIED", x["flags"])
        self.assertIn("D1_SCIENTIFIC_FIT_UNKNOWN", x["flags"])
        self.assertNotEqual(x["decision"], "STRUCTURALLY_READY_FOR_D1_PLANNING_ONLY")

    def test_dataset_metadata_contradicts_proposed_claim(self):
        p = packet()
        p["pre_download_data_fit"]["status"] = "OFFICIAL_METADATA_CONTRADICTS"
        x = review_choice(p)
        self.assertEqual(x["decision"], "REASSESS_OR_COMPARE_BEFORE_D1")
        self.assertIn("D1_INCOMPATIBLE_WITH_PROPOSED_CLAIM", x["flags"])

    def test_scope_and_ids_cannot_be_invented(self):
        p = packet()
        p["preferred_id"] = "MADE_UP"
        with self.assertRaises(ValueError):
            review_choice(p)
        p = packet()
        p["candidates"] = p["candidates"] * 3
        with self.assertRaises(ValueError):
            review_choice(p)

    def test_critical_search_gap_is_visible(self):
        p = packet()
        p["coverage"]["critical_coverage_gaps"] = ["unread closest paper"]
        x = review_choice(p)
        self.assertIn("SEARCH_PARTIAL_CRITICAL_GAPS", x["flags"])
