"""Reconstructed historical replay fixture integrity, not an agent blind test."""
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class ReplayFixtureTests(unittest.TestCase):
    def setUp(self):
        self.case=json.loads((ROOT/"LESSONS/SAFE_GAIT_REPLAY.json").read_text(encoding="utf-8"))

    def test_replay_is_not_misrepresented_as_blinded(self):
        self.assertEqual(self.case["blinded_evaluation_status"],"NOT_RUN")
        self.assertIn("RECONSTRUCTED",self.case["source_status"])
        self.assertEqual(len(self.case["checkpoints"]),3)

    def test_earlier_checkpoints_do_not_reveal_later_success(self):
        first=self.case["checkpoints"][0]
        second=self.case["checkpoints"][1]
        self.assertNotIn("SAFE-Gait succeeds",json.dumps(first["visible_evidence"]))
        self.assertEqual(second["visible_evidence"]["future_perf"],"UNKNOWN")
        self.assertFalse(any("DS cross-dataset advantage" in json.dumps(item)
                              for item in [x["visible_evidence"] for x in self.case["checkpoints"][:2]))

    def test_negative_controls_have_distinct_invalid_reasons(self):
        controls=self.case["negative_controls"]
        self.assertEqual(len(controls),3)
        self.assertTrue(all(c["id"].startswith("N") and c["expected_route"] for c in controls))
        self.assertEqual(len({c["expected_route"] for c in controls}),3)

if __name__=="__main__":
    unittest.main()
