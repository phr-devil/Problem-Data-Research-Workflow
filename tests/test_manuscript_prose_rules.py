"""Offline regression for prose policy; these checks do not validate AI origin or science."""
import unittest
from pathlib import Path

from core.manuscript_style import scan_paragraphs

ROOT = Path(__file__).resolve().parents[1]


class ManuscriptProsePolicyTests(unittest.TestCase):
    def test_canonical_writing_contract_covers_all_tiers(self):
        writing = (ROOT / "MANUSCRIPT_WRITING.md").read_text(encoding="utf-8")
        qa = (ROOT / "MANUSCRIPT_QA.md").read_text(encoding="utf-8")
        for term in (
            "HARD｜明显错误", "MAJOR｜具有论证", "STYLE｜弱线索",
            "聊天/提纲痕迹", "占位符和内部日志外泄",
            "证据与学术规范", "术语精确与章节职责",
            "无信息开场/结尾", "模板句式与机械排比",
            "孤岛式段落", "内容不均衡", "章节间重复",
            "引用、图表与科学主张耦合", "不设绝对数量阈值",
            "禁止分点作答", "括号只作必要功能",
        ):
            with self.subTest(term=term):
                self.assertIn(term, writing)
        for term in (
            "反模板化三层验收", "HARD 格式/完整性",
            "HARD 科学真实性", "MAJOR 论证结构",
            "MAJOR 信息密度/准确性", "STYLE 弱线索",
            "作者批准", "不能因此自动画图", "不设任何禁词数量",
            "不允许以特定检测器得分",
        ):
            with self.subTest(term=term):
                self.assertIn(term, qa)

    def test_submission_prose_excludes_internal_project_numbers(self):
        writing = (ROOT / "MANUSCRIPT_WRITING.md").read_text(encoding="utf-8")
        qa = (ROOT / "MANUSCRIPT_QA.md").read_text(encoding="utf-8")
        for marker in ("投稿正文只能使用自然语言描述研究", "Project 19",
                       "EXP-003", "SEC-INTRO-01", "纯文字、连贯段落",
                       "公开数据集"):
            self.assertIn(marker, writing)
        for marker in ("内部项目编号与编号式稿件表达：HARD 检查",
                       "纯文字连贯学术叙述", "不得机械搜索替换"):
            self.assertIn(marker, qa)

    def test_authorization_and_scientific_boundaries_stay_intact(self):
        for path in ("MANUSCRIPT_WRITING.md", "MANUSCRIPT_QA.md"):
            content = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn("SEALED", content)
            self.assertIn("证据", content)
            self.assertIn("授权", content)
        self.assertIn("WRITING_LOCKED",
                      (ROOT / "WRITING_GATE.md").read_text(encoding="utf-8"))
        self.assertIn("正文不得清单化或括号堆砌",
                      (ROOT / "AGENTS.md").read_text(encoding="utf-8"))

    def test_high_confidence_templates_prompt_review(self):
        paragraphs = [
            "Challenge: Our approach solves everything.",
            "This study sheds light on an important topic.",
            "With the rapid advancement of artificial intelligence, many tasks changed.",
            "Our contributions are as follows: we introduce a new module.",
        ]
        report = scan_paragraphs(paragraphs)
        codes = {flag for x in report["flagged_sentences"] for flag in x["flags"]}
        self.assertIn("CHAT_OUTLINE_LABEL", codes)
        self.assertIn("GENERIC_RESEARCH_PROMISE", codes)
        self.assertIn("TEMPLATE_RESEARCH_FRAMING", codes)
        self.assertIsNone(report["external_ai_rate"])
        self.assertEqual(report["method"], "HEURISTIC_LOCATOR_NOT_AI_DETECTOR")

    def test_legitimate_terminology_and_equations_not_auto_rejected(self):
        report = scan_paragraphs([
            "Inertial measurement unit (IMU) signals were segmented at 60 Hz.",
            "The pivotal term in f(x) is the boundary condition.",
            "A robust estimator minimized the mean absolute error.",
            "The difference was significant under the stated test protocol.",
        ])
        self.assertEqual(report["flagged_sentences"], [])
        self.assertIsNone(report["external_ai_rate"])

    def test_repeat_connectors_require_context(self):
        report = scan_paragraphs([
            "Furthermore, we evaluated the signals.",
            "Furthermore, we calibrated each device.",
            "Furthermore, we examined timing.",
        ])
        self.assertTrue(all("REPEATED_TRANSITION" in item["flags"]
                            for item in report["flagged_sentences"]))
        self.assertLess(report["style_flagged_word_coverage_percent"], 101)

    def test_references_not_scanned_as_prose(self):
        report = scan_paragraphs([
            "The method was evaluated on three cohorts.",
            "References",
            "Our contributions are as follows: An Article Title.",
        ])
        self.assertFalse(report["flagged_sentences"])


if __name__ == "__main__":
    unittest.main()
