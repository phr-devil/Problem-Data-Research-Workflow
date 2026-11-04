"""Behavior checks: complete metadata can never self-certify Q2 success."""
import unittest
from core.q2_preflight import preflight, CLAIM_KEYS, VENUE_KEYS


class Q2PreflightTests(unittest.TestCase):
    def _packet(self):
        data = {key: "verifiable-source-pointer" for key in CLAIM_KEYS}
        data["venues"] = [{**{k: "source-backed" for k in VENUE_KEYS},
                           "journal": "Example venue", "quartile": "Q2",
                           "recent_comparable_articles": ["DOI:example"]}]
        return data

    def test_missing_science_does_not_qualify(self):
        x = preflight({"venues": []})
        self.assertEqual(x["status"], "INCOMPLETE")
        self.assertFalse(x["q2_potential_supported"])

    def test_q3_cannot_pass_minimum(self):
        x = self._packet()
        x["venues"][0]["quartile"] = "Q3"
        y = preflight(x)
        self.assertEqual(y["status"], "INCOMPLETE")
        self.assertIn("VERIFIABLE_JCR_Q1_OR_Q2_VENUE_CANDIDATE", y["missing"])

    def test_structurally_complete_is_still_not_scientific_certification(self):
        x = preflight(self._packet())
        self.assertEqual(x["status"], "READY_FOR_HUMAN_SCIENTIFIC_AND_JCR_REVIEW")
        self.assertFalse(x["q2_potential_supported"])
        self.assertEqual(x["human_science_review"], "REQUIRED")

    def test_non_dict_or_unsupported_quartile(self):
        self.assertEqual(preflight([])["status"], "INCOMPLETE")
        data = self._packet()
        data["venues"][0]["quartile"] = "UNKNOWN"
        self.assertEqual(preflight(data)["status"], "INCOMPLETE")


if __name__ == "__main__":
    unittest.main()
