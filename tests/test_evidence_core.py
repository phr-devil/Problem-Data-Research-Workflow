"""Executable structural guarantees; not evidence of research effectiveness."""
import json
import tempfile
import unittest
from pathlib import Path

from core.comparison import compare_runs
from core.contracts import ContractError, validate_claim, validate_run
from core.state import initialize, record_event, recover, status

def run_record(run_id="r1", *, split="dev", task_id="task1"):
    obj = {"run_id": run_id, "task_id": task_id, "protocol_id": "p1",
           "dataset_version": "d1", "evaluator_version": "e1",
           "group_split": "groups1", "sample_ids_hash": "hash1",
           "legal_inputs": ["sensor"], "split": split, "status": "VALID",
           "metrics": {"macro_f1": 0.6},
           "artifact_refs": {"metrics": "metrics.json", "predictions": "pred.csv",
                             "code": "model.py"}, "budget_basis": "cpu_1h"}
    if split == "sealed":
        obj.update({"frozen_protocol_ref": "frozen-v1", "authorization_ref": "user-ref"})
    return obj

class ContractTests(unittest.TestCase):
    def test_valid_and_bad_run(self):
        validate_run(run_record())
        obj = run_record()
        del obj["sample_ids_hash"]
        with self.assertRaises(ContractError):
            validate_run(obj)
        with self.assertRaisesRegex(ContractError, "Run records are empirical"):
            validate_run(dict(run_record(), evidence_path="NON_DATA"))

    def test_claim_evidence_required(self):
        bad = {"claim_id":"c1","task_id":"task1","claim_text":"new mechanism",
               "status":"SUPPORTED","evidence_run_ids":[],"artifact_refs":[]}
        with self.assertRaises(ContractError):
            validate_claim(bad)

    def test_non_data_claim_path_needs_bounded_real_evidence(self):
        proof = {
            "claim_id": "th1", "task_id": "theory_task",
            "claim_text": "Bounded theorem", "status": "SUPPORTED",
            "evidence_path": "NON_DATA", "evidence_type": "THEORETICAL_PROOF",
            "claim_scope": "Under explicitly named assumptions",
            "assumptions_ref": "assumptions.md",
            "strongest_alternative": "different assumptions",
            "evidence_refs": ["proof.md"], "artifact_refs": ["proof.md"],
        }
        self.assertEqual(validate_claim(proof)["evidence_path"], "NON_DATA")
        for missing in ("evidence_refs", "assumptions_ref", "claim_scope", "evidence_type"):
            with self.subTest(missing=missing):
                invalid = dict(proof)
                invalid.pop(missing)
                with self.assertRaises(ContractError):
                    validate_claim(invalid)
        initial = dict(proof, status="HYPOTHESIZED")
        initial.pop("assumptions_ref")
        self.assertEqual(validate_claim(initial)["status"], "HYPOTHESIZED")
        improper = dict(proof, evidence_run_ids=["fake_run"])
        with self.assertRaisesRegex(ContractError, "may not disguise"):
            validate_claim(improper)
        mixed = dict(proof, evidence_path="MIXED")
        with self.assertRaises(ContractError):
            validate_claim(mixed)

    def test_non_data_confirmation_is_not_empirical_generalization(self):
        base = {
            "claim_id": "th1", "task_id": "t1",
            "claim_text": "Domain bounded result", "status": "CONFIRMED",
            "evidence_path": "NON_DATA", "evidence_type": "SIMULATION",
            "claim_scope": "Only parameterized simulation conditions",
            "assumptions_ref": "assumptions.md", "strongest_alternative": "domain shift",
            "evidence_refs": ["sim_report.md"], "artifact_refs": ["sim_report.md"],
            "independent_validation_refs": ["independent_sim.md"],
            "confirmation_protocol_ref": "frozen_protocol_v1",
            "confirmation_scope": "SIMULATION_DOMAIN_ONLY",
            "independence_limit": "shared simulator assumptions",
        }
        validate_claim(base)
        with self.assertRaises(ContractError):
            validate_claim(dict(base, confirmation_scope="EMPIRICAL_GENERALIZATION"))
        with self.assertRaises(ContractError):
            validate_claim(dict(base, independent_validation_refs=[]))
        with self.assertRaisesRegex(ContractError, "separate artifact"):
            validate_claim(dict(base, independent_validation_refs=["sim_report.md"]))
        with self.assertRaises(ContractError):
            validate_claim(dict(base, evidence_type="AUDITED_MECHANISM",
                                confirmation_scope="EMPIRICAL_GENERALIZATION"))
        theorem = dict(base, evidence_type="THEORETICAL_PROOF",
                       confirmation_scope="THEOREM_SCOPE_ONLY")
        validate_claim(theorem)

    def test_comparison_rejects_sealed(self):
        with self.assertRaisesRegex(ContractError, "sealed"):
            compare_runs(run_record(), run_record("r2", split="sealed"), "macro_f1")

    def test_comparison_rejects_protocol_mismatch(self):
        b = run_record("r2")
        b["protocol_id"] = "p2"
        with self.assertRaisesRegex(ContractError, "NOT_COMPARABLE"):
            compare_runs(run_record(), b, "macro_f1")

    def test_missing_budget_needs_review(self):
        a, b = run_record(), run_record("r2")
        a.pop("budget_basis")
        b.pop("budget_basis")
        self.assertEqual(compare_runs(a, b, "macro_f1")["comparison_status"], "BUDGET_REVIEW_REQUIRED")

    def test_budget_mismatch_needs_review(self):
        b = run_record("r2")
        b["budget_basis"] = "gpu_8h"
        result = compare_runs(run_record(), b, "macro_f1")
        self.assertEqual(result["comparison_status"], "BUDGET_REVIEW_REQUIRED")

class StateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        initialize(self.root, "demo")
        for name in ("metrics.json", "pred.csv", "model.py"):
            (self.root / name).write_text("test content", encoding="utf-8")

    def artifact(self, path="r1.json", **changes):
        obj = run_record()
        obj.update(changes)
        (self.root / path).write_text(json.dumps(obj), encoding="utf-8")
        return path

    def test_note_does_not_advance_valid_run(self):
        record_event(self.root, "note", note="Hypothesis only")
        self.assertEqual(status(self.root)["evidence_count"], 0)
        self.assertIsNone(status(self.root)["latest_valid_run_id"])

    def test_valid_run_is_attributed(self):
        path = self.artifact()
        record_event(self.root, "run", artifact=path)
        s = status(self.root)
        self.assertEqual(s["latest_valid_run_id"], "r1")
        self.assertEqual(s["evidence_count"], 1)

    def test_missing_artifact_cannot_advance(self):
        with self.assertRaises(ContractError):
            record_event(self.root, "run", artifact="not-present.json")
        self.assertEqual(status(self.root)["evidence_count"], 0)

    def test_tampering_is_detected(self):
        path = self.artifact()
        record_event(self.root, "run", artifact=path)
        (self.root / path).write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(ContractError, "fingerprint"):
            status(self.root)

    def test_recover_stale_index_after_event_append(self):
        path = self.artifact()
        record_event(self.root, "run", artifact=path)
        state_path = self.root / "STATE.json"
        obj = json.loads(state_path.read_text(encoding="utf-8"))
        obj["last_event_id"] = None
        state_path.write_text(json.dumps(obj), encoding="utf-8")
        with self.assertRaisesRegex(ContractError, "mismatch"):
            status(self.root)
        self.assertEqual(recover(self.root)["status"], "CONSISTENT")

    def test_supported_claim_requires_recorded_run(self):
        (self.root / "paper.txt").write_text("draft", encoding="utf-8")
        claim = {"claim_id":"c1","task_id":"task1","claim_text":"effect",
                 "status":"SUPPORTED","strongest_alternative":"regularization",
                 "evidence_run_ids":["r1"],"artifact_refs":["paper.txt"]}
        (self.root / "claim.json").write_text(json.dumps(claim), encoding="utf-8")
        with self.assertRaisesRegex(ContractError, "missing/invalid"):
            record_event(self.root, "claim", artifact="claim.json")
        self.artifact()
        record_event(self.root, "run", artifact="r1.json")
        record_event(self.root, "claim", artifact="claim.json")
        self.assertEqual(status(self.root)["evidence_count"], 2)

    def test_non_data_claim_event_uses_real_fingerprinted_sources(self):
        for name in ("assumptions.md", "proof.md", "independent.md"):
            (self.root / name).write_text("reviewable " + name, encoding="utf-8")
        claim = {
            "claim_id": "c_theorem", "task_id": "theorem1", "claim_text": "A conditional lemma",
            "status": "CONFIRMED", "evidence_path": "NON_DATA",
            "evidence_type": "THEORETICAL_PROOF", "claim_scope": "bounded theorem only",
            "assumptions_ref": "assumptions.md", "strongest_alternative": "weaker theorem",
            "evidence_refs": ["proof.md"], "artifact_refs": ["proof.md"],
            "independent_validation_refs": ["independent.md"],
            "confirmation_scope": "THEOREM_SCOPE_ONLY",
            "confirmation_protocol_ref": "frozen_review_1",
            "independence_limit": "shared formal assumptions",
        }
        (self.root / "c_theorem.json").write_text(json.dumps(claim), encoding="utf-8")
        record_event(self.root, "claim", artifact="c_theorem.json")
        self.assertEqual(status(self.root, deep=True)["evidence_count"], 1)
        self.assertIsNone(status(self.root)["latest_valid_run_id"])
        (self.root / "proof.md").write_text("tampered", encoding="utf-8")
        with self.assertRaisesRegex(ContractError, "fingerprint"):
            status(self.root, deep=True)

    def test_non_data_claim_event_rejects_missing_real_evidence_file(self):
        (self.root / "assumptions.md").write_text("assumptions", encoding="utf-8")
        (self.root / "proof.md").write_text("proof", encoding="utf-8")
        claim = {
            "claim_id": "c_missing", "task_id": "theory1", "claim_text": "claim",
            "status": "SUPPORTED", "evidence_path": "NON_DATA",
            "evidence_type": "THEORETICAL_PROOF", "claim_scope": "theorem only",
            "assumptions_ref": "assumptions.md", "strongest_alternative": "counterexample",
            "evidence_refs": ["missing_independent_proof.md"],
            "artifact_refs": ["proof.md"],
        }
        (self.root / "c_missing.json").write_text(json.dumps(claim), encoding="utf-8")
        with self.assertRaisesRegex(ContractError, "artifact path missing"):
            record_event(self.root, "claim", artifact="c_missing.json")

    def test_writer_lock_blocks_mutations(self):
        path = self.root / ".evidence-write.lock"
        path.write_text("in-progress", encoding="utf-8")
        with self.assertRaisesRegex(ContractError, "another writer"):
            record_event(self.root, "note", note="should fail")
        path.unlink()
        self.assertEqual(status(self.root)["evidence_count"], 0)

    def test_no_path_escape(self):
        with self.assertRaises(ContractError):
            record_event(self.root, "run", artifact="../outside.json")

    def test_confirmed_claim_requires_sealed_run(self):
        self.artifact()
        record_event(self.root, "run", artifact="r1.json")
        (self.root / "paper.txt").write_text("draft", encoding="utf-8")
        claim = {"claim_id":"c1", "task_id":"task1","claim_text":"confirmed?",
                 "status":"CONFIRMED","strongest_alternative":"simple",
                 "evidence_run_ids":["r1"], "artifact_refs":["paper.txt"],
                 "confirmation_run_ids":["r1"], "confirmation_protocol_ref":"frozen"}
        (self.root / "c1.json").write_text(json.dumps(claim), encoding="utf-8")
        with self.assertRaisesRegex(ContractError, "confirmation Run"):
            record_event(self.root, "claim", artifact="c1.json")

if __name__ == "__main__":
    unittest.main()
