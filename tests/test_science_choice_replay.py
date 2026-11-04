"""Adversarial synthetic choices; not a measured Q2/research-success benchmark."""
import json
from pathlib import Path
import unittest
from core.science_choice_replay import blind_agent_cases, score_choices

CASES = json.loads((Path(__file__).resolve().parents[1] /
                    "evals/science_choice_cases.synthetic.json").read_text(encoding="utf-8"))


def correct_responses():
    result = []
    for case in CASES:
        result.append({
            "case_id": case["case_id"],
            "selected_choice": case["expert"]["acceptable_choices"][0],
            "noticed_risks": case["expert"]["must_notice"],
            "next_action_type": ("REQUEST_USER_CHOICE" if "DOWNLOAD" in case["case_id"]
                                 else "READ_ONLY"),
            "q2_decision": "Q2_UNCERTAIN",
        })
    return result


class ScienceChoiceReplayTests(unittest.TestCase):
    def test_blind_contexts_hide_expert_answers(self):
        visible = blind_agent_cases(CASES)
        self.assertEqual(len(visible), 4)
        self.assertNotIn("expert", visible[0])
        self.assertNotIn("acceptable_choices", str(visible))

    def test_curated_synthetic_cases_pass_contract(self):
        report = score_choices(CASES, correct_responses())
        self.assertTrue(report["all_contracts_pass"])
        self.assertEqual(report["real_blinded_research_improvement"], "NOT_MEASURED")

    def test_cheap_low_novelty_choice_is_not_automatically_right(self):
        rows = correct_responses()
        rows[0]["selected_choice"] = "easy_one_percent_tuning"
        self.assertFalse(score_choices(CASES, rows)["cases"][0]["contract_pass"])

    def test_confounded_causal_claim_fails(self):
        rows = correct_responses()
        rows[1]["selected_choice"] = "claim_device_causes_drop"
        self.assertFalse(score_choices(CASES, rows)["cases"][1]["contract_pass"])

    def test_missing_auth_or_premature_q2_fails(self):
        rows = correct_responses()
        rows[-1]["next_action_type"] = "TRAIN_DEV"
        self.assertFalse(score_choices(CASES, rows)["cases"][-1]["authorization_scope_respected"])
        rows = correct_responses()
        rows[0]["q2_decision"] = "Q2_POTENTIAL_SUPPORTED"
        self.assertFalse(score_choices(CASES, rows)["cases"][0]["no_unsupported_q2_success"])

    def test_missing_or_duplicate_response_rejected(self):
        with self.assertRaises(ValueError):
            score_choices(CASES, correct_responses()[:2])
        duplicate = correct_responses()
        duplicate[1]["case_id"] = duplicate[0]["case_id"]
        with self.assertRaises(ValueError):
            score_choices(CASES, duplicate)


if __name__ == "__main__":
    unittest.main()
