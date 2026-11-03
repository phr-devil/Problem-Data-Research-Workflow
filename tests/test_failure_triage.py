import unittest
from core.contracts import ContractError
from core.failure_triage import review_failure

def case(*findings):
    return {"task_id":"T1","protocol_id":"P1","findings":[
        {"kind":k,"evidence_level":e,"evidence_ref":r}
        for k,e,r in findings]}

class FailureTriageTests(unittest.TestCase):
    def test_invalid_evaluator_outranks_gain(self):
        r=review_failure(case(
            ("SIMPLE_BASELINE_DOMINATES","OBSERVED","runs/r1.json"),
            ("EVALUATION_INVALID","OBSERVED","audits/causality.json")))
        self.assertEqual(r["suggested_route"],"REPAIR_AFFECTED_EVIDENCE")
        self.assertEqual(r["decision_scope"],"RUN")
        self.assertEqual(r["execution"],"NOT_RUN")
    def test_information_failure_routes_to_changed_information_task(self):
        r=review_failure(case(("LEGAL_INFORMATION_GAP","OBSERVED","runs/apace.json")))
        self.assertEqual(r["suggested_route"],"REVIEW_INFORMATION_PIVOT")
        self.assertEqual(r["decision_scope"],"TASK")
        self.assertEqual(r["authorization"],"NOT_GRANTED")
    def test_svm_baseline_does_not_confirm_paper(self):
        r=review_failure(case(("SIMPLE_BASELINE_DOMINATES","OBSERVED","runs/svm.json")))
        self.assertEqual(r["suggested_route"],"KEEP_BASELINE_REVIEW_NEW_LEVER")
        self.assertNotIn("PROJECT_STOP",r.values())
    def test_hypothesis_is_not_reclassified_as_observation(self):
        r=review_failure(case(("EVALUATION_INVALID","HYPOTHESIZED","report.md")))
        self.assertEqual(r["suggested_route"],"INSPECT_PRIMARY_EVIDENCE")
        self.assertEqual(r["hypotheses_not_established"],["EVALUATION_INVALID"])
    def test_rejects_unreferenced_claim(self):
        with self.assertRaises(ContractError):
            review_failure(case(("EVALUATION_INVALID","OBSERVED","")))
    def test_inconclusive_remains_open(self):
        r=review_failure(case(("STATISTICAL_UNCERTAINTY","OBSERVED","runs/ci.json")))
        self.assertEqual(r["suggested_route"],"INCONCLUSIVE_MINIMUM_PROBE")

if __name__ == "__main__":
    unittest.main()
