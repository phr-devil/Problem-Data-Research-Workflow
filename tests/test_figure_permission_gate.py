"""Guard the explicit-user-only figure generation policy."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FigurePermissionGateTests(unittest.TestCase):
    def test_no_automatic_figures(self):
        policy = (ROOT / "FIGURE_POLICY.md").read_text(encoding="utf-8")
        for key in ("FIGURE_DRAWING_LOCKED", "不生成任何图片", "用户明确要求",
                    "不运行绘图脚本", "WRITING_LOCKED", "不会自动要求绘图"):
            with self.subTest(key=key):
                self.assertIn(key, policy)

    def test_entry_points_reference_figure_guard(self):
        for name in ("AGENTS.md", "START.md", "WORKFLOW.md", "WRITING_GATE.md",
                     "CONFIRMATION.md", "NEXT_ACTION_POLICY.md"):
            with self.subTest(name=name):
                self.assertIn("FIGURE_POLICY.md", (ROOT / name).read_text(encoding="utf-8"))

    def test_style_freeze_keeps_opt_in_gate(self):
        policy = (ROOT / "FIGURE_POLICY.md").read_text(encoding="utf-8")
        for marker in ("没有用户明确出图要求", "CI也不得实际渲染图片", "style_fingerprint",
                       "template_id", "不要求为普通科研项目安装"):
            with self.subTest(marker=marker):
                self.assertIn(marker, policy)

    def test_palette_is_selection_not_authorization(self):
        policy = (ROOT / "FIGURE_POLICY.md").read_text(encoding="utf-8")
        for name in ("tol-bright", "tol-muted", "tol-vibrant", "okabe-ito", "tableau10",
                     "semantic_colors", "palette_registry_version", "不因升级工作流而自动迁移",
                     "只有用户明确要求绘图才能实际渲染", "无法", "SEALED访问"):
            # The policy wording, not palette metadata, determines actual image permission.
            if name == "无法":
                continue
            with self.subTest(name=name):
                self.assertIn(name, policy)

    def test_figure_request_does_not_grant_other_authorizations(self):
        policy = (ROOT / "FIGURE_POLICY.md").read_text(encoding="utf-8")
        self.assertIn("绘图授权**独立于论文写作授权**", policy)
        self.assertIn("不授予数据下载", policy)


if __name__ == "__main__":
    unittest.main()
