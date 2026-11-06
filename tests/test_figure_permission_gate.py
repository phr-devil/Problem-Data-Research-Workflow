"""Guard the explicit-user-only figure generation policy."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FigurePermissionGateTests(unittest.TestCase):
    def test_no_automatic_figures(self):
        policy = (ROOT / "FIGURE_POLICY.md").read_text(encoding="utf-8")
        for key in ("FIGURE_DRAWING_LOCKED", "不生成任何图片", "只有用户本人明确要求",
                    "不运行绘图脚本", "WRITING_LOCKED", "不自动要求绘图"):
            with self.subTest(key=key):
                self.assertIn(key, policy)

    def test_entry_points_reference_figure_guard(self):
        for name in ("AGENTS.md", "START.md", "WORKFLOW.md", "WRITING_GATE.md",
                     "CONFIRMATION.md", "NEXT_ACTION_POLICY.md"):
            with self.subTest(name=name):
                self.assertIn("FIGURE_POLICY.md", (ROOT / name).read_text(encoding="utf-8"))

    def test_figure_request_does_not_grant_other_authorizations(self):
        policy = (ROOT / "FIGURE_POLICY.md").read_text(encoding="utf-8")
        self.assertIn("绘图授权**独立于论文写作授权**", policy)
        self.assertIn("不授予数据下载", policy)


if __name__ == "__main__":
    unittest.main()
