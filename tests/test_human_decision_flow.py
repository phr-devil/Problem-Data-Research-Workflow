"""Human review decision chain: structural regression only, never approval."""
import unittest
import json
from pathlib import Path

from core.human_decision_review import DEPENDENCIES, STEPS, dependencies_of, review

ROOT = Path(__file__).resolve().parents[1]


def packet(target="H3", decisions=None):
    return {"format": "pd-rw-human-review-v1", "target": target, "decisions": decisions or {}}


def user(step, choice="selected"):
    return {
        "kind": "USER_CONFIRMED", "original_user_message_ref": f"original-chat-{step}",
        "chosen_option": choice
    }


def delegated(step, scope="choose this option"):
    return {
        "kind": "USER_DELEGATED", "original_user_message_ref": f"original-chat-{step}",
        "delegated_scope": scope
    }


class HumanDecisionFlowTests(unittest.TestCase):
    def test_dependency_map_covers_ten_nodes_and_has_no_cycle(self):
        self.assertEqual(len(STEPS), 10)
        self.assertEqual(set(DEPENDENCIES), set(STEPS))
        for step in STEPS:
            self.assertNotIn(step, dependencies_of(step))
        self.assertNotIn("H7", dependencies_of("H8"))
        self.assertNotIn("H9", dependencies_of("H10"))

    def test_missing_h2_cannot_be_silently_skipped_for_h3(self):
        result = review(packet("H3", {"H1": user("H1")}))
        self.assertEqual(result["result"], "REVIEW_REQUIRED")
        self.assertEqual(result["missing_prerequisites"], ["H2"])
        self.assertFalse(result["allows_download_training_sealed_or_writing"])

    def test_first_stage_requires_h3_and_h4_before_final_h5(self):
        r = review(packet("H5", {"H1": user("H1"), "H2": delegated("H2"),
                                  "H3": user("H3")}))
        self.assertEqual(r["missing_prerequisites"], ["H4"])

    def test_user_can_approve_multiple_and_delegate_specific_scope(self):
        choices = {s: user(s) for s in ("H1", "H3", "H4")}
        choices["H2"] = delegated("H2", "all six sources and compare contribution routes")
        r = review(packet("H5", choices))
        self.assertEqual(r["result"], "DECLARED_DEPENDENCIES_PRESENT_NOT_AUTHENTICATED")
        self.assertTrue(r["requires_original_user_message_review"])
        self.assertFalse(r["allows_download_training_sealed_or_writing"])

    def test_ai_self_approval_or_boolean_flags_not_accepted(self):
        choices = {"H1": {"kind": "USER_CONFIRMED", "chosen_option": "scope"},
                   "H2": {"kind": "USER_DELEGATED", "delegated_scope": "all"}}
        r = review(packet("H3", choices))
        self.assertEqual(r["malformed_declarations"], ["H1", "H2"])
        self.assertEqual(r["missing_prerequisites"], ["H1", "H2"])
        self.assertEqual(r["result"], "REVIEW_REQUIRED")

    def test_h8_can_be_reached_without_algorithm_h7(self):
        choices = {s: user(s) for s in ("H1", "H2", "H3", "H4", "H5", "H6")}
        r = review(packet("H8", choices))
        self.assertEqual(r["missing_prerequisites"], [])

    def test_h10_does_not_pretend_independent_confirmation(self):
        choices = {s: user(s) for s in ("H1", "H2", "H3", "H4", "H5", "H6", "H8")}
        r = review(packet("H10", choices))
        self.assertEqual(r["missing_prerequisites"], [])
        self.assertIn("separate writing gate", r["note"])

    def test_pending_and_unknown_nodes(self):
        r = review(packet("H4", {"H1": user("H1"), "H2": {"kind": "PENDING"}}))
        self.assertEqual(r["missing_prerequisites"], ["H2", "H3"])
        self.assertIn("H2", r["pending_steps"])
        with self.assertRaises(ValueError):
            review(packet("H11"))

    def test_invalidated_d1_blocks_old_final_topic_and_task(self):
        decisions = {s: user(s) for s in ("H1", "H2", "H3", "H4", "H5", "H6")}
        p = packet("H7", decisions)
        self.assertEqual(review(p)["result"], "DECLARED_DEPENDENCIES_PRESENT_NOT_AUTHENTICATED")
        p["invalidated_decisions"] = ["H4"]
        result = review(p)
        self.assertEqual(result["result"], "REVIEW_REQUIRED")
        self.assertEqual(result["missing_prerequisites"], ["H4", "H5", "H6"])
        self.assertEqual(result["stale_declarations"], ["H4", "H5", "H6"])
        self.assertEqual(result["target_blocked_by_reopening"], ["H4"])

    def test_revised_database_does_not_automatically_restore_old_h5(self):
        decisions = {s: user(s) for s in ("H1", "H2", "H3", "H4", "H5", "H6")}
        decisions["H4"] = user("H4", "new D1 after original was rejected")
        p = packet("H6", decisions)
        # H4 is newly settled, but H5 was chosen against the *old* D1:
        # outstanding downstream invalidation must persist until re-reviewed.
        p["invalidated_decisions"] = ["H5"]
        r = review(p)
        self.assertEqual(r["result"], "REVIEW_REQUIRED")
        self.assertEqual(r["missing_prerequisites"], ["H5"])
        self.assertEqual(r["stale_declarations"], ["H5", "H6"])
        self.assertFalse(r["allows_download_training_sealed_or_writing"])

    def test_reopened_target_cannot_be_silently_reapproved(self):
        choices = {s: user(s) for s in ("H1", "H2", "H3", "H4", "H5")}
        p = packet("H5", choices)
        p["invalidated_decisions"] = ["H5"]
        r = review(p)
        self.assertEqual(r["missing_prerequisites"], [])
        self.assertEqual(r["result"], "REVIEW_REQUIRED")
        self.assertEqual(r["target_blocked_by_reopening"], ["H5"])

    def test_invalidated_sibling_does_not_invent_dependency(self):
        choices = {s: user(s) for s in ("H1", "H2", "H3", "H4", "H5", "H6", "H8")}
        p = packet("H10", choices)
        p["invalidated_decisions"] = ["H7"]  # optional algorithm route
        r = review(p)
        self.assertEqual(r["missing_prerequisites"], [])
        self.assertEqual(r["result"], "DECLARED_DEPENDENCIES_PRESENT_NOT_AUTHENTICATED")
        self.assertEqual(r["stale_declarations"], [])

    def test_reopening_metadata_must_be_valid(self):
        for value in ("H4", ["H4", "H4"], ["H11"], [None]):
            with self.subTest(invalidated=value):
                p = packet("H5", {"H1": user("H1")})
                p["invalidated_decisions"] = value
                with self.assertRaises(ValueError):
                    review(p)

    def test_prominent_entrypoint_and_heading_namespace(self):
        read = lambda p: (ROOT / p).read_text(encoding="utf-8")
        for p in ("README.md", "START.md", "AGENTS.md", "WORKFLOW.md"):
            with self.subTest(file=p):
                self.assertIn("USER_DEEP_PARTICIPATION", read(p))
                self.assertIn("H4", read(p))
        homepage = read("README.md")
        self.assertNotIn("方向确定后立即自主选库", homepage)
        self.assertNotIn("无需再次让用户选择数据库", homepage)
        self.assertIn("PROOF_PATH", homepage)
        for p in ("WORKFLOW.md", "AGENTS.md", "templates/PAPER_BLUEPRINT.md"):
            with self.subTest(namespace=p):
                self.assertIn("REVIEW:H", read(p))
                self.assertIn("HEADING:H", read(p))
        self.assertIn("invalidated_decisions", read("core/README.md"))

    def test_documents_have_human_choice_at_each_owner(self):
        rules = {
            "WORKFLOW.md": ("USER_DEEP_PARTICIPATION", "H1", "H10", "HUMAN_REVIEW_PENDING"),
            "START.md": ("USER_DEEP_PARTICIPATION", "H1–H5", "PREFERRED"),
            "SEARCH_DISCOVERY.md": ("H3", "H5", "BREADTH_SCAN"),
            "DATA_DISCOVERY.md": ("H4", "H5", "PRE_DOWNLOAD_SCIENCE_FIT"),
            "HIGH_VALUE_RESEARCH_DESIGN.md": ("H2", "H8"),
            "TASK_EXPLORATION.md": ("H6", "DATA_ACQUIRED_VERIFIED"),
            "ALGORITHM_ENGINEERING.md": ("H7", "PROBE_CANDIDATE"),
            "EXPERIMENT_LOOP.md": ("H7", "SEALED"),
            "PAPER_FIRST.md": ("H8", "Q2_POTENTIAL_SUPPORTED"),
            "CONFIRMATION.md": ("H9", "CONFIRMATION_UNAVAILABLE"),
            "WRITING_GATE.md": ("H10", "WRITING_LOCKED"),
            "NEXT_ACTION_POLICY.md": ("USER_DECISION_REQUIRED", "USER_DEEP_PARTICIPATION"),
            "templates/RESEARCH_RECORD.md": ("H_ID", "ORIGINAL_MESSAGE_REF"),
            "templates/STATE.md": ("HUMAN_REVIEW_CURRENT", "HUMAN_DECISION_REF"),
        }
        for file, required in rules.items():
            doc = (ROOT / file).read_text(encoding="utf-8")
            for marker in required:
                with self.subTest(file=file, marker=marker):
                    self.assertIn(marker, doc)

    def test_explicit_conflict_phrases_removed(self):
        discovery = (ROOT / "DATA_DISCOVERY.md").read_text(encoding="utf-8")
        self.assertNotIn("不新增人为筛库确认轮次", discovery)
        self.assertNotIn("自主选库不构成下载", discovery)
        self.assertNotIn("不等待用户确认“选哪个库”", discovery)
        search = (ROOT / "SEARCH_DISCOVERY.md").read_text(encoding="utf-8")
        self.assertNotIn("不增加用户轮次", search)



# The unified policy is a structural contract; authentic user messages, scientific
# quality and action authorization cannot be certified by any synthetic packet.
from core.human_decision_review import CONTRACT


def filled_review(step, delegated_choice=False, proof=False):
    spec = CONTRACT["steps"][step]
    entry = {
        "kind": "USER_DELEGATED" if delegated_choice else "USER_CONFIRMED",
        "original_user_message_ref": "synthetic-message-" + step,
        "dimension_decisions": {name: "explicit scoped choice" for name in spec["required_dimensions"]},
        "evidence_refs": {name: "synthetic-evidence-" + name for name in spec["evidence_minimum"]},
    }
    if delegated_choice:
        entry["delegated_scope"] = "choose only H4 dataset under stated costs"
    else:
        entry["chosen_option"] = "explicit synthetic H step choice"
    if proof and step == "H4":
        entry["dimension_decisions"]["dataset_or_proof_path"] = "PROOF_PATH mathematical demonstration"
    return entry


def strict_packet(target, completed, *, delegated_h4=False, proof=False):
    return {
        "format": "pd-rw-human-review-v1",
        "protocol_version": CONTRACT["protocol_version"],
        "target": target,
        "decisions": {
            step: filled_review(step, delegated_choice=(step == "H4" and delegated_h4), proof=proof)
            for step in completed
        },
    }


class UnifiedInteractionProtocolTests(unittest.TestCase):
    def test_single_machine_contract_and_fixed_definitions(self):
        self.assertEqual(CONTRACT["owner"], "WORKFLOW.md")
        self.assertEqual(CONTRACT["new_project_sequence"], ["H1", "H2", "H3", "H4", "H5"])
        self.assertEqual(len(CONTRACT["steps"]), 10)
        self.assertEqual(set(CONTRACT["steps"]), set(STEPS))
        self.assertEqual(len(CONTRACT["vocabularies"]["question_sources"]), 6)
        self.assertEqual(len(CONTRACT["vocabularies"]["contribution_routes"]), 5)
        for name in STEPS:
            spec = CONTRACT["steps"][name]
            self.assertEqual(tuple(spec["prerequisites"]), DEPENDENCIES[name])
            self.assertTrue(spec["required_dimensions"])
            self.assertTrue(spec["evidence_minimum"])
            self.assertTrue(spec["name"])
        self.assertEqual(CONTRACT["steps"]["H2"]["required_dimensions"],
                         ["question_sources", "contribution_routes", "search_focus"])
        self.assertIn("dataset_or_proof_path", CONTRACT["steps"]["H4"]["required_dimensions"])
        self.assertEqual(dependencies_of("H5"), {"H1", "H2", "H3", "H4"})

    def test_malformed_or_partial_h2_cannot_complete_review(self):
        p = strict_packet("H3", ("H1", "H2"))
        del p["decisions"]["H2"]["dimension_decisions"]["contribution_routes"]
        r = review(p)
        self.assertEqual(r["missing_required_dimensions"]["H2"], ["contribution_routes"])
        self.assertIn("H2", r["missing_prerequisites"])
        self.assertFalse(r["can_present_review_declarations_only"])
        self.assertFalse(r["can_advance_declarations_only"])
        self.assertEqual(r["next_review"], "H2")

    def test_h2_unknown_does_not_count_as_choice(self):
        p = strict_packet("H3", ("H1", "H2"))
        p["decisions"]["H2"]["dimension_decisions"]["contribution_routes"] = "UNKNOWN"
        self.assertEqual(review(p)["next_review"], "H2")

    def test_incomplete_evidence_blocks_declared_completion(self):
        p = strict_packet("H5", ("H1", "H2", "H3", "H4"))
        del p["decisions"]["H4"]["evidence_refs"]["source_and_feasibility_comparison"]
        r = review(p)
        self.assertEqual(r["missing_evidence_refs"]["H4"], ["source_and_feasibility_comparison"])
        self.assertIn("H4", r["missing_prerequisites"])

    def test_can_present_does_not_mean_user_has_chosen(self):
        p = strict_packet("H5", ("H1", "H2", "H3", "H4"))
        r = review(p)
        self.assertTrue(r["can_present_review_declarations_only"])
        self.assertFalse(r["can_advance_declarations_only"])
        self.assertEqual(r["next_review"], "H5")
        self.assertFalse(r["allows_download_training_sealed_or_writing"])
        p["decisions"]["H5"] = filled_review("H5")
        r = review(p)
        self.assertTrue(r["can_advance_declarations_only"])
        self.assertEqual(r["next_review"], "H6")
        self.assertTrue(r["requires_original_user_message_review"])

    def test_cross_project_synthetic_cases_enforce_sequence(self):
        cases = json.loads(
            (ROOT / "evals" / "cases" / "human_review_sequences.json").read_text(encoding="utf-8")
        )
        self.assertTrue(cases["synthetic_only"])
        self.assertGreaterEqual(len(cases["cases"]), 10)
        domains = set()
        for item in cases["cases"]:
            domain, mode, target = item["domain"], item["mode"], item["target"]
            domains.add(domain)
            completed = {
                "new_full": ("H1", "H2", "H3", "H4"),
                "partial_h2": ("H1", "H2"),
                "missing_h4": ("H1", "H2", "H3"),
                "h1h2": ("H1", "H2"),
                "delegated_h4": ("H1", "H2", "H3", "H4"),
                "proof_path": ("H1", "H2", "H3", "H4"),
                "reopened_h4": ("H1", "H2", "H3", "H4", "H5", "H6"),
                "legacy": ("H1", "H2", "H3", "H4", "H5"),
                "full_h5": ("H1", "H2", "H3", "H4", "H5"),
            }[mode]
            if mode == "legacy":
                p = packet(target, {s: user(s) for s in completed})
            else:
                p = strict_packet(target, completed, delegated_h4=(mode == "delegated_h4"),
                                  proof=(mode == "proof_path"))
            if mode == "partial_h2":
                del p["decisions"]["H2"]["dimension_decisions"]["contribution_routes"]
            if mode == "reopened_h4":
                p["invalidated_decisions"] = ["H4"]
            r = review(p)
            with self.subTest(case=item["id"], domain=domain):
                self.assertEqual(r["next_review"], item["expected_next"])
                self.assertEqual(r["can_present_review_declarations_only"],
                                 item["expected_can_present"])
                self.assertEqual(r["can_advance_declarations_only"],
                                 item["expected_can_advance"])
                self.assertFalse(r["allows_download_training_sealed_or_writing"])
        self.assertGreaterEqual(len(domains), 4)

    def test_wrong_version_is_rejected_and_legacy_is_supported(self):
        p = strict_packet("H3", ("H1", "H2"))
        p["protocol_version"] = "invented-version"
        with self.assertRaises(ValueError):
            review(p)
        r = review(packet("H3", {"H1": user("H1"), "H2": user("H2")}))
        self.assertEqual(r["protocol_version"], "legacy_unverified")
        self.assertTrue(r["can_present_review_declarations_only"])

    def test_consistency_between_canonical_policy_and_entrypoints(self):
        doc = lambda name: (ROOT / name).read_text(encoding="utf-8")
        for name in ("WORKFLOW.md", "START.md", "AGENTS.md",
                     "NEXT_ACTION_POLICY.md", "README.md"):
            with self.subTest(name=name):
                self.assertIn("human_review_protocol.v1.json", doc(name))
        for name, markers in {
            "SEARCH_DISCOVERY.md": ["H2", "H3", "question_sources", "contribution_routes"],
            "HIGH_VALUE_RESEARCH_DESIGN.md": ["H2", "contribution_routes"],
            "DATA_DISCOVERY.md": ["H4", "dataset_or_proof_path"],
            "templates/RESEARCH_RECORD.md": ["protocol_version", "current_review"],
            "templates/STATE.md": ["protocol_version", "HUMAN_REVIEW_CURRENT"],
            "REPLAY_PROTOCOL.md": ["human_review_sequences.json"],
        }.items():
            with self.subTest(name=name):
                for marker in markers:
                    self.assertIn(marker, doc(name))

if __name__ == "__main__":
    unittest.main()
