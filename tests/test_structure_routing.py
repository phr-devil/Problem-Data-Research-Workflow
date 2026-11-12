"""Offline regression for additive, index-only PD-RW structure.

No image generation, code execution of research workflows, network or state changes.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEXES = (
    "modules/README.md", "modules/research/README.md", "modules/paper/README.md",
    "modules/figures/README.md", "policies/README.md", "docs/STRUCTURE.md",
)
CANONICAL = (
    "AGENTS.md", "WORKFLOW.md", "START.md", "NEXT_ACTION_POLICY.md",
    "WRITING_GATE.md", "FIGURE_POLICY.md", "ACADEMIC_DIAGRAM_STYLE.md",
    "DUAL_DOCUMENT_WORKFLOW.md", "PAPER_WORD_STYLE.md",
    "SEARCH_DISCOVERY.md", "DATA_DISCOVERY.md", "EXPERIMENT_LOOP.md",
    "CONFIRMATION.md", "templates/PAPER_BLUEPRINT.md",
    "templates/RESEARCH_RECORD.md", "core/figure_change_scope.py",
)
LINK = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")


class RoutingStructureTests(unittest.TestCase):
    def test_entry_and_canonical_paths_unchanged(self):
        for name in CANONICAL + INDEXES:
            with self.subTest(path=name):
                self.assertTrue((ROOT / name).is_file(), name)
        agent = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("唯一默认入口", agent)
        self.assertIn("WORKFLOW.md", agent)
        self.assertIn("FIGURE_POLICY.md", agent)
        self.assertIn("WRITING_GATE.md", agent)
        self.assertIn("DUAL_DOCUMENT_WORKFLOW.md", agent)
        self.assertIn("modules/README.md", agent)

    def test_compact_entry_and_provenance_contract(self):
        agent = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        workflow = (ROOT / "WORKFLOW.md").read_text(encoding="utf-8")
        structure = (ROOT / "docs/STRUCTURE.md").read_text(encoding="utf-8")
        # No hard character caps: scientifically necessary conditions must survive edits.
        # Structure tests verify ownership/routing; Agent reading cost requires replay.
        self.assertIn("唯一默认入口", agent)
        self.assertIn("唯一科研决策总控", workflow)
        for marker in ("RULE_REPO", "RULE_COMMIT", "LOADED_FILES",
                       "RULE_VERSION_UNVERIFIED", "按实际阻碍"):
            self.assertIn(marker, agent)
        for marker in ("三个决策循环（六项活动", "SCIENCE_RESULT_HARVEST.md",
                       "WRITING_LOCKED", "CONFIRMATION.md"):
            self.assertIn(marker, workflow)
        self.assertIn("单一权威", structure)
        self.assertIn("优先替换", structure)

    def test_new_indexes_are_pointers_with_valid_relative_links(self):
        for name in INDEXES:
            with self.subTest(index=name):
                path = ROOT / name
                data = path.read_text(encoding="utf-8")
                self.assertIn("INDEX_ONLY", data)
                # Navigation remains INDEX_ONLY without a brittle size threshold.
                for target in LINK.findall(data):
                    if target.startswith(("http:", "https:", "mailto:", "#")):
                        continue
                    dest = target.split("#", 1)[0]
                    resolved = (path.parent / dest).resolve()
                    self.assertTrue(resolved.is_relative_to(ROOT.resolve()),
                                    f"index link escapes repository: {name} -> {target}")
                    self.assertTrue(resolved.exists(), f"broken index link: {name} -> {target}")

    def test_task_routes_do_not_create_permissions(self):
        policy = (ROOT / "FIGURE_POLICY.md").read_text(encoding="utf-8")
        writing = (ROOT / "WRITING_GATE.md").read_text(encoding="utf-8")
        self.assertIn("FIGURE_DRAWING_LOCKED", policy)
        self.assertIn("WRITING_LOCKED", writing)
        self.assertIn("禁止", writing)
        art = (ROOT / "modules/figures/README.md").read_text(encoding="utf-8")
        paper = (ROOT / "modules/paper/README.md").read_text(encoding="utf-8")
        self.assertIn("../../FIGURE_POLICY.md", art)
        self.assertIn("../../WRITING_GATE.md", paper)

    def test_single_main_workflow_not_duplicated(self):
        self.assertFalse((ROOT / "modules/WORKFLOW.md").exists())
        self.assertFalse((ROOT / "policies/WORKFLOW.md").exists())
        self.assertIn("原有三循环/六活动", (ROOT / "docs/STRUCTURE.md").read_text(encoding="utf-8"))


    def test_current_strategy_authority_and_protocol_mirror(self):
        """Catch stale responsibility/version prose, not just present files."""
        workflow = (ROOT / "WORKFLOW.md").read_text(encoding="utf-8")
        structure = (ROOT / "docs/STRUCTURE.md").read_text(encoding="utf-8")
        inheritance = (ROOT / "docs/RULE_INHERITANCE_AUDIT.md").read_text(encoding="utf-8")
        agent = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        review = (ROOT / "AUTHOR_STRATEGY_REVIEW.md").read_text(encoding="utf-8")
        protocol = json.loads(
            (ROOT / "contracts/human_review_protocol.v1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(protocol["protocol_version"], "pd-rw-human-review-v1.3")
        for document in (workflow, structure, agent, review):
            with self.subTest(document=document[:45]):
                self.assertIn("H6", document)
                self.assertIn("H8", document)
                self.assertIn("作者", document)
        self.assertIn("H7", workflow)
        self.assertIn("H7", structure)
        self.assertIn("pd-rw-human-review-v1.3", structure)
        self.assertIn("pd-rw-human-review-v1.3", inheritance)
        for obsolete in ("H6–H8改为AI主责", "H6–H8由AI", "H6–H8 AI自主开发",
                         "机器合同采用`pd-rw-human-review-v1.2`"):
            with self.subTest(obsolete=obsolete):
                self.assertNotIn(obsolete, structure)
                self.assertNotIn(obsolete, inheritance)

    def test_documented_synthetic_scenario_count_matches_json(self):
        cases = json.loads((ROOT / "SCENARIOS.json").read_text(encoding="utf-8"))["cases"]
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"{len(cases)}个PD-RW专属的**合成**反例/风险场景", readme)
        self.assertEqual(len({case["id"] for case in cases}), len(cases))

    def test_rule_change_owner_map_and_scope(self):
        structure = (ROOT / "docs/STRUCTURE.md").read_text(encoding="utf-8")
        for marker in ("增量规则变更的结构合同", "唯一 owner", "显式退役",
                       "定向测试", "NOT_MEASURED"):
            self.assertIn(marker, structure)



if __name__ == "__main__":
    unittest.main()
