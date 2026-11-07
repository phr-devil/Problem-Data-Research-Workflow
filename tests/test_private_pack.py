"""Offline private-pack schema tests; all examples intentionally public/fake."""
import json
import tempfile
import unittest
from pathlib import Path
from evals.private_pack import ROOT, external, validate, public_tasks

def fixture():
    return {"format":"pdrw-private-pack-v1","visibility":"EXTERNAL_PRIVATE",
            "pack_id":"dummy","cases":[{"case_id":"A1",
               "agent_task":{"prompt":"Discuss synthetic data","allowed_effects":["READ_FILE"],"budget_id":"fixed"},
               "reference":{"rubric_version":"v1","review_criteria":["Plausible alternatives"]}}]}

class PrivatePackTests(unittest.TestCase):
    def test_no_reference_in_agent_export(self):
        public=public_tasks(fixture())
        self.assertEqual(len(public["cases"]),1)
        self.assertNotIn("reference",str(public))
        self.assertNotIn("Plausible alternatives",json.dumps(public))
        self.assertEqual(len(public["task_sha256"]),64)

    def test_missing_reference_and_duplicate_cases_rejected(self):
        data=fixture()
        data["cases"][0].pop("reference")
        with self.assertRaisesRegex(ValueError,"reference"):
            validate(data)
        data=fixture()
        data["cases"].append(data["cases"][0])
        with self.assertRaisesRegex(ValueError,"duplicate"):
            validate(data)

    def test_only_off_repo_locations_accepted(self):
        with self.assertRaisesRegex(ValueError,"outside"):
            external(ROOT / "evals/private-pack.json")
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"fixture.json"
            p.write_text(json.dumps(fixture()),encoding="utf-8")
            self.assertEqual(external(p,require_file=True),p.resolve())

    def test_contract_explicitly_denies_certification(self):
        content=(ROOT/"evals/PRIVATE_PACK_CONTRACT.md").read_text(encoding="utf-8")
        for item in ("REGRESSION_ONLY","NOT_CERTIFIED","NOT_MEASURED","TRACE_DECLARATIVE_ONLY"):
            self.assertIn(item,content)

if __name__=="__main__":
    unittest.main()
