"""History-to-current policy trace and targeted deterministic behavior regression.

This suite checks actual repository owner files and existing advisory contracts.
It does not invoke agents, infer authentic user authorization or measure Token savings.
"""
import re
import unittest
from pathlib import Path

from core.human_decision_review import review
from chapter10_replay import audit_responses

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "RULE_INHERITANCE_AUDIT.md"


def doc(path):
    return (ROOT / path).read_text(encoding="utf-8")


def selected(step):
    return {"kind": "USER_CONFIRMED",
            "original_user_message_ref": f"synthetic-user-{step}",
            "chosen_option": f"synthetic-choice-{step}"}


class RuleInheritanceAuditTests(unittest.TestCase):
    def test_legacy_rules_map_to_existing_single_owner_and_live_witness(self):
        text = AUDIT.read_text(encoding="utf-8")
        self.assertIn("822c44ed633d", text)
        self.assertIn("13390243b5bf", text)
        rows = []
        for line in text.splitlines():
            if not re.match(r"^\| `[AW]\d{2}` \|", line):
                continue
            parts = [part.strip() for part in line.strip().strip("|").split("|")]
            self.assertEqual(len(parts), 6, line)
            ident, old_ref, owner, anchor, status, rationale = parts
            ident, owner, anchor, status = (part.strip("`") for part in
                                            (ident, owner, anchor, status))
            rows.append((ident, old_ref, owner, anchor, status))
            self.assertRegex(old_ref, r"^[AW]:L\d+(-\d+)?$")
            self.assertIn(status, {"PRESERVED", "MOVED", "MERGED", "REPLACED"})
            self.assertTrue(rationale, ident)
            target = ROOT / owner
            self.assertTrue(target.is_file(), (ident, owner))
            self.assertIn(anchor, target.read_text(encoding="utf-8"),
                          (ident, owner, anchor))
        ids = [r[0] for r in rows]
        self.assertEqual(len(ids), len(set(ids)), "historical ID reused")
        self.assertEqual(sum(x.startswith("A") for x in ids), 27)
        self.assertEqual(sum(x.startswith("W") for x in ids), 40)
        self.assertEqual(len(ids), 67)

    def test_explicit_replacements_override_obsolete_autonomy_and_word_rules(self):
        audit = doc("docs/RULE_INHERITANCE_AUDIT.md")
        for marker in ("`W04`", "`W11`", "`W15`", "`REPLACED`"):
            self.assertIn(marker, audit)
        self.assertIn("H1→H2→H3→H4→H5", doc("WORKFLOW.md"))
        self.assertIn("H4 由用户选D1", doc("DATA_DISCOVERY.md"))
        styles = doc("PAPER_WORD_STYLE.md")
        self.assertIn("全部样式", styles)
        self.assertIn("0/0 pt", styles)
        # H4 selection, even if declared, does not grant download/fitting access.
        decisions = {s: selected(s) for s in ("H1", "H2", "H3")}
        r = review({"format": "pd-rw-human-review-v1",
                    "target": "H4", "decisions": decisions})
        self.assertFalse(r["can_advance_declarations_only"])
        self.assertFalse(r["allows_download_training_sealed_or_writing"])
        decisions["H4"] = selected("H4")
        r = review({"format": "pd-rw-human-review-v1",
                    "target": "H5", "decisions": decisions})
        self.assertFalse(r["allows_download_training_sealed_or_writing"])
        self.assertFalse(r["can_advance_declarations_only"])

    def test_stale_data_choice_invalidates_downstream_not_other_science(self):
        decisions = {s: selected(s) for s in ("H1", "H2", "H3", "H4", "H5", "H6")}
        packet = {"format": "pd-rw-human-review-v1",
                  "target": "H7", "decisions": decisions,
                  "invalidated_decisions": ["H4"]}
        r = review(packet)
        self.assertEqual(r["result"], "REVIEW_REQUIRED")
        self.assertEqual(r["missing_prerequisites"], ["H4", "H5", "H6"])
        self.assertEqual(r["stale_declarations"], ["H4", "H5", "H6"])
        self.assertFalse(r["allows_download_training_sealed_or_writing"])

    def test_next_action_contract_blocks_premature_action_and_preserves_none(self):
        cases = [{"id": "synthetic", "expected_route": "PAPER_FIRST.md",
                  "decision_scope": "EVIDENCE"}]
        base = {"case_id": "synthetic", "route": "PAPER_FIRST.md",
                "evidence_used": ["DEV:synthetic"], "next_action": "inspect",
                "auth": "read-only", "decision_scope": "EVIDENCE",
                "claim_boundary": "DEV only", "cost_cap": "no fit",
                "expected_decision_change": "check evidence gap"}
        def status(**kw):
            return audit_responses([{**base, **kw}], cases)[0]["status"]
        self.assertEqual(status(next_action_owner="USER_DECISION_REQUIRED",
                                user_options=["request grant", "read only"],
                                next_agent_instruction="download and train"), "INVALID")
        self.assertEqual(status(next_action_owner="NO_NEXT_ACTION",
                                next_agent_instruction="new experiment"), "INVALID")
        self.assertEqual(status(next_action_owner="USER_DECISION_REQUIRED",
                                user_options=["request grant", "read only"]), "CONTRACT_OK")

    def test_no_duplicate_scientific_log_and_limits_still_enforced(self):
        structure = doc("docs/STRUCTURE.md")
        self.assertIn("RULE_INHERITANCE_AUDIT.md", structure)
        self.assertIn("普通科研任务不预读", structure)
        self.assertIn("按实际阻碍加载专题", doc("AGENTS.md"))
        self.assertIn("WRITING_LOCKED", doc("WRITING_GATE.md"))
        self.assertIn("FIGURE_DRAWING_LOCKED", doc("FIGURE_POLICY.md"))
        self.assertIn("SEALED", doc("CONFIRMATION.md"))
        self.assertIn("IF_POS/NEG/INVALID", doc("NEXT_ACTION_POLICY.md"))
        self.assertIn("INVALID", doc("EXPERIMENT_LOOP.md"))
        self.assertIn("不新增第三份常设台账", doc("DUAL_DOCUMENT_WORKFLOW.md"))
        self.assertIn("NOT_MEASURED", doc("REPLAY_PROTOCOL.md"))


if __name__ == "__main__":
    unittest.main()
