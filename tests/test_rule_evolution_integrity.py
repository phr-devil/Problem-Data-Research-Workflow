"""Guard rule inheritance, owner routing and deterministic authority boundaries.

Offline/static checks do NOT simulate an LLM or certify scientific correctness.
"""
from pathlib import Path
import unittest

from chapter10_replay import audit_responses
from core.human_decision_review import review

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class RuleEvolutionIntegrity(unittest.TestCase):
    def test_no_brittle_caps_replace_semantic_requirements(self):
        for path in ("tests/test_structure_routing.py",
                     "tests/test_adaptive_output_token_policy.py",
                     "tests/test_dual_document_workflow.py"):
            source = read(path)
            for forbidden in ("assertLess(len(agent), 4500)",
                              "assertLess(len(workflow), 10000)",
                              "assertLess(len(data), 3500)"):
                self.assertNotIn(forbidden, source, (path, forbidden))
        self.assertIn("取消机械字符上限", read("docs/STRUCTURE.md"))

    def test_restored_six_part_handoff_and_probe_branches(self):
        action = read("NEXT_ACTION_POLICY.md")
        workflow = read("WORKFLOW.md")
        experiment = read("EXPERIMENT_LOOP.md")
        for fragment in ("USER_SCOPE", "期限/时效", "费用/算力上限",
                         "近邻", "竞争解释", "依赖是否失效",
                         "NEXT_LEGAL_ACTION_OR_USER_CHOICE", "IF_POS/NEG/INVALID"):
            self.assertIn(fragment, action, fragment)
        self.assertIn("DECISION_IF_POS/NEG/INVALID", workflow)
        self.assertIn("EXPERIMENT_LOOP.md", workflow)
        self.assertIn("IF_POS_NEG_INVALID", experiment)
        self.assertIn("INVALID", experiment)
        self.assertIn("INCONCLUSIVE", experiment)
        self.assertIn("不虚构 Run", action)

    def test_rule_reload_is_conditional_and_evidence_anchored(self):
        entry = read("AGENTS.md")
        record = read("DUAL_DOCUMENT_WORKFLOW.md")
        for marker in ("适用规则重核", "上下文压缩", "RULE_COMMIT",
                       "执行前", "复用", "原始许可"):
            self.assertIn(marker, entry)
        for marker in ("规则恢复不等于授权复制", "RULE_COMMIT",
                       "并发Agent", "旧决定"):
            self.assertIn(marker, record)
        self.assertIn("不能确认受限操作的许可时停止该操作", entry)

    def test_single_owner_with_change_trace_and_existing_gates(self):
        structure = read("docs/STRUCTURE.md")
        for key in ("AUTH-EXEC", "AUTH-SEALED", "AUTH-WRITE",
                    "AUTH-FIGURE", "EVIDENCE-VALIDITY", "RULE-RELOAD"):
            self.assertIn(key, structure)
        for key in ("PRESERVED", "MOVED", "MERGED", "REPLACED",
                    "RETIRED", "UNKNOWN", "NEGATIVE_CASES/TESTS"):
            self.assertIn(key, structure)
        template = read(".github/PULL_REQUEST_TEMPLATE.md")
        self.assertIn("Original requirement", template)
        self.assertIn("Owner / trigger", template)
        self.assertIn("Negative regression", template)
        self.assertIn("NOT_MEASURED", read("REPLAY_PROTOCOL.md"))
        self.assertIn("WRITING_LOCKED", read("WRITING_GATE.md"))
        self.assertIn("FIGURE_DRAWING_LOCKED", read("FIGURE_POLICY.md"))

    def test_decision_replay_blocks_unapproved_execution(self):
        cases = [{"id": "case", "expected_route": "PAPER_FIRST.md",
                  "decision_scope": "EVIDENCE"}]
        base = {"case_id": "case", "route": "PAPER_FIRST.md",
                "evidence_used": ["run:verified-dev"], "next_action": "inspect",
                "auth": "read-only", "decision_scope": "EVIDENCE",
                "claim_boundary": "DEV only", "cost_cap": "no fit",
                "expected_decision_change": "recheck scientific claim"}
        def run(**extra):
            return audit_responses([{**base, **extra}], cases)[0]["status"]
        self.assertEqual(run(next_action_owner="USER_DECISION_REQUIRED",
                             user_options=["Request fitting permission", "Read-only"],
                             next_agent_instruction="Train"), "INVALID")
        self.assertEqual(run(next_action_owner="AGENT_DECIDABLE",
                             next_agent_instruction="Train"), "INVALID")
        self.assertEqual(run(next_action_owner="NO_NEXT_ACTION",
                             next_agent_instruction="Invent new work"), "INVALID")
        self.assertEqual(run(next_action_owner="USER_DECISION_REQUIRED",
                             user_options=["Request permission", "Read-only"]), "CONTRACT_OK")
        # This is response-format preflight, NOT proof of real user authorization.
        self.assertEqual(review({"format": "pd-rw-human-review-v1",
                                 "target": "H3", "decisions": {}})["result"],
                         "REVIEW_REQUIRED")


if __name__ == "__main__":
    unittest.main()
