"""Real replay-contract behavior, not a claim of scientific Agent success."""
import unittest
from chapter10_replay import audit_responses


CASE = [{"id": "Q2-DEMO", "expected_route": "PAPER_FIRST.md",
         "decision_scope": "EVIDENCE"}]
BASE = {
    "case_id": "Q2-DEMO", "route": "PAPER_FIRST.md",
    "evidence_used": ["run:R1"], "next_action": "inspect one gap",
    "auth": "read-only", "decision_scope": "EVIDENCE",
    "claim_boundary": "DEV only", "cost_cap": "zero fit",
    "expected_decision_change": "Q2 evidence yes/no",
}


def status(**updates):
    row = {**BASE, **updates}
    return audit_responses([row], CASE)[0]


class DecisionReplayContractTests(unittest.TestCase):
    def test_legacy_result_still_accepted(self):
        self.assertEqual(status()["status"], "CONTRACT_OK")

    def test_in_scope_agent_instruction_requires_verification(self):
        x = status(next_action_owner="AGENT_DECIDABLE",
                   next_agent_instruction="Read existing DEV Run",
                   authorization_verified=True)
        self.assertEqual(x["status"], "CONTRACT_OK")
        self.assertEqual(status(next_action_owner="AGENT_DECIDABLE",
                                next_agent_instruction="Run GPU")["status"], "INVALID")

    def test_human_choice_cannot_contain_execution_instruction(self):
        x = status(next_action_owner="USER_DECISION_REQUIRED",
                   user_options=["authorize GPU", "read-only audit"],
                   next_agent_instruction="Train now")
        self.assertEqual(x["status"], "INVALID")
        self.assertEqual(status(next_action_owner="USER_DECISION_REQUIRED",
                                user_options=["authorize", "no fit"])["status"],
                         "CONTRACT_OK")

    def test_no_next_action_cannot_invent_work(self):
        self.assertEqual(status(next_action_owner="NO_NEXT_ACTION",
                                next_agent_instruction="write draft")["status"],
                         "INVALID")

    def test_q2_claim_needs_source_pointers_not_only_journal_name(self):
        self.assertEqual(status(q2_decision="Q2_POTENTIAL_SUPPORTED")["status"],
                         "INVALID")
        self.assertEqual(status(q2_decision="Q2_POTENTIAL_SUPPORTED",
                                q2_evidence_ref="run:R1", q2_venue_ref="JCR:source")["status"],
                         "CONTRACT_OK")


if __name__ == "__main__":
    unittest.main()
