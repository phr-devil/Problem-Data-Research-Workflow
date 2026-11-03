"""Optional RWF bridge must be read-only, scoped, and fail closed."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from core.contracts import ContractError
from core.forge_bridge import verify_with_forge


class ForgeBridgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.pd = self.root / "pd"
        self.rwf = self.root / "rwf"
        self.project = self.root / "forge-project"
        self.pd.mkdir()
        self.project.mkdir()
        (self.rwf / "adapters").mkdir(parents=True)
        (self.rwf / "adapters" / "pd_rw_bridge.py").write_text("# RWF installed in real use")
        self.run = self.pd / "run.json"
        self.run.write_text('{"run_id":"R","metrics":{"macro_F1":0.7}}')

    def call(self):
        return verify_with_forge(self.pd, self.run, self.rwf,
                                 self.project, self.project / "run.json", "macro_F1")

    def output(self, **changes):
        evidence = {
            "status": "METRIC_VERIFIED_DEV_ONLY",
            "pd_run_sha256": hashlib.sha256(self.run.read_bytes()).hexdigest(),
            "forge_run_sha256": "a" * 64,
            "prediction_sha256": "b" * 64,
            "metric": "macro_F1",
            "recomputed_value": 0.7,
        }
        evidence.update(changes)
        return SimpleNamespace(returncode=0, stdout=json.dumps(evidence), stderr="")

    def test_verified_handoff_is_dev_only(self):
        with patch("core.forge_bridge.subprocess.run", return_value=self.output()) as call:
            result = self.call()
        self.assertEqual(result["verification"], "METRIC_VERIFIED_DEV_ONLY")
        self.assertFalse(result["scientific_confirmation"])
        self.assertEqual(call.call_args.kwargs["cwd"], self.rwf)

    def test_sha_mismatch_fails_closed(self):
        with patch("core.forge_bridge.subprocess.run",
                   return_value=self.output(pd_run_sha256="0"*64)):
            with self.assertRaisesRegex(ContractError, "does not match"):
                self.call()

    def test_forge_failure_fails_closed(self):
        with patch("core.forge_bridge.subprocess.run",
                   return_value=SimpleNamespace(returncode=2, stdout="", stderr="bad labels")):
            with self.assertRaisesRegex(ContractError, "bad labels"):
                self.call()

    def test_external_run_path_rejected(self):
        outside = self.root / "outside.json"
        outside.write_text("{}")
        with self.assertRaisesRegex(ContractError, "under its project root"):
            verify_with_forge(self.pd, outside, self.rwf, self.project, outside, "macro_F1")

    def test_relative_forge_run_scoped_to_forge_project(self):
        with patch("core.forge_bridge.subprocess.run", return_value=self.output()) as proc:
            self.call()
        args = proc.call_args.args[0]
        self.assertEqual(args[args.index("--forge-run")+1],
                         str((self.project / "run.json").resolve()))

    def test_non_finite_metric_receipt_is_rejected(self):
        with patch("core.forge_bridge.subprocess.run",
                   return_value=self.output(recomputed_value="nan")):
            with self.assertRaisesRegex(ContractError, "finite recomputed"):
                self.call()

    def test_missing_rwf_bridge_rejected(self):
        (self.rwf / "adapters" / "pd_rw_bridge.py").unlink()
        with self.assertRaisesRegex(ContractError, "bridge missing"):
            self.call()


if __name__ == "__main__":
    unittest.main()
