"""Deterministic H1-H5 user / H6-H8 agent decision regression.

Declarations are not authentication, real tool permission or Agent behavior.
"""
import unittest
from pathlib import Path

from core.human_decision_review import CONTRACT, review
from core.contracts import review_activity_handoff

ROOT = Path(__file__).resolve().parents[1]


def choice(step, *, agent=False):
    spec = CONTRACT["steps"][step]
    entry = {
        "kind": "AGENT_DECIDED" if agent else "USER_CONFIRMED",
        "dimension_decisions": {key: "scientifically scoped" for key in spec["required_dimensions"]},
        "evidence_refs": {key: "synthetic/source" for key in spec["evidence_minimum"]},
    }
    if agent:
        entry.update(agent_decision_ref=f"synthetic/decision/{step}",
                     h5_scope_ref="synthetic/original-user-H5")
    else:
        entry.update(original_user_message_ref=f"synthetic/original-user-{step}",
                     chosen_option=f"user selection {step}")
    return entry


def packet(target, included):
    return {
        "format": "pd-rw-human-review-v1",
        "protocol_version": CONTRACT["protocol_version"],
        "target": target,
        "decisions": {
            step: choice(step, agent=step in {"H6", "H7", "H8"})
            for step in included
        },
    }


class DevAutonomyContractTests(unittest.TestCase):
    def test_owner_partition_and_protocol_version(self):
        self.assertEqual(CONTRACT["protocol_version"], "pd-rw-human-review-v1.2")
        for step in ("H1", "H2", "H3", "H4", "H5", "H9", "H10"):
            self.assertEqual(CONTRACT["steps"][step]["decision_owner"], "USER")
        for step in ("H6", "H7", "H8"):
            self.assertEqual(CONTRACT["steps"][step]["decision_owner"], "AGENT")

    def test_h6_h7_h8_are_agent_decisions_without_fake_user_grants(self):
        done = ("H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8")
        for step in ("H6", "H7", "H8"):
            with self.subTest(step=step):
                r = review(packet(step, done))
                self.assertTrue(r["can_advance_declarations_only"])
                self.assertEqual(r["target_decision_owner"], "AGENT")
                self.assertFalse(r["target_requires_user_scientific_choice"])
                self.assertIn(step, r["agent_decision_declarations"])
                self.assertFalse(r["allows_download_training_sealed_or_writing"])
        # H7 remains optional for scientific discovery/no new algorithm.
        r = review(packet("H8", ("H1", "H2", "H3", "H4", "H5", "H6", "H8")))
        self.assertTrue(r["can_advance_declarations_only"])

    def test_no_h5_no_agent_forging_or_missing_provenance(self):
        p = packet("H6", ("H1", "H2", "H3", "H4", "H6"))
        r = review(p)
        self.assertFalse(r["can_advance_declarations_only"])
        self.assertIn("H5", r["missing_prerequisites"])
        p = packet("H6", ("H1", "H2", "H3", "H4", "H5", "H6"))
        del p["decisions"]["H6"]["h5_scope_ref"]
        r = review(p)
        self.assertIn("H6", r["malformed_declarations"])
        self.assertFalse(r["can_advance_declarations_only"])
        p = packet("H6", ("H1", "H2", "H3", "H4", "H5", "H6"))
        del p["decisions"]["H6"]["evidence_refs"]["falsifier_and_comparator"]
        r = review(p)
        self.assertIn("H6", r["missing_evidence_refs"])
        self.assertFalse(r["can_advance_declarations_only"])

    def test_agent_cannot_take_h5_h9_h10_user_decisions(self):
        for target in ("H5", "H9", "H10"):
            p = packet(target, ("H1", "H2", "H3", "H4", "H5", "H6", "H8", "H9", "H10"))
            p["decisions"][target] = choice(target, agent=True)
            r = review(p)
            self.assertIn(target, r["malformed_declarations"])
            self.assertFalse(r["can_advance_declarations_only"])
            self.assertTrue(r["target_requires_user_scientific_choice"])

    def test_invalidated_h5_stales_agent_decisions_and_h9(self):
        p = packet("H9", ("H1", "H2", "H3", "H4", "H5", "H6", "H8"))
        p["invalidated_decisions"] = ["H5"]
        r = review(p)
        self.assertFalse(r["can_present_review_declarations_only"])
        for node in ("H5", "H6", "H8"):
            self.assertIn(node, r["missing_prerequisites"])

    def test_legacy_science_decisions_can_be_read_but_not_reclassified(self):
        p = packet("H6", ("H1", "H2", "H3", "H4", "H5", "H6"))
        p["protocol_version"] = "pd-rw-human-review-v1.1"
        self.assertFalse(review(p)["can_advance_declarations_only"])
        p["decisions"]["H6"] = choice("H6", agent=False)
        self.assertTrue(review(p)["can_advance_declarations_only"])

    def test_activity04_accepts_standing_dev_scope_not_human_h7_signoff(self):
        from tests.test_research_activity_handoff import packet as activity_packet
        p = activity_packet("04")
        spec = __import__("json").loads(
            (ROOT / "contracts/research_activity_protocol.v1.json").read_text(encoding="utf-8")
        )["activities"]["04"]
        p["entry_evidence_refs"] = {
            key: "synthetic/source"
            for key in spec["entry_checks"]["all"] + spec["entry_checks"].get("EMPIRICAL", [])
        }
        p["execution_kind"] = "CONTROLLED_EXPERIMENT"
        p["human_review_packet"] = packet(
            "H7", ("H1", "H2", "H3", "H4", "H5", "H6", "H7")
        )
        r = review_activity_handoff(p)
        self.assertIn("dev_execution_scope_ref", r["missing_entry_evidence_declarations"])
        self.assertFalse(r["declared_activity_ready_not_authenticated"])
        p["entry_evidence_refs"]["dev_execution_scope_ref"] = "synthetic/user-H5+legal-DEV+host"
        r = review_activity_handoff(p)
        self.assertEqual(r["human_review_declarations_status"],
                         "DECLARED_COMPLETE_NOT_AUTHENTICATED")
        self.assertTrue(r["declared_activity_ready_not_authenticated"])
        self.assertFalse(r["authorizes_download_fitting_sealed_figures_or_writing"])
        # Historical per-operation permission references retain compatibility.
        del p["entry_evidence_refs"]["dev_execution_scope_ref"]
        p["entry_evidence_refs"]["original_execution_permission_ref"] = "synthetic/old-permit"
        self.assertTrue(review_activity_handoff(p)["declared_activity_ready_not_authenticated"])

    def test_entry_and_science_docs_match_safe_autonomy_scope(self):
        for name in ("WORKFLOW.md", "AGENTS.md", "NEXT_ACTION_POLICY.md",
                     "ALGORITHM_ENGINEERING.md", "EXPERIMENT_LOOP.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("H5", text, name)
            self.assertIn("DEV", text, name)
        workflow = (ROOT / "WORKFLOW.md").read_text(encoding="utf-8")
        self.assertIn("AI_DEV_AUTONOMY", workflow)
        for policy in ("WRITING_GATE.md", "CONFIRMATION.md", "FIGURE_POLICY.md"):
            text = (ROOT / policy).read_text(encoding="utf-8")
            self.assertTrue(any(x in text for x in ("WRITING_LOCKED", "SEALED", "FIGURE_DRAWING_LOCKED")), policy)


if __name__ == "__main__":
    unittest.main()
