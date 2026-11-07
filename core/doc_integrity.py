"""Optional read-only integrity check for two PD-RW Markdown files.

Checks structure/IDs only. It does not verify scientific truth, permissions,
source Runs, image output or manuscript writing. Never writes or scans data.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

CHAPTER = re.compile(r"^## (\d+)\. ")
SUB = re.compile(r"^### (\d+)\.(\d+) ")
SEC = re.compile(r"^- SEC_ID:\s*(SEC-[A-Za-z0-9_-]+)\s*$")
EXP = re.compile(r"^### (EXP-[A-Za-z0-9_-]+)(?:\b|｜)")
EXPR = re.compile(r"\bEXP-[A-Za-z0-9_-]+\b")
SECR = re.compile(r"\bSEC-[A-Za-z0-9_-]+\b")
GAP_DEF = re.compile(r"^- GAP_ID:\s*(GAP-[A-Za-z0-9_-]+)(?:\s|$)")
GAP_REF = re.compile(r"\bGAP-[A-Za-z0-9_-]+\b")


def _lines(content: str) -> list[tuple[int, str]]:
    out = []
    fence = None
    for n, value in enumerate(content.splitlines(), 1):
        mark = re.match(r"^\s*((?:\x60{3,}|~{3,}))", value)
        if mark:
            token = mark.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            out.append((n, value))
    return out


def inspect_text(record: str | None, blueprint: str | None) -> list[dict]:
    findings = []
    record_ids, section_ids, gap_ids = set(), set(), set()

    def issue(level, code, file, line=0, detail=""):
        findings.append(dict(level=level, code=code, file=file, line=line, detail=detail))

    if record is None:
        issue("INFO", "RECORD_NOT_PRESENT", "RESEARCH_RECORD.md",
              detail="Legacy/no project record: rely on genuine STATE/Run.")
    else:
        lines = _lines(record)
        if sum(bool(re.match(r"^# (?!#)\S", s)) for _, s in lines) != 1:
            issue("ERROR", "RECORD_H1_COUNT", "RESEARCH_RECORD.md")
        snap = next((n for n, s in lines if s.startswith("## 0. ")), 0)
        hist = next((n for n, s in lines if s.startswith("## 5. ")), 0)
        if not snap:
            issue("WARN", "SNAPSHOT_NOT_FOUND", "RESEARCH_RECORD.md")
        if not hist:
            issue("WARN", "HISTORY_NOT_FOUND", "RESEARCH_RECORD.md")
        if hist and snap and hist <= snap:
            issue("ERROR", "HISTORY_BEFORE_SNAPSHOT", "RESEARCH_RECORD.md", hist)
        for n, s in lines:
            gap = GAP_DEF.match(s)
            if gap:
                gid = gap.group(1)
                if gid in gap_ids:
                    issue("WARN", "DUPLICATE_GAP_ID", "RESEARCH_RECORD.md", n, gid)
                gap_ids.add(gid)
            match = EXP.match(s)
            if match:
                eid = match.group(1)
                if eid in record_ids:
                    issue("ERROR", "DUPLICATE_EXP_ID", "RESEARCH_RECORD.md", n, eid)
                record_ids.add(eid)
                if hist and n < hist:
                    issue("WARN", "EVENT_BEFORE_HISTORY", "RESEARCH_RECORD.md", n, eid)

    if blueprint is None:
        issue("INFO", "BLUEPRINT_NOT_PRESENT", "PAPER_BLUEPRINT.md",
              detail="No paper plan yet/legacy project: do not force migration.")
    else:
        lines = _lines(blueprint)
        if sum(bool(re.match(r"^# (?!#)\S", s)) for _, s in lines) != 1:
            issue("ERROR", "BLUEPRINT_H1_COUNT", "PAPER_BLUEPRINT.md")
        chapter, pending, pending_line = None, False, 0
        for n, s in lines:
            head = CHAPTER.match(s)
            sub = SUB.match(s)
            if s.startswith("## "):
                if pending:
                    issue("WARN", "SECTION_WITHOUT_ID", "PAPER_BLUEPRINT.md", pending_line)
                chapter = int(head.group(1)) if head else None
                pending = False
            elif s.startswith("### "):
                if pending:
                    issue("WARN", "SECTION_WITHOUT_ID", "PAPER_BLUEPRINT.md", pending_line)
                pending = bool(sub)
                pending_line = n
                if sub and int(sub.group(1)) != chapter:
                    issue("ERROR", "SUBSECTION_PARENT_MISMATCH", "PAPER_BLUEPRINT.md", n, s)
            match = SEC.match(s)
            if match:
                sid = match.group(1)
                if sid in section_ids:
                    issue("ERROR", "DUPLICATE_SEC_ID", "PAPER_BLUEPRINT.md", n, sid)
                section_ids.add(sid)
                if pending:
                    pending = False
        if pending:
            issue("WARN", "SECTION_WITHOUT_ID", "PAPER_BLUEPRINT.md", pending_line)

    if record is not None and blueprint is not None:
        for gap in sorted(set(GAP_REF.findall(blueprint)) - gap_ids):
            issue("WARN", "GAP_NOT_DEFINED_IN_RECORD", "PAPER_BLUEPRINT.md",
                  detail=gap + " is optional; check source before reusing.")
        for exp in sorted(set(EXPR.findall(blueprint)) - record_ids):
            issue("WARN", "EXP_NOT_IN_RECORD", "PAPER_BLUEPRINT.md",
                  detail=exp + " may be a valid external/legacy reference; verify source.")
        for sid in sorted(set(SECR.findall(record)) - section_ids):
            issue("WARN", "SEC_NOT_IN_BLUEPRINT", "RESEARCH_RECORD.md",
                  detail=sid + " may be a previous subsection; verify source.")
    return findings


def check_project(project: Path, record="RESEARCH_RECORD.md",
                  blueprint="PAPER_BLUEPRINT.md") -> list[dict]:
    root = project.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("project must be a directory")

    def load(rel):
        if not rel or Path(rel).is_absolute():
            raise ValueError("document path must be project-relative")
        path = (root / rel).resolve()
        if not path.is_relative_to(root):
            raise ValueError("document outside project directory")
        if not path.is_file():
            return None
        if path.stat().st_size > 4 * 1024 * 1024:
            raise ValueError("document too large for optional lint")
        return path.read_text(encoding="utf-8")

    return inspect_text(load(record), load(blueprint))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--record", default="RESEARCH_RECORD.md")
    parser.add_argument("--blueprint", default="PAPER_BLUEPRINT.md")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        findings = check_project(args.project, args.record, args.blueprint)
    except (OSError, ValueError, UnicodeError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
    else:
        if not findings:
            print("PASS: no structural/ID issues detected (scientific validity NOT checked).")
        for x in findings:
            print("{level} {code} {file}:{line} {detail}".format(**x))
    return int(any(x["level"] == "ERROR" for x in findings))


if __name__ == "__main__":
    raise SystemExit(main())
