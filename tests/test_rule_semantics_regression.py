"""Focused read-only regression for rule/version routing and DEV permission boundaries.

This tests deterministic code behavior and current documentation contracts.
It does not authenticate user grants or prove live Agent compliance.
"""
import json
import re
import unittest
from pathlib import Path

from core.execution_preflight import action_preflight

ROOT = Path(__file__).resolve().parents[1]


class RuleSemanticsRegression(unittest.TestCase):
    def test_current_protocol_matches_user_facing_technical_entry(self):
        contract = json.loads(
            (ROOT / "contracts/human_review_protocol.v1.json").read_text(encoding="utf-8")
        )
        core_guide = (ROOT / "core/README.md").read_text(encoding="utf-8")
        self.assertEqual(contract["protocol_version"], "pd-rw-human-review-v1.3")
        self.assertIn("新项目默认 v1.3", core_guide)
        self.assertIn(contract["protocol_version"], core_guide)
        self.assertNotIn("统一审核合同 v1.1（新项目默认）", core_guide)

    def test_docs_state_h5_h6_and_legacy_scope_together(self):
        structure = (ROOT / "docs/STRUCTURE.md").read_text(encoding="utf-8")
        self.assertRegex(structure, r"H5范围有效、H6作者策略已选择/委托")
        self.assertIn("旧项目未变范围经原消息核实", structure)
        self.assertIn("执行宿主原始权限", structure)
        self.assertNotIn("安全非付费本地DEV训练在H5后不需逐次批准", structure)

    def test_dev_in_scope_is_autonomous_but_not_self_authorized(self):
        base = dict(
            action="DEV_TRAIN", h5_scope_confirmed=True,
            dev_inputs_verified=True, within_h5_scope=True,
            within_author_selected_strategy=True, safe_local_nonpaid=True,
            no_project_specific_prohibition=True,
            h6_author_strategy_confirmed=True,
        )
        self.assertEqual(action_preflight(base)["decision"], "UNKNOWN")
        self.assertEqual(
            action_preflight(base, independently_authorized=True)["decision"],
            "ALLOW",
        )
        # Each indispensable prerequisite must independently fail closed.
        for key in ("h5_scope_confirmed", "dev_inputs_verified",
                    "within_h5_scope", "within_author_selected_strategy",
                    "safe_local_nonpaid", "no_project_specific_prohibition"):
            with self.subTest(prerequisite=key):
                packet = dict(base)
                packet[key] = False
                self.assertEqual(
                    action_preflight(packet, independently_authorized=True)["decision"],
                    "BLOCK",
                )

    def test_new_h6_absent_does_not_turn_h5_into_training_permission(self):
        base = dict(
            action="DEV_TRAIN", h5_scope_confirmed=True,
            dev_inputs_verified=True, within_h5_scope=True,
            within_author_selected_strategy=True, safe_local_nonpaid=True,
            no_project_specific_prohibition=True,
        )
        result = action_preflight(base, independently_authorized=True)
        self.assertNotEqual(result["decision"], "ALLOW")
        pending = dict(base, h6_strategy_pending=True)
        self.assertEqual(
            action_preflight(pending, independently_authorized=True)["decision"],
            "BLOCK",
        )
        legacy = dict(
            base, legacy_unchanged_scope_confirmed=True,
            h6_strategy_pending=True,
        )
        self.assertEqual(
            action_preflight(legacy, independently_authorized=True)["decision"],
            "ALLOW",
        )

    def test_restricted_effect_is_not_granted_by_dev_authorization(self):
        for action in ("READ_SEALED", "DOWNLOAD", "WRITE_MANUSCRIPT",
                       "DRAW_IMAGE", "PAY", "EXTERNAL_UPLOAD", "SUBMIT"):
            with self.subTest(action=action):
                self.assertEqual(
                    action_preflight(dict(
                        action=action, h5_scope_confirmed=True,
                        h6_author_strategy_confirmed=True, user_approved=True,
                    ))["decision"],
                    "UNKNOWN",
                )

    def test_legacy_notes_are_not_current_entry_instructions(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        legacy = (ROOT / "docs/LEGACY_RELEASE_NOTES.md").read_text(encoding="utf-8")
        self.assertIn("docs/LEGACY_RELEASE_NOTES.md", readme)
        self.assertNotIn("## v1.5 轻量执行层", readme)
        self.assertIn("## v1.5 轻量执行层", legacy)
        self.assertIn("非现行规则", legacy)


if __name__ == "__main__":
    unittest.main()
