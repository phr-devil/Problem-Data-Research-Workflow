"""Deterministic regression of figure cache/delta QA without rendering images."""
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
import unittest

from core.figure_change_scope import advise

ROOT = Path(__file__).resolve().parents[1]


class FigureChangeScopeTests(unittest.TestCase):
    def setUp(self):
        self.src = json.loads((ROOT / "templates/FIGURE_SPEC.example.json").read_text(encoding="utf-8"))
        self.src["figure_id"] = "Figure2"
        self.src["sources"]["source_fingerprint"] = "checked-sha-1"
        self.src["scientific"]["must_show"] = [{"id": "M1", "evidence_ref": "method:3.2",
                                                "visual_ids": ["A", "B"]}]
        self.src["scientific"]["nodes"] = [{"id": "A"}, {"id": "B"}]
        self.src["scientific"]["edges"] = [{"id": "E1", "from": "A", "to": "B"}]
        self.src["qa"] = dict.fromkeys(("science_qa", "connectors_qa", "visual_qa"), "PASS")

    def test_first_render_needs_all_scientific_and_visual_checks(self):
        result = advise(None, self.src)
        self.assertEqual(result["change_flags"], ["FIRST_RENDER"])
        self.assertIn("ALL_CONNECTORS", result["suggested_checks"])
        self.assertIn("FINAL_PAPER_WIDTH_VISUAL", result["suggested_checks"])

    def test_unchanged_verified_spec_skips_rework(self):
        result = advise(self.src, deepcopy(self.src))
        self.assertEqual(result["change_flags"], ["NO_SPEC_CHANGE"])
        self.assertEqual(result["suggested_checks"], [])

    def test_label_only_change_is_local_but_final_visual_required(self):
        other = deepcopy(self.src)
        other["design"]["labels"] = {"A": "Input"}
        result = advise(self.src, other)
        self.assertEqual(result["change_flags"], ["LABEL_CHANGE"])
        self.assertIn("CHANGED_LABELS_BOXES_ADJACENT_CONNECTORS", result["suggested_checks"])
        self.assertIn("FINAL_PAPER_WIDTH_VISUAL", result["suggested_checks"])
        self.assertFalse(result["needs_new_design"])

    def test_topology_change_requires_complete_science_and_connectors(self):
        other = deepcopy(self.src)
        other["scientific"]["edges"][0]["to"] = "C"
        result = advise(self.src, other)
        self.assertIn("SCIENTIFIC_CHANGE", result["change_flags"])
        self.assertIn("ALL_MUST_SHOW_AND_SCIENCE", result["suggested_checks"])
        self.assertIn("ALL_CONNECTORS", result["suggested_checks"])

    def test_source_change_requires_science_refresh(self):
        other = deepcopy(self.src)
        other["sources"]["source_fingerprint"] = "checked-sha-2"
        result = advise(self.src, other)
        self.assertIn("SOURCE_CHANGE", result["change_flags"])
        self.assertIn("REAL_SOURCE_AND_CLAIMS", result["suggested_checks"])

    def test_unknown_source_and_unverified_qa_prevent_cache_skip(self):
        other = deepcopy(self.src)
        other["sources"]["source_fingerprint"] = "UNKNOWN"
        other["qa"]["visual_qa"] = "NOT_RUN"
        result = advise(other, deepcopy(other))
        self.assertIn("SOURCE_UNVERIFIED", result["change_flags"])
        self.assertIn("PRIOR_QA_UNVERIFIED", result["change_flags"])
        self.assertIn("FINAL_PAPER_WIDTH_VISUAL", result["suggested_checks"])

    def test_local_issue_keeps_incremental_route(self):
        other = deepcopy(self.src)
        other["design"]["review"] = {
            "issue_scope": "LOCAL", "stalled": False, "rejected_layout_reason": ""
        }
        result = advise(self.src, other)
        self.assertEqual(result["recommended_mode"], "LOCAL_EDIT")
        self.assertFalse(result["discard_prior_global_layout"])

    def test_global_layout_failure_rebuilds_without_science_change(self):
        other = deepcopy(self.src)
        other["design"]["review"] = {
            "issue_scope": "GLOBAL_LAYOUT", "stalled": False,
            "rejected_layout_reason": "Parallel branches obscured by one linear row"
        }
        other["qa"]["global_design_qa"] = "FAIL"
        result = advise(self.src, other)
        self.assertNotIn("SCIENTIFIC_CHANGE", result["change_flags"])
        self.assertEqual(result["recommended_mode"], "LAYOUT_REBUILD")
        self.assertTrue(result["needs_new_design"])
        self.assertTrue(result["discard_prior_global_layout"])
        self.assertIn("GLOBAL_DESIGN_QA", result["suggested_checks"])

    def test_conceptual_visual_anchor_requires_full_redesign(self):
        other = deepcopy(self.src)
        other["design"]["review"] = {
            "issue_scope": "VISUAL_ANCHORING", "stalled": False,
            "rejected_layout_reason": "Old image constrains an incorrect reading order"
        }
        result = advise(self.src, other)
        self.assertEqual(result["recommended_mode"], "FULL_REDESIGN")
        self.assertTrue(result["discard_prior_global_layout"])

    def test_stalled_local_edit_requires_strategy_review_not_forced_redesign(self):
        other = deepcopy(self.src)
        other["design"]["review"] = {
            "issue_scope": "LOCAL", "stalled": True,
            "rejected_layout_reason": "Text remains unreadable after two edits"
        }
        result = advise(self.src, other)
        self.assertEqual(result["recommended_mode"], "LOCAL_EDIT")
        self.assertTrue(result["needs_strategy_switch"])
        self.assertIn("DIAGNOSE_STAGNATION", result["suggested_checks"])

    def test_explicit_failed_global_qa_blocks_cache_skip(self):
        other = deepcopy(self.src)
        other["qa"]["global_design_qa"] = "FAIL"
        result = advise(self.src, other)
        self.assertEqual(result["recommended_mode"], "LAYOUT_REBUILD")
        self.assertIn("GLOBAL_DESIGN_QA_UNVERIFIED", result["change_flags"])
        self.assertIn("GLOBAL_DESIGN_QA", result["suggested_checks"])

    def test_initial_design_has_global_qa(self):
        result = advise(None, self.src)
        self.assertEqual(result["recommended_mode"], "INITIAL_DESIGN")
        self.assertIn("GLOBAL_DESIGN_QA", result["suggested_checks"])

    def test_invalid_review_is_rejected(self):
        other = deepcopy(self.src)
        other["design"]["review"] = {"issue_scope": "MADE_UP", "stalled": False}
        with self.assertRaises(ValueError):
            advise(self.src, other)

    def test_policy_document_routes_are_scoped(self):
        acad = (ROOT / "ACADEMIC_DIAGRAM_STYLE.md").read_text(encoding="utf-8")
        policy = (ROOT / "FIGURE_POLICY.md").read_text(encoding="utf-8")
        qa = (ROOT / "MANUSCRIPT_QA.md").read_text(encoding="utf-8")
        for token in ("DESIGN_PREFLIGHT", "DESIGN_ROUTE", "LOCAL_EDIT",
                      "LAYOUT_REBUILD", "FULL_REDESIGN", "GLOBAL_DESIGN_QA",
                      "图像锚定隔离", "失败原因"):
            self.assertIn(token, acad)
        self.assertIn("不自动改动已认可的其他图", policy)
        self.assertIn("GLOBAL_DESIGN_QA", policy)
        self.assertIn("整体可读性", qa)

    def test_invalid_spec_and_mismatched_ids_rejected(self):
        with self.assertRaises(ValueError):
            advise(self.src, {"figure_id": "Figure2"})
        other = deepcopy(self.src)
        other["figure_id"] = "Figure3"
        with self.assertRaises(ValueError):
            advise(self.src, other)

    def test_rules_preserve_image_permission_and_quality(self):
        acad = (ROOT / "ACADEMIC_DIAGRAM_STYLE.md").read_text(encoding="utf-8")
        policy = (ROOT / "FIGURE_POLICY.md").read_text(encoding="utf-8")
        agent = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for token in ("FIGURE_SPEC.example.json", "增量重绘", "差异 QA",
                      "实际渲染", "MUST_SHOW", "drawio-academic-skills"):
            self.assertIn(token, acad)
        for token in ("用户明确", "FIGURE_DRAWING_LOCKED", "论文实际宽度",
                      "core.figure_change_scope"):
            self.assertIn(token, policy)
        self.assertIn("ACADEMIC_DIAGRAM_STYLE.md", agent)
        self.assertIn("core.figure_change_scope", agent)


if __name__ == "__main__":
    unittest.main()
