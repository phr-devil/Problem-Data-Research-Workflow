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
                     "只有用户明确要求绘图才能实际渲染", "SEALED访问"):
            # Palette metadata never authorizes image generation.
            with self.subTest(name=name):
                self.assertIn(name, policy)

    def test_figure_evidence_and_output_integrity_are_scoped(self):
        policy = (ROOT / "FIGURE_POLICY.md").read_text(encoding="utf-8")
        for term in ("independent_unit", "missing_policy", "uncertainty_definition",
                     "selection_history", "SVG+PNG", "单一成功文件误报", "不新增授权门槛"):
            with self.subTest(term=term):
                self.assertIn(term, policy)

    def test_figure_request_does_not_grant_other_authorizations(self):
        policy = (ROOT / "FIGURE_POLICY.md").read_text(encoding="utf-8")
        self.assertIn("绘图授权**独立于论文写作授权**", policy)
        self.assertIn("不授予数据下载", policy)


    def test_academic_diagram_style_entry_and_reference(self):
        policy = (ROOT / "FIGURE_POLICY.md").read_text(encoding="utf-8")
        style = (ROOT / "ACADEMIC_DIAGRAM_STYLE.md").read_text(encoding="utf-8")
        self.assertIn("[ACADEMIC_DIAGRAM_STYLE.md](ACADEMIC_DIAGRAM_STYLE.md)", policy)
        self.assertIn("仅用户授权出图后", policy)
        self.assertIn("仅用户明确授权", style)
        self.assertIn("academic-diagram", style)
        for name in ("02-maskgct.png", "05-janus.png", "03-cut3r.png",
                     "01-loftup.png", "04-llada.png", "06-transfusion.png"):
            with self.subTest(reference=name):
                self.assertIn(name, style)
        self.assertIn("真正打开并观察", style)

    def test_academic_diagram_scientific_coverage_contract(self):
        style = (ROOT / "ACADEMIC_DIAGRAM_STYLE.md").read_text(encoding="utf-8")
        for marker in ("MUST_SHOW", "关键科学关系 → 可核的来源 → 图中模块/箭头/视觉编码",
                       "CAPTION_OR_TEXT", "OMIT", "SCIENTIFIC_COVERAGE_INCOMPLETE",
                       "不能用“简洁”作为删掉关键机制的理由"):
            with self.subTest(marker=marker):
                self.assertIn(marker, style)
        self.assertIn("不另建长期记录", style)
        self.assertIn("不能替代图中应可见的核心机制", style)

    def test_academic_diagram_rejects_visual_overload_without_new_permissions(self):
        style = (ROOT / "ACADEMIC_DIAGRAM_STYLE.md").read_text(encoding="utf-8")
        for marker in ("COMPLEXITY_REVIEW", "重复标签", "局部拥挤",
                       "不得删除任何 MUST_SHOW 关系", "同一已授权图片",
                       "不设固定框数", "实际渲染", "逐条追踪箭头",
                       "不另启实验", "不能直接宣称视觉 QA 完成"):
            with self.subTest(marker=marker):
                self.assertIn(marker, style)
        self.assertIn("不授予安装、计算、自动绘图或投稿权限", style)

if __name__ == "__main__":
    unittest.main()
