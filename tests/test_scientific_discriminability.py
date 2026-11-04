"""Synthetic metadata tests: descriptive structure, never causal or Q2 validation."""
import unittest
from core.scientific_discriminability import screen_discriminability as screen


class ScientificDiscriminabilityTests(unittest.TestCase):
    def check(self, rows):
        return screen(rows, factor_a="device", factor_b="class",
                      group_key="subject", role="DEV")

    def test_device_and_subject_confounded_even_when_class_crossed(self):
        rows = [
            {"device": "A", "class": c, "subject": "P1"} for c in ("walk", "run")
        ] + [
            {"device": "B", "class": c, "subject": "P2"} for c in ("walk", "run")
        ]
        d = self.check(rows)
        self.assertEqual(d["status"], "CROSSED_THIN_DECLARED_GROUPS")
        self.assertTrue(d["each_declared_group_fixed_within_factor"]["factor_a"])
        self.assertEqual(d["distinct_declared_groups_total"], 2)
        self.assertFalse(d["causal_identification_verified"])
        self.assertFalse(d["science_verified"])

    def test_nested_device_subject_factor_is_detected(self):
        rows = [{"device": "A", "class": "one", "subject": "P1"},
                {"device": "B", "class": "two", "subject": "P2"}]
        self.assertEqual(self.check(rows)["status"], "STRUCTURALLY_NESTED_OR_CONFOUNDED")

    def test_full_crossing_does_not_cause_causal_pass(self):
        rows = [{"device": d, "class": c, "subject": f"p{n}"}
                for d in ("A", "B") for c in ("one", "two") for n in (1, 2)]
        result = self.check(rows)
        self.assertEqual(result["status"], "DESCRIPTIVELY_CROSSED")
        self.assertFalse(result["independence_verified"])

    def test_missing_cell_and_single_factor(self):
        rows = [{"device": "A", "class": "one", "subject": "p1"},
                {"device": "A", "class": "two", "subject": "p2"},
                {"device": "B", "class": "two", "subject": "p3"}]
        self.assertEqual(self.check(rows)["status"], "PARTIALLY_CROSSED")
        self.assertEqual(self.check(rows[:2])["status"], "NO_TWO_FACTOR_CONTRAST")

    def test_invalid_role_or_metadata_are_rejected(self):
        with self.assertRaises(PermissionError):
            screen([], factor_a="a", factor_b="b", group_key="g", role="SEALED_CONFIRM")
        with self.assertRaises(ValueError):
            self.check([{"device": "A", "class": "one"}])
        with self.assertRaises(ValueError):
            screen([{"a": 1, "b": 2, "g": 3}], factor_a="a", factor_b="a",
                   group_key="g", role="DEV")


if __name__ == "__main__":
    unittest.main()
