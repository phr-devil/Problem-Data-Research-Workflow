"""Case-index regression: checks structure and distinctions, not scientific truth."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CaseRegistryContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = (ROOT / "LESSONS/CASE_REGISTRY.md").read_text(encoding="utf-8")
        cls.agent = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    def test_coverage_and_unique_case_identity(self):
        ids = re.findall(r"(?m)^\|\s*(?:\*\*)?`([A-Z0-9-]+)`", self.case)
        self.assertGreaterEqual(len(ids), 28)
        self.assertEqual(len(ids), len(set(ids)), "Do not merge or duplicate cases")
        for required in (
            "SAFE-GAIT-K1", "CRPS-P19", "GALAXY-HRGUARD-P23",
            "MV-UNCERTAINTY-P24", "DUAL-IMU-P21", "LR-IMU-P25",
            "TACVERSE-Q0-P28", "PTLG-P31", "PMSM-THERMAL"
        ):
            self.assertIn(required, ids)

    def test_status_axes_do_not_falsely_promote_evidence(self):
        for required in (
            "ALGO_DEV_POSITIVE", "SCIENTIFIC_RESULT_SUPPORTED",
            "PAPER_PATH_CANDIDATE", "CONFIRMATION_DONE_SCOPED",
            "USER_ASSERTED_SUCCESS", "ALGO_FINAL_METRICS_UNKNOWN",
            "SECONDARY_LOCAL_AUDIT", "NOT_RUN", "IDENTITY_CONFLICT",
            "SOURCE", "归档算法分支不取消其它已成立的科学结论"
        ):
            if required == "SOURCE":
                self.assertIn("来源简称", self.case)
            else:
                self.assertIn(required, self.case)
        self.assertIn("37 条 SEALED", self.case)
        self.assertIn("5 人同数据源确认", self.case)
        self.assertIn("待", self.case)

    def test_single_owner_and_no_default_preload(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        structure = (ROOT / "docs/STRUCTURE.md").read_text(encoding="utf-8")
        discovery = (ROOT / "SEARCH_DISCOVERY.md").read_text(encoding="utf-8")
        for x in (readme, structure, discovery):
            self.assertIn("LESSONS/CASE_REGISTRY.md", x)
        self.assertIn("跨项目成功/失败/身份追溯", self.agent)
        self.assertIn("LESSONS/CASE_REGISTRY.md", self.agent)
        self.assertIn("仅在明确复盘", self.agent)
        # Loading the historical case registry is conditional, not default.
        # Do not truncate entrypoint rules to meet an arbitrary character cap.
        self.assertIn("按实际阻碍加载专题", self.agent)
        self.assertIn("适用规则重核", self.agent)
        self.assertIn("CASE_INDEX_ONLY", self.case)
        self.assertIn("REPLAY_PROTOCOL.md", self.case)


if __name__ == "__main__":
    unittest.main()
