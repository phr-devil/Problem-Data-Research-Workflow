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
        p["not_applicable_evidence_ref"] = "synthetic/proof_of_no_algorithm_claim"
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

    def test_empirical_data_acceptance_cannot_be_substituted_by_proof_card(self):
        p = packet("02", "EMPIRICAL")
        del p["deliverable_refs"]["DATA_MANIFEST"]
        del p["deliverable_refs"]["DATA_INSIGHT_CARD"]
        p["deliverable_refs"]["PROOF_EVIDENCE_CARD"] = "synthetic/proof"
        p["deliverable_refs"]["PROOF_OBSERVATION_CARD"] = "synthetic/proof/observation"
        result = review_activity_handoff(p)
        self.assertEqual(result["missing_alternative_deliverable_groups"], [])
        self.assertEqual(result["missing_evidence_path_deliverables"],
                         ["DATA_MANIFEST", "DATA_INSIGHT_CARD"])
        self.assertFalse(result["declared_handoff_complete_not_verified"])

    def test_confirmed_and_unavailable_cannot_be_both_reported(self):
        p = packet("06", "EMPIRICAL")
        p["deliverable_refs"]["CONFIRMATION_UNAVAILABLE"] = "synthetic/unavailable"
        result = review_activity_handoff(p)
        self.assertTrue(result["contradictory_confirmation_outputs"])
        self.assertFalse(result["declared_handoff_complete_not_verified"])

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



def _human_packet(*nodes):
    from core.human_decision_review import CONTRACT as H_CONTRACT
    return {
        "format": "pd-rw-human-review-v1",
        "protocol_version": H_CONTRACT["protocol_version"],
        "target": nodes[-1],
        "decisions": {
            step: {
                "kind": "USER_CONFIRMED",
                "original_user_message_ref": f"synthetic/original/{step}",
                "chosen_option": f"synthetic choice {step}",
                "dimension_decisions": {
                    key: "synthetic scoped decision"
                    for key in H_CONTRACT["steps"][step]["required_dimensions"]
                },
                "evidence_refs": {
                    key: "synthetic/source"
                    for key in H_CONTRACT["steps"][step]["evidence_minimum"]
                },
            }
            for step in nodes
        }
    }


class ActivityEntryAndHumanReviewTests(unittest.TestCase):
    def _entered(self, activity, evidence_path="EMPIRICAL"):
        p = packet(activity, evidence_path)
        checks = CONTRACT["activities"][activity].get("entry_checks", {})
        keys = checks.get("all", []) + checks.get(evidence_path, [])
        p["entry_evidence_refs"] = {key: f"synthetic/{key}" for key in keys}
        return p

    def test_activity_cannot_claim_ready_from_handoff_fields_alone(self):
        p = packet("02")
        r = review_activity_handoff(p)
        self.assertTrue(r["declared_handoff_complete_not_verified"])
        self.assertFalse(r["entry_declarations_complete_not_authenticated"])
        self.assertEqual(r["human_review_declarations_status"], "NOT_CHECKED")
        self.assertFalse(r["declared_activity_ready_not_authenticated"])

    def test_activity02_requires_both_h5_and_data_acceptance(self):
        p = self._entered("02")
        r = review_activity_handoff(p)
        self.assertTrue(r["entry_declarations_complete_not_authenticated"])
        self.assertFalse(r["declared_activity_ready_not_authenticated"])
        p["human_review_packet"] = _human_packet("H1", "H2", "H3", "H4", "H5")
        r = review_activity_handoff(p)
        self.assertEqual(r["human_review_declarations_status"],
                         "DECLARED_COMPLETE_NOT_AUTHENTICATED")
        self.assertTrue(r["declared_activity_ready_not_authenticated"])
        self.assertFalse(r["authorizes_download_fitting_sealed_figures_or_writing"])
        del p["entry_evidence_refs"]["required_files_acceptance_ref"]
        r = review_activity_handoff(p)
        self.assertFalse(r["declared_activity_ready_not_authenticated"])
        self.assertIn("required_files_acceptance_ref",
                      r["missing_entry_evidence_declarations"])

    def test_h5_reference_unbacked_by_declared_human_decision_is_insufficient(self):
        p = self._entered("03")
        p["human_review_packet"] = _human_packet("H1", "H2", "H3", "H4", "H5")
        self.assertEqual(review_activity_handoff(p)["human_review_declarations_missing"], ["H6"])
        self.assertFalse(review_activity_handoff(p)["declared_activity_ready_not_authenticated"])

    def test_nonmethod_scope_has_disposition_not_fake_experiment_pass(self):
        p = self._entered("04", "NON_DATA")
        p["execution_kind"] = "NO_CONTROLLED_EXPERIMENT"
        p["applicability"] = "NOT_APPLICABLE"
        p["not_applicable_reason"] = "proof-only task, no model claim"
        p["not_applicable_evidence_ref"] = "synthetic/nonmethod_rationale"
        p["human_review_applicability"] = {
            "H7": {"status": "NOT_APPLICABLE",
                   "reason": "no new algorithm or major experimental choice",
                   "evidence_ref": "synthetic/no_h7"}
        }
        p["human_review_packet"] = _human_packet("H1", "H2", "H3", "H4", "H5", "H6")
        r = review_activity_handoff(p)
        self.assertTrue(r["declared_non_method_scope_ready_not_authenticated"])
        self.assertFalse(r["declared_handoff_complete_not_verified"])
        self.assertEqual(r["non_method_disposition"], "JUSTIFIED_NOT_APPLICABLE_DECLARED")
        self.assertEqual(r["required_human_review_declarations"], ["H6"])
        self.assertFalse(r["authorizes_download_fitting_sealed_figures_or_writing"])

    def test_method_scope_requires_h7_for_major_mechanism(self):
        p = self._entered("04")
        p["execution_kind"] = "CONTROLLED_EXPERIMENT"
        p["entry_evidence_refs"]["original_execution_permission_ref"] = "synthetic/user/permit"
        p["human_review_packet"] = _human_packet("H1", "H2", "H3", "H4", "H5", "H6")
        r = review_activity_handoff(p)
        self.assertIn("H7", r["human_review_declarations_missing"])
        p["human_review_packet"]["decisions"]["H7"] = _human_packet("H7")["decisions"]["H7"]
        r = review_activity_handoff(p)
        self.assertTrue(r["declared_activity_ready_not_authenticated"])

    def test_confirmation_unavailable_needs_h10_not_fake_h9(self):
        p = self._entered("06")
        p["deliverable_refs"].pop("INDEPENDENT_CONFIRM")
        p["deliverable_refs"]["CONFIRMATION_UNAVAILABLE"] = "synthetic/unavailable"
        p["entry_evidence_refs"]["confirmation_unavailability_basis_ref"] = "synthetic/no_holdout"
        p["human_review_applicability"] = {
            "H9": {"status": "NOT_APPLICABLE",
                   "reason": "no scientifically eligible independent confirmation",
                   "evidence_ref": "synthetic/no_resource"}
        }
        p["human_review_packet"] = _human_packet(
            "H1", "H2", "H3", "H4", "H5", "H6", "H8", "H10")
        r = review_activity_handoff(p)
        self.assertEqual(r["required_human_review_declarations"], ["H10"])
        self.assertTrue(r["declared_activity_ready_not_authenticated"])
        self.assertTrue(r["confirmation_unavailable_declared"])
        self.assertFalse(r["scientific_truth_verified"])

    def test_real_confirmation_requires_h9_and_separate_access_ref(self):
        p = self._entered("06")
        p["human_review_packet"] = _human_packet("H1", "H2", "H3", "H4", "H5", "H6", "H8", "H10")
        r = review_activity_handoff(p)
        self.assertIn("H9", r["human_review_declarations_missing"])
        self.assertIn("original_confirmation_access_permission_ref",
                      r["missing_entry_evidence_declarations"])
        p["human_review_packet"]["decisions"]["H9"] = _human_packet("H9")["decisions"]["H9"]
        p["entry_evidence_refs"]["frozen_confirmation_protocol_ref"] = "synthetic/frozen"
        p["entry_evidence_refs"]["original_confirmation_access_permission_ref"] = "synthetic/permit"
        r = review_activity_handoff(p)
        self.assertTrue(r["declared_activity_ready_not_authenticated"])
        self.assertFalse(r["authorizes_download_fitting_sealed_figures_or_writing"])

if __name__ == "__main__":
    unittest.main()
