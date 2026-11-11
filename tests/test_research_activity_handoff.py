"""Six-activity handoff structure regression. All fixtures are synthetic.

This suite never authenticates scientific observations, original user grants,
downloads, fits models, opens SEALED, produces figures or writes manuscripts.
"""
import json
import unittest
from pathlib import Path

from core.contracts import ContractError, review_activity_handoff

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads(
    (ROOT / "contracts" / "research_activity_protocol.v1.json").read_text(encoding="utf-8")
)


def packet(activity, evidence_path="EMPIRICAL"):
    spec = CONTRACT["activities"][activity]
    deliverables = {
        name: f"synthetic/{activity}/{name}"
        for name in spec["required_deliverables"]
    }
    for alternatives in spec["one_of_deliverables"]:
        chosen = alternatives[-1] if evidence_path == "NON_DATA" else alternatives[0]
        deliverables[chosen] = f"synthetic/{activity}/{chosen}"
    return {
        "format": "pd-rw-activity-handoff-v1",
        "contract_version": CONTRACT["contract_version"],
        "activity_id": activity,
        "evidence_path": evidence_path,
        "evidence": {
            item["key"]: {"status": "REPORTED", "ref": f"synthetic/{activity}/{item['key']}"}
            for item in spec["mandatory_evidence"]
        },
        "deliverable_refs": deliverables,
    }


class ResearchActivityHandoffTests(unittest.TestCase):
    def test_six_stable_activities_without_new_research_gate(self):
        self.assertEqual(CONTRACT["research_flow"], ["01", "02", "03", "04", "05", "06"])
        self.assertEqual(set(CONTRACT["activities"]), set(CONTRACT["research_flow"]))
        self.assertEqual(CONTRACT["allowed_parallel_pairs"], [["04", "05"]])
        self.assertEqual(CONTRACT["activities"]["04"]["allowed_parallel_activities"], ["05"])
        self.assertEqual(CONTRACT["activities"]["05"]["allowed_parallel_activities"], ["04"])
        for activity, spec in CONTRACT["activities"].items():
            with self.subTest(activity=activity):
                for key in ("entry_requirements", "mandatory_evidence", "required_deliverables",
                            "one_of_deliverables", "human_review", "allowed_parallel_activities",
                            "reopen_triggers", "alternative_evidence_paths"):
                    self.assertIn(key, spec)
                self.assertTrue(spec["entry_requirements"])
                self.assertTrue(spec["reopen_triggers"])

    def test_declared_complete_never_authenticates_or_grants_execution(self):
        for activity in CONTRACT["research_flow"]:
            for path in ("EMPIRICAL", "NON_DATA"):
                with self.subTest(activity=activity, path=path):
                    result = review_activity_handoff(packet(activity, path))
                    self.assertTrue(result["declared_handoff_complete_not_verified"])
                    self.assertFalse(result["scientific_truth_verified"])
                    self.assertTrue(result["real_evidence_and_user_message_authentication_required"])
                    self.assertFalse(result["authorizes_download_fitting_sealed_figures_or_writing"])

    def test_missing_critical_evidence_blocks_handoff_even_if_other_fields_complete(self):
        p = packet("02")
        del p["evidence"]["label_truth_or_theorem_scope"]
        result = review_activity_handoff(p)
        self.assertIn("label_truth_or_theorem_scope", result["missing_evidence_declarations"])
        self.assertFalse(result["declared_handoff_complete_not_verified"])

    def test_unknown_or_exploratory_critical_evidence_cannot_be_promoted(self):
        for state in ("UNKNOWN", "NOT_RUN", "INVALID", "STALE", "EXPLORATORY"):
            with self.subTest(state=state):
                p = packet("03")
                key = "independent_evaluation_contract"
                p["evidence"][key] = {"status": state}
                if state == "EXPLORATORY":
                    p["evidence"][key]["ref"] = "synthetic/exploratory"
                result = review_activity_handoff(p)
                self.assertIn(key, result["unresolved_critical_evidence"])
                self.assertFalse(result["declared_handoff_complete_not_verified"])

    def test_honest_no_insight_is_reported_not_fabricated_scientific_evidence(self):
        p = packet("02")
        key = "observed_phenomenon_or_no_reliable_insight"
        p["evidence"][key] = {"status": "UNKNOWN", "note": "NO_RELIABLE_INSIGHT_YET"}
        result = review_activity_handoff(p)
        self.assertIn(key, result["documented_gaps"])
        self.assertNotIn(key, result["unresolved_critical_evidence"])
        self.assertTrue(result["declared_handoff_complete_not_verified"])

    def test_non_data_research_does_not_require_fake_dataset(self):
        p = packet("02", "NON_DATA")
        self.assertIn("PROOF_EVIDENCE_CARD", p["deliverable_refs"])
        self.assertNotIn("DATA_MANIFEST", p["deliverable_refs"])
        self.assertTrue(review_activity_handoff(p)["declared_handoff_complete_not_verified"])

    def test_method_branch_may_be_inapplicable_without_claiming_experiment(self):
        p = packet("04", "NON_DATA")
        p["applicability"] = "NOT_APPLICABLE"
        p["not_applicable_reason"] = "pure conceptual review, no method claim"
        r = review_activity_handoff(p)
        self.assertTrue(r["justified_non_method_skip_declared"])
        self.assertFalse(r["declared_handoff_complete_not_verified"])
        p["not_applicable_reason"] = ""
        with self.assertRaises(ContractError):
            review_activity_handoff(p)
        p = packet("03")
        p["applicability"] = "NOT_APPLICABLE"
        p["not_applicable_reason"] = "not allowed to skip core task"
        with self.assertRaises(ContractError):
            review_activity_handoff(p)

    def test_confirmation_unavailable_is_not_confirmed(self):
        p = packet("06", "NON_DATA")
        self.assertIn("CONFIRMATION_UNAVAILABLE", p["deliverable_refs"])
        result = review_activity_handoff(p)
        self.assertTrue(result["confirmation_unavailable_declared"])
        self.assertFalse(result["scientific_truth_verified"])
        self.assertIn("H10", result["human_review_nodes"])

    def test_malformed_provenance_and_missing_artifact_are_not_accepted(self):
        p = packet("01")
        p["evidence"]["named_nearest_neighbor_and_falsifier"]["ref"] = ""
        p["deliverable_refs"]["SEARCH_HANDOFF"] = ""
        result = review_activity_handoff(p)
        self.assertIn("named_nearest_neighbor_and_falsifier", result["malformed_evidence_declarations"])
        self.assertIn("SEARCH_HANDOFF", result["missing_deliverables"])
        self.assertFalse(result["declared_handoff_complete_not_verified"])

    def test_no_scientific_route_is_prescribed_by_handoff_contract(self):
        a4 = CONTRACT["activities"]["04"]
        self.assertNotIn("algorithm_name", a4)
        self.assertNotIn("fixed_experiment_count", a4)
        self.assertEqual(a4["human_review"], ["H7"])
        self.assertEqual(CONTRACT["activities"]["03"]["human_review"], ["H6"])
        self.assertEqual(CONTRACT["activities"]["05"]["human_review"], ["H8"])
        self.assertEqual(CONTRACT["activities"]["06"]["human_review"], ["H9", "H10"])

    def test_documents_route_to_the_single_activity_contract(self):
        files = ("WORKFLOW.md", "AGENTS.md", "START.md", "NEXT_ACTION_POLICY.md",
                 "DATA_DISCOVERY.md", "DATA_INSIGHT.md", "TASK_EXPLORATION.md",
                 "EXPERIMENT_LOOP.md", "PAPER_FIRST.md", "CONFIRMATION.md",
                 "templates/STATE.md", "templates/RESEARCH_RECORD.md")
        for path in files:
            with self.subTest(file=path):
                self.assertIn("research_activity_protocol.v1.json",
                              (ROOT / path).read_text(encoding="utf-8"))
        policy = (ROOT / "FIGURE_POLICY.md").read_text(encoding="utf-8")
        self.assertIn("FIGURE_DRAWING_LOCKED", policy)
        self.assertIn("WRITING_LOCKED", (ROOT / "WRITING_GATE.md").read_text(encoding="utf-8"))

    def test_invalid_input_is_rejected(self):
        for field, value in (("format", "wrong"), ("activity_id", "07"),
                             ("evidence_path", "FAKE"), ("contract_version", "stale")):
            with self.subTest(field=field):
                p = packet("01")
                p[field] = value
                with self.assertRaises(ContractError):
                    review_activity_handoff(p)


if __name__ == "__main__":
    unittest.main()
