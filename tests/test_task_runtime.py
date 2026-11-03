"""Only read-only task/probe and fingerprint behavior is exercised."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from core.contracts import ContractError
from core.task_runtime import qualify_task, check_run_task_alignment
from core.probes import validate_probe, review_probe
from core.state import initialize, record_event, status

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def task_spec():
    return {
        "task_id":"task1", "protocol_id":"p1", "dataset_version":"d1",
        "target_definition":"predict label from past sensor samples",
        "label_provenance":"manual labels; validity requires a separate audit",
        "prediction_time":"before observed future outcome",
        "group_key":"subject", "independent_unit":"subject",
        "metric":"macro_f1", "metric_direction":"max",
        "evaluator_version":"e1", "legal_inputs":["sensor"],
        "editable_paths":["model.py"],
        "protected_paths":["data.json", "split.json", "eval.py"],
        "references":{"data_manifest":"data.json",
                      "split_manifest":"split.json", "evaluator":"eval.py"},
        "correctness_checks":["negative test: train/dev subject overlap rejects"]
    }

def probe():
    return {
        "probe_id":"q1", "task_id":"task1", "parent_run_id":"r1",
        "observed_error":"cross-device labels collapse", "failed_premise":"static calibration invariant",
        "competing_explanation":"baseline undertrained", "mechanism":"device-dependent scale",
        "lever":"INDUCTIVE_BIAS", "distinct_prediction":"gain on unseen device not training subset",
        "minimum_test":"paired device-held-out dev groups against matched tuned baseline",
        "if_positive":"retest on independent dev groups",
        "if_negative":"discard this mechanism only",
        "if_invalid":"fix evaluator and rerun affected comparison",
        "estimated_cost":"0.3 GPU h", "authorization_scope":"existing dev-only GPU budget",
        "evidence_refs":["runs/r1.json"]
    }

class TaskSpecTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        for fname, content in [
            ("data.json", '{"data_version":"d1"}'),
            ("split.json", '{"train_ids":["1","2"],"dev_ids":["3"],"train_groups":["a"],"dev_groups":["b"]}'),
            ("eval.py", "# evaluator stub; NOT executed by task-check\n"),
            ("model.py", "# editable model stub\n"),
            ("metrics.json", '{"macro_f1":0.6}'),
            ("pred.csv", "sample_id,y_pred\n3,1\n")]:
            (self.root/fname).write_text(content, encoding="utf-8")
        self.spec=task_spec()
        (self.root/"task.json").write_text(json.dumps(self.spec),encoding="utf-8")

    def test_disjoint_and_fingerprints(self):
        result=qualify_task(self.root,"task.json")
        self.assertEqual(result["qualification"],"STRUCTURAL_PRECHECK_ONLY")
        self.assertEqual(result["split_checks"],["train_ids/dev_ids:DISJOINT", "train_groups/dev_groups:DISJOINT"])
        self.assertEqual(result["fingerprints"]["evaluator"],digest(self.root/"eval.py"))

    def test_evaluator_tamper_is_rejected_with_expected_sha(self):
        self.spec["expected_sha256"]={"evaluator":digest(self.root/"eval.py")}
        (self.root/"task.json").write_text(json.dumps(self.spec),encoding="utf-8")
        (self.root/"eval.py").write_text("# changed\n",encoding="utf-8")
        with self.assertRaisesRegex(ContractError,"stale protected"):
            qualify_task(self.root,"task.json")

    def test_development_group_leakage(self):
        (self.root/"split.json").write_text('{"train_groups":["p1"],"dev_groups":["p1"]}',encoding="utf-8")
        with self.assertRaisesRegex(ContractError,"leakage"):
            qualify_task(self.root,"task.json")

    def test_outside_project_root_is_rejected(self):
        self.spec["references"]["evaluator"]="../outside.py"
        self.spec["protected_paths"]=["data.json","split.json","../outside.py"]
        (self.root/"task.json").write_text(json.dumps(self.spec),encoding="utf-8")
        with self.assertRaises(ContractError):
            qualify_task(self.root,"task.json")

    def test_run_alignment(self):
        valid={"task_id":"task1","protocol_id":"p1","dataset_version":"d1",
               "evaluator_version":"e1","legal_inputs":["sensor"],
               "task_spec_ref":"task.json","task_spec_sha256":digest(self.root/"task.json")}
        check_run_task_alignment(self.root,valid)
        valid["evaluator_version"]="different"
        with self.assertRaisesRegex(ContractError,"mismatch"):
            check_run_task_alignment(self.root,valid)

    def test_linked_artifacts_are_detected_in_deep_status(self):
        initialize(self.root,"toy")
        valid={"run_id":"r1","task_id":"task1","protocol_id":"p1",
               "dataset_version":"d1","evaluator_version":"e1",
               "group_split":"split-v1","sample_ids_hash":"group-hash",
               "legal_inputs":["sensor"],"split":"dev","status":"VALID",
               "metrics":{"macro_f1":0.6},
               "artifact_refs":{"metrics":"metrics.json","predictions":"pred.csv","code":"model.py"},
               "task_spec_ref":"task.json","task_spec_sha256":digest(self.root/"task.json")}
        (self.root/"run.json").write_text(json.dumps(valid),encoding="utf-8")
        event=record_event(self.root,"run",artifact="run.json")
        self.assertIn("pred.csv",event["linked_sha256"])
        self.assertEqual(status(self.root,deep=True)["linked_fingerprints"],"DEEP_VERIFIED")
        (self.root/"pred.csv").write_text("changed\n",encoding="utf-8")
        self.assertEqual(status(self.root)["status"],"CONSISTENT")
        with self.assertRaisesRegex(ContractError,"linked artifact fingerprint"):
            status(self.root,deep=True)

class ProbeTests(unittest.TestCase):
    def test_valid_probe_needs_auth(self):
        self.assertEqual(review_probe(probe())["decision"],"AUTH_REQUIRED")

    def test_duplicate_premise_review_not_auto_stop(self):
        x=review_probe(probe(),previous_failed_premises=["static calibration invariant"],authorization_granted=True)
        self.assertEqual(x["decision"],"REVIEW_DIFFERENT_LEVER")

    def test_same_text_cannot_be_mechanism_discriminator(self):
        p=probe()
        p["distinct_prediction"]=p["competing_explanation"]
        with self.assertRaisesRegex(ContractError,"distinguishable"):
            validate_probe(p)

    def test_missing_evidence_rejected(self):
        p=probe();p["evidence_refs"]=[]
        with self.assertRaisesRegex(ContractError,"evidence"):
            validate_probe(p)

if __name__=="__main__":
    unittest.main()
