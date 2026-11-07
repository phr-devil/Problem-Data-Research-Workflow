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

    def test_new_indexes_are_pointers_with_valid_relative_links(self):
        for name in INDEXES:
            with self.subTest(index=name):
                path = ROOT / name
                data = path.read_text(encoding="utf-8")
                self.assertIn("INDEX_ONLY", data)
                self.assertLess(len(data), 3500, "an index should not become another policy")
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
