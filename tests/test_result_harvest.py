"""Scientific result-harvest tests use synthetic summaries only."""
import unittest
from core.result_harvest import inspect_existing_results as inspect


def example():
    return {
        "role": "DEV", "task_id": "T1", "protocol_id": "P1",
        "metric": "accuracy", "higher_is_better": True, "group_unit": "subject",
        "champion_run_ref": "RUN_B", "baseline_run_ref": "RUN_A",
        "selection_history_ref": "history.json",
        "matched_information_and_evaluator": True,
        "observations": [
            {"group": "P1", "condition": "device_A", "baseline": .60, "champion": .80},
            {"group": "P2", "condition": "device_A", "baseline": .70, "champion": .75},
            {"group": "P3", "condition": "device_B", "baseline": .70, "champion": .62},
            {"group": "P4", "condition": "device_B", "baseline": .65, "champion": .60},
        ],
    }


class ResultHarvestTests(unittest.TestCase):
    def test_signed_condition_variation_is_only_exploratory(self):
        result = inspect(example())
        self.assertEqual(result["status"], "EXPLORATORY_ONLY")
        self.assertIn("OPPOSITE_SIGN_ACROSS_CONDITIONS_EXPLORATORY",
                      result["candidate_clues"])
        self.assertEqual(result["distinct_declared_groups_total"], 4)
        self.assertFalse(result["science_confirmed"])
        self.assertFalse(result["q2_potential_verified"])
        self.assertFalse(result["source_metrics_independently_verified"])
        self.assertFalse(result["causal_mechanism_verified"])

    def test_lower_is_better_and_no_invented_significance(self):
        p = example()
        p["metric"] = "error"
        p["higher_is_better"] = False
        v = inspect(p)
        self.assertGreater(v["condition_summaries"][1]["unweighted_mean_paired_gain"], 0)
        self.assertNotIn("p_value", str(v))

    def test_group_mixed_effects_and_resource_difference(self):
        p = example()
        p["observations"][1]["champion"] = .50
        p["measured_costs"] = [{"name": "labels", "unit": "count", "baseline": 20,
                                "champion": 5}]
        v = inspect(p)
        self.assertIn("WITHIN_CONDITION_GROUP_HETEROGENEITY_EXPLORATORY",
                      v["candidate_clues"])
        self.assertIn("MEASURED_RESOURCE_DIFFERENCE_EXPLORATORY",
                      v["candidate_clues"])
        self.assertEqual(v["cost_observations"][0]["difference"], -15)

    def test_same_snapshot_reused(self):
        p = example()
        h = inspect(p)["input_sha256"]
        p["previous_packet_sha256"] = h
        self.assertEqual(inspect(p)["status"], "UNCHANGED_INPUT_REUSE")

    def test_reject_sealed_and_wrong_protocol(self):
        p = example()
        p["role"] = "SEALED_CONFIRM"
        with self.assertRaises(PermissionError):
            inspect(p)
        p["role"] = "DEV"
        p["matched_information_and_evaluator"] = False
        with self.assertRaises(ValueError):
            inspect(p)

    def test_reject_duplicate_group_condition(self):
        p = example()
        p["observations"].append(dict(p["observations"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            inspect(p)

    def test_reject_bad_numbers_or_missing_sources(self):
        p = example()
        p["observations"][0]["baseline"] = float("nan")
        with self.assertRaisesRegex(ValueError, "finite"):
            inspect(p)
        p = example()
        p["selection_history_ref"] = ""
        with self.assertRaises(ValueError):
            inspect(p)

    def test_reject_unbounded_slice_search(self):
        p = example()
        p["observations"] = [{"group": str(i), "condition": str(i),
                               "baseline": 0, "champion": 1} for i in range(21)]
        with self.assertRaisesRegex(ValueError, "20"):
            inspect(p)

    def test_no_fake_confirmation_from_uniform_gain(self):
        p = example()
        for r in p["observations"]:
            r["champion"] = r["baseline"] + .05
        v = inspect(p)
        self.assertEqual(v["candidate_clues"], ["THIN_DECLARED_GROUP_SUPPORT"])
        self.assertFalse(v["independent_groups_verified"])


if __name__ == "__main__":
    unittest.main()
