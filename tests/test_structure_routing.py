"""Offline regression for additive, index-only PD-RW structure.

No image generation, code execution of research workflows, network or state changes.
"""
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


if __name__ == "__main__":
    unittest.main()
