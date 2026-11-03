"""Tests for advisory feasibility routing; synthetic metadata, no data or training."""
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from core.cli import main
from core.contracts import ContractError
from core.feasibility_review import review_feasibility


def sample(delta=None, fmt="forge-dev-classification-v1"):
    result = {
        "task_id": "T", "protocol_id": "P", "candidate": "C",
        "evaluation_type": fmt, "n_independent_groups": 4,
        "data_validity": "HASHED_DEV_AND_METRIC_ARITHMETIC_ONLY",
        "evidence_ref": "runs/C/RUN.json",
        "signal_evidence": "UNKNOWN_WITHOUT_MATCHED_REFERENCE",
        "remaining_error": {"measure": "classification_error_rate",
                            "group_macro_mean": 0.15,
                            "theoretical_attainable_gain": "UNKNOWN"},
        "paired_evidence": None,
    }
    if delta is not None:
        result["signal_evidence"] = (
            "DEV_IMPROVEMENT_OVER_REFERENCE_OBSERVED" if delta > 0 else
            "NO_DEV_IMPROVEMENT_OVER_REFERENCE_OBSERVED" if delta < 0 else
            "DEV_TIE_WITH_REFERENCE"
        )
        result["paired_evidence"] = {
            "metric": "macro_F1", "directional_delta": delta,
            "scientific_claim_confirmed": False,
        }
    return result


class FeasibilityRoutingTests(unittest.TestCase):
    def test_unknown_signal_is_not_a_failed_task(self):
        a = review_feasibility(sample())
        self.assertEqual(a["suggested_route"], "GET_FAIR_SIMPLE_REFERENCE_IF_AUTHORIZED")
        self.assertFalse(a["automatic_project_stop"])
        self.assertFalse(a["fitting_performed"])
        self.assertEqual(a["scientific_success"], "NOT_DETERMINED")

    def test_positive_relative_gain_is_not_paper_confirmation(self):
        a = review_feasibility(sample(0.03))
        self.assertEqual(a["suggested_route"], "VERIFY_RESIDUAL_MECHANISM_AND_UNSEEN_GROUPS")
        self.assertEqual(a["status"], "ADVISORY_INPUT_NOT_REVERIFIED")

    def test_negative_relative_gain_does_not_imply_project_stop(self):
        a = review_feasibility(sample(-0.01))
        self.assertEqual(a["suggested_route"], "REVIEW_NEW_LEGAL_INFORMATION_OR_DISTINCT_FAILURE_PREMISE")
        self.assertFalse(a["automatic_project_stop"])

    def test_bad_oracle_claim_rejected(self):
        x = sample()
        x["remaining_error"]["theoretical_attainable_gain"] = 0.8
        with self.assertRaisesRegex(ContractError, "Residual magnitude"):
            review_feasibility(x)

    def test_contradictory_delta_rejected(self):
        x = sample(0.02)
        x["signal_evidence"] = "NO_DEV_IMPROVEMENT_OVER_REFERENCE_OBSERVED"
        with self.assertRaisesRegex(ContractError, "contradicts paired delta"):
            review_feasibility(x)

    def test_small_groups_marked_without_refusal(self):
        x = sample()
        x["n_independent_groups"] = 2
        a = review_feasibility(x)
        self.assertEqual(a["group_uncertainty"], "LIMITED_GROUP_EVIDENCE")

    def test_event_route_is_task_specific(self):
        a = review_feasibility(sample(fmt="forge-dev-event-v1"))
        self.assertEqual(a["suggested_route"], "USE_TASK_SPECIFIC_EVENT_DIAGNOSTIC")

    def test_cli_requires_no_extra_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "report.json"
            p.write_text(json.dumps(sample()), encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                status = main(["feasibility-check", "--file", str(p)])
            self.assertEqual(status, 0)
            self.assertIn("GET_FAIR_SIMPLE_REFERENCE", output.getvalue())
            self.assertEqual([x.name for x in Path(directory).iterdir()], ["report.json"])


if __name__ == "__main__":
    unittest.main()
