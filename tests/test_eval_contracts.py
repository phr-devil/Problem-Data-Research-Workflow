"""Offline adversarial tests for opt-in PD-RW agent evaluation; no agent is run."""
import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from evals.benchmark import (
    CASES, CATEGORIES, blind_cases, compare_runs, load_cases, score_run, suite_hash,
)

ROOT = Path(__file__).resolve().parents[1]


def sample_run(cases, name="before", core_only=False):
    return {
        "format": "pdrw-eval-agent-run-v1", "run_id": name,
        "workflow_ref": "sha-old" if name == "before" else "sha-new",
        "suite_hash": suite_hash(cases), "model_id": "synthetic-model",
        "model_config_id": "test-settings-1", "tool_profile": "sandbox-simulated",
        "budget_id": "same-cap",
        "responses": [
            {"case_id": c["id"], "selected_choice": c["expected"]["acceptable_choices"][0],
             "noticed_risks": c["expected"]["must_notice"]}
            for c in cases if not core_only or c["core"]
        ],
    }


def sample_observations(cases, run, core_only=False):
    return {
        "format": "pdrw-eval-observations-v1",
        "run_id": run["run_id"], "suite_hash": suite_hash(cases),
        "capture_source": "EXTERNAL_INSTRUMENTED",
        "cases": [
            {"case_id": c["id"], "events": [{"type": "READ_FILE", "resource_class": "SYNTHETIC"}],
             "checks": {"task_complete": True, "evidence_consistent": True},
             "usage": {"input_tokens": 250, "output_tokens": 100,
                       "tool_calls": 1, "wall_ms": 3500}}
            for c in cases if not core_only or c["core"]
        ],
    }


class EvaluationContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = load_cases()

    def test_complete_deterministic_suite_and_preserved_legacy(self):
        self.assertEqual(len(self.cases), 16)
        self.assertEqual(sum(c["core"] for c in self.cases), 6)
        self.assertEqual({c["category"] for c in self.cases}, set(CATEGORIES))
        old = json.loads((ROOT / "SCENARIOS.json").read_text(encoding="utf-8"))
        self.assertEqual(len(old["cases"]), 60)
        self.assertIn("D10-60", {c["id"] for c in old["cases"]})
        self.assertTrue((ROOT / "chapter10_replay.py").exists())

    def test_blind_hides_answers_for_full_and_core_sets(self):
        for core, count in ((False, 16), (True, 6)):
            r = blind_cases(self.cases, core_only=core)
            self.assertEqual(len(r["cases"]), count)
            txt = json.dumps(r)
            self.assertNotIn("acceptable_choices", txt)
            self.assertNotIn("must_notice", txt)
            self.assertNotIn("qualitative_focus", txt)
            self.assertNotIn("legacy_ref", txt)
            self.assertNotIn("expert", txt)

    def test_wrong_choice_is_not_automatically_agent_success(self):
        run = sample_run(self.cases)
        complete = score_run(self.cases, run)
        self.assertEqual(complete["reference_matches"], 16)
        self.assertEqual(complete["verdict"], "NOT_MEASURED")
        self.assertIsNone(complete["total_tokens_observed"])
        run["responses"][0]["selected_choice"] = "tune"
        self.assertEqual(score_run(self.cases, run)["reference_matches"], 15)

    def test_no_self_reported_permission_and_no_fake_capture(self):
        run = sample_run(self.cases)
        run["authorization_verified"] = True
        self.assertEqual(score_run(self.cases, run)["verdict"], "NOT_MEASURED")
        obs = sample_observations(self.cases, run)
        obs["capture_source"] = "AGENT_SELF_REPORT"
        with self.assertRaisesRegex(ValueError, "externally"):
            score_run(self.cases, run, obs)

    def test_real_trace_forbidden_actions_fail_closed(self):
        run = sample_run(self.cases)
        obs = sample_observations(self.cases, run)
        item = next(x for x in obs["cases"] if x["case_id"] == "EV-P02")
        item["events"] = [{"type": "READ_FILE", "resource_class": "SEALED"}]
        result = score_run(self.cases, run, obs)
        self.assertEqual(result["verdict"], "BLOCKED")
        self.assertEqual(next(x for x in result["cases"] if x["case_id"] == "EV-P02")[
            "observed_permission_boundary"], "FAIL")
        item["events"] = [{"type": "READ_SEALED", "resource_class": "SEALED"}]
        self.assertEqual(score_run(self.cases, run, obs)["verdict"], "BLOCKED")
        item["events"] = [{"type": "READ_FILE", "resource_class": "SYNTHETIC"}]
        item["checks"]["evidence_consistent"] = False
        self.assertEqual(score_run(self.cases, run, obs)["verdict"], "BLOCKED")

    def test_partial_observations_remain_not_measured(self):
        run = sample_run(self.cases)
        obs = sample_observations(self.cases, run)
        obs["cases"].pop()
        result = score_run(self.cases, run, obs)
        self.assertEqual(result["verdict"], "NOT_MEASURED")
        self.assertIsNone(result["total_tokens_observed"])
        self.assertEqual(result["observation_coverage"], 15)

    def test_complete_synthetic_observations_never_certify_science(self):
        run = sample_run(self.cases)
        obs = sample_observations(self.cases, run)
        result = score_run(self.cases, run, obs)
        self.assertEqual(result["verdict"], "RECORDED_NOT_CERTIFIED")
        self.assertEqual(result["total_tokens_observed"], 16 * 350)
        self.assertEqual(result["independent_scientific_validity"], "NOT_CERTIFIED")
        self.assertEqual(result["real_agent_improvement"], "NOT_MEASURED")

    def test_compare_mismatched_settings_or_missing_logs(self):
        before, after = sample_run(self.cases), sample_run(self.cases, "after")
        b, a = sample_observations(self.cases, before), sample_observations(self.cases, after)
        self.assertEqual(compare_runs(self.cases, before, after, None, None)["status"],
                         "COMPARISON_NOT_MEASURED")
        after["model_id"] = "other-model"
        self.assertEqual(compare_runs(self.cases, before, after, b, a)["status"],
                         "INCOMPARABLE")
        after["model_id"] = before["model_id"]
        result = compare_runs(self.cases, before, after, b, a)
        self.assertEqual(result["status"], "DESCRIPTIVE_COMPARISON_ONLY")
        self.assertEqual(result["baseline_tokens"], result["candidate_tokens"])
        a["cases"][0]["events"].append({"type": "DOWNLOAD"})
        self.assertEqual(compare_runs(self.cases, before, after, b, a)["status"],
                         "COMPARISON_NOT_MEASURED")

    def test_resource_class_is_required_and_cannot_bypass_holdout(self):
        run = sample_run(self.cases)
        obs = sample_observations(self.cases, run)
        obs["cases"][0]["events"][0]["resource_class"] = "sealed"
        with self.assertRaisesRegex(ValueError, "resource_class"):
            score_run(self.cases, run, obs)
        obs["cases"][0]["events"][0].pop("resource_class")
        with self.assertRaisesRegex(ValueError, "resource_class"):
            score_run(self.cases, run, obs)

    def test_rubric_weights_remain_review_only_and_sum_to_100(self):
        rubric = json.loads((ROOT / "evals/rubrics.json").read_text(encoding="utf-8"))
        self.assertEqual(sum(rubric["weights"].values()), 100)
        self.assertIn("scientific_creativity", rubric["reviewer_required_for"])
        self.assertIn("permission_boundary", rubric["hard_gates"])

    def test_untrusted_bad_telemetry_and_duplicate_ids_rejected(self):
        run = sample_run(self.cases)
        run["responses"].append(copy.deepcopy(run["responses"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            score_run(self.cases, run)
        run["responses"].pop()
        obs = sample_observations(self.cases, run)
        obs["cases"][0]["usage"]["input_tokens"] = True
        with self.assertRaisesRegex(ValueError, "integer telemetry"):
            score_run(self.cases, run, obs)

    def test_case_mutation_and_duplicate_or_invalid_effect_rejected(self):
        with TemporaryDirectory() as tmp:
            dst = Path(tmp)
            for p in CASES.glob("*.json"):
                (dst / p.name).write_bytes(p.read_bytes())
            first = dst / "research.json"
            obj = json.loads(first.read_text(encoding="utf-8"))
            obj["cases"][1]["id"] = obj["cases"][0]["id"]
            first.write_text(json.dumps(obj), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                load_cases(dst)
            obj["cases"][1]["id"] = "EV-R02"
            obj["cases"][1]["permission_context"]["allowed_effects"] = ["ARBITRARY_EXTERNAL_ACT"]
            first.write_text(json.dumps(obj), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "synthetic effects"):
                load_cases(dst)

    def test_no_new_authorization_gate_or_rendering(self):
        text = (ROOT / "evals/EVALUATION_POLICY.md").read_text(encoding="utf-8")
        self.assertIn("非科研活动或审批", text)
        self.assertIn("NOT_MEASURED", text)
        self.assertIn("真实图像", text)
        self.assertIn("授权", (ROOT / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertIn("WRITING_LOCKED", (ROOT / "WRITING_GATE.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
