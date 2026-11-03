"""SAFE-Gait inspired information-condition regression tests; no model fitting."""
from __future__ import annotations
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from core.contracts import ContractError
from core.information_probe import review_information_shift
from core.cli import main

def task_info(*, before=True):
    return {
        "task_id": "APACE" if before else "SAFE-Gait",
        "protocol_id": "zero-label" if before else "one-calibration",
        "target_label_k": 0 if before else 1,
        "k_unit": "per new wearer",
        "legal_predecision_information": (
            ["insole signals"] if before
            else ["insole signals", "one supervised calibration residual"]
        ),
    }

def case(**overrides):
    value={
      "root_problem": "subject-specific cross-condition gait prediction",
      "before": task_info(),
      "after": task_info(before=False),
      "new_information": {
        "available_before_prediction": True,
        "support_query_disjoint": True,
        "cost_feasible": True,
        "same_information_simple_baseline": True
      },
      "evidence": {
        "oracle_gain_range": [0.08,0.10],
        "learned_policy_stable_advantage": False,
        "refs": ["APACE dev-only diagnostic", "SAFE-Gait 2026-10-28 manuscript summary"]
      },
      "unresolved_shared_blockers": [],
    }
    value.update(overrides)
    return value

class InformationSettingTests(unittest.TestCase):
    def test_positive_case_is_only_candidate_not_success(self):
        result=review_information_shift(case())
        self.assertEqual(result["decision"],"INFORMATION_SETTING_PIVOT_CANDIDATE")
        self.assertTrue(result["oracle_policy_gap"])
        self.assertEqual(result["science_success"],"NOT_EVALUATED")
        self.assertEqual(result["previous_task_success"],"NOT_INFERRED")
        self.assertTrue(result["requires_new_task_protocol_and_claim"])

    def test_no_new_information_is_not_a_new_lever(self):
        after={**task_info(before=False),"target_label_k":0,
               "legal_predecision_information":["insole signals"]}
        result=review_information_shift(case(after=after))
        self.assertEqual(result["decision"],"NO_NEW_INFORMATION_LEVER")

    def test_future_target_label_is_inadmissible(self):
        value=case(new_information={
            "available_before_prediction":False,
            "support_query_disjoint":True,
            "cost_feasible":True,
            "same_information_simple_baseline":True})
        result=review_information_shift(value)
        self.assertEqual(result["decision"],"INADMISSIBLE_OR_UNAFFORDABLE_INFORMATION")

    def test_support_query_overlap_is_inadmissible(self):
        info={**case()["new_information"],"support_query_disjoint":False}
        self.assertEqual(review_information_shift(case(new_information=info))["decision"],
                         "INADMISSIBLE_OR_UNAFFORDABLE_INFORMATION")

    def test_shared_missing_truth_still_blocks_alternative(self):
        value=case(unresolved_shared_blockers=["no independent reference labels on any device"])
        result=review_information_shift(value)
        self.assertEqual(result["decision"],"UNRESOLVED_SHARED_PREMISE")
        self.assertIn("COMMON_FAILURE_PREMISE_NOT_RESOLVED",result["warnings"])

    def test_unknown_access_is_uncertainty_not_stop(self):
        info={**case()["new_information"],"available_before_prediction":None}
        result=review_information_shift(case(new_information=info))
        self.assertEqual(result["decision"],"ACCESS_OR_SUPPORT_QUERY_UNKNOWN")
        self.assertNotEqual(result["science_success"],"FAILED")

    def test_oracle_is_not_deployable_performance(self):
        v=case(evidence={"oracle_gain":0.12,"learned_vs_simple":0.03,"refs":["dev comparison"]})
        result=review_information_shift(v)
        self.assertFalse(result["oracle_policy_gap"])
        self.assertEqual(result["science_success"],"NOT_EVALUATED")

    def test_k_unit_and_identity_are_part_of_contract(self):
        bad=case()
        bad["after"]["k_unit"]=""
        with self.assertRaises(ContractError):
            review_information_shift(bad)
        bad=case()
        bad["after"]["protocol_id"]=bad["before"]["protocol_id"]
        bad["after"]["task_id"]=bad["before"]["task_id"]
        with self.assertRaises(ContractError):
            review_information_shift(bad)

    def test_evidence_numeric_cannot_be_fabricated(self):
        v=case(evidence={"oracle_gain":float("nan"),"refs":["bad"]})
        with self.assertRaises(ContractError):
            review_information_shift(v)

    def test_cli_is_read_only(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"case.json"
            path.write_text(json.dumps(case()),encoding="utf-8")
            output=io.StringIO()
            with redirect_stdout(output):
                rc=main(["information-check","--file",str(path)])
            result=json.loads(output.getvalue())
            self.assertEqual(rc,0)
            self.assertEqual(result["decision"],"INFORMATION_SETTING_PIVOT_CANDIDATE")
            self.assertEqual(set(p.name for p in Path(temp).iterdir()),{"case.json"})

if __name__=="__main__":
    unittest.main()
