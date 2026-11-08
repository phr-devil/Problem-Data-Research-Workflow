"""Article-type outlines and optional gap-reference regression tests."""
import re
import unittest
from pathlib import Path
from core.doc_integrity import inspect_text

ROOT=Path(__file__).resolve().parents[1]

class PaperTypeAndGapTests(unittest.TestCase):
    def test_three_outline_types_without_gated_restructuring(self):
        docs=[
            ("PAPER_BLUEPRINT.md",6),
            ("PAPER_BLUEPRINT_REVIEW.md",5),
            ("PAPER_BLUEPRINT_PERSPECTIVE.md",5),
        ]
        for name,number in docs:
            with self.subTest(name=name):
                source=(ROOT/"templates"/name).read_text(encoding="utf-8")
                chapters=re.findall(r"(?m)^## (\d+)\. ",source)
                subheadings=re.findall(r"(?m)^### (\d+)\.(\d+) ",source)
                sec=re.findall(r"(?m)^- SEC_ID: (SEC-[A-Z0-9-]+)$",source)
                self.assertEqual(chapters,[str(i) for i in range(1,number+1)])
                # Introduction/Conclusion may have stable internal SEC_IDs
                # without visible second-level headings in journal prose.
                self.assertGreaterEqual(len(sec),len(subheadings))
                self.assertEqual(len(sec),len(set(sec)))
                intro=source.split("## 1. Introduction",1)[1].split("## 2.",1)[0]
                self.assertNotIn("### ",intro)
                self.assertRegex(intro,r"(?m)^- SEC_ID: SEC-[A-Z0-9-]+$")
                self.assertTrue(source.count("## 1. Introduction") == 1)
                self.assertTrue(all(any(int(ch)==int(num) for ch in chapters)
                                    for num,_ in subheadings))
                self.assertEqual([x for x in inspect_text(None,source)
                                  if x["level"]=="ERROR"],[])
                self.assertIn("非正文",source)

    def test_optional_gap_id_is_single_authoritative_source(self):
        record="# Record\n## 0. Now\n- GAP_ID: GAP-001 | DEV cross-group evidence missing\n## 5. History"
        paper="# Paper\n## 1. Intro\n### 1.1 Evidence\n- SEC_ID: SEC-X\n- Gap: GAP-001"
        findings=inspect_text(record,paper)
        self.assertNotIn("GAP_NOT_DEFINED_IN_RECORD",{x["code"] for x in findings})
        extra=paper.replace("GAP-001","GAP-999")
        warn={x["code"] for x in inspect_text(record,extra)}
        self.assertIn("GAP_NOT_DEFINED_IN_RECORD",warn)
        self.assertFalse(any(z["level"]=="ERROR" for z in inspect_text(record,extra)))

    def test_duplicate_gap_does_not_create_new_required_gate(self):
        record="# Record\n## 0. Now\n- GAP_ID: GAP-001\n- GAP_ID: GAP-001\n## 5. History"
        codes={x["code"] for x in inspect_text(record,None)}
        self.assertIn("DUPLICATE_GAP_ID",codes)
        guide=(ROOT/"DUAL_DOCUMENT_WORKFLOW.md").read_text(encoding="utf-8")
        for marker in ("CRITICAL_REVIEW","PERSPECTIVE","不强制建 GAP ID","WRITING_GATE.md"):
            self.assertIn(marker,guide)
        gate=(ROOT/"WRITING_GATE.md").read_text(encoding="utf-8")
        self.assertIn("WRITING_LOCKED",gate)

if __name__=="__main__":
    unittest.main()
