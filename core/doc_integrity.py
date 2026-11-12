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


# Important events are audited inside the existing research record. Untyped
# legacy events are not migrated; validation cannot certify scientific truth.
BLUEPRINT_TRIGGERS = frozenset({"DIRECTION_SET", "IMPORTANT_RUN",
    "NEGATIVE_RESULT", "CLAIM_CHANGE", "ROUTE_CHANGE", "HANDOFF"})
BLUEPRINT_EVENT_KINDS = BLUEPRINT_TRIGGERS | {"ROUTINE"}
BLUEPRINT_FIELD = re.compile(
    r"^- (EVENT_KIND|BLUEPRINT_CHECK|BLUEPRINT_SECTIONS|"
    r"BLUEPRINT_EVIDENCE|BLUEPRINT_REASON):\s*(.*?)\s*$")
DEFAULT_CHAPTERS = ("Introduction", "Related Work", "Proposed Method",
                    "Experiments", "Discussion", "Conclusion")
NO_EVIDENCE = {"", "NONE", "UNKNOWN", "NOT_RUN", "TBD", "N/A", "-"}


def _audit_blueprint_events(lines, blueprint, sections, issue):
    events, current = [], None
    for n, line in lines:
        if EXP.match(line):
            if current:
                events.append(current)
            current = (n, [])
        elif current:
            if line.startswith(("## ", "### ")):
                events.append(current)
                current = None
            else:
                current[1].append((n, line))
    if current:
        events.append(current)
    for start, body in events:
        fields = {}
        for n, line in body:
            m = BLUEPRINT_FIELD.match(line)
            if m:
                key, val = m.groups()
                if key in fields:
                    issue("ERROR", "BLUEPRINT_AUDIT_DUPLICATE_FIELD",
                          "RESEARCH_RECORD.md", n, key)
                fields[key] = val.strip()
        kind = fields.get("EVENT_KIND")
        if kind is None:
            continue  # Older free-text events are backward compatible.
        if kind not in BLUEPRINT_EVENT_KINDS:
            issue("ERROR", "BLUEPRINT_EVENT_KIND_INVALID",
                  "RESEARCH_RECORD.md", start, kind)
            continue
        if kind == "ROUTINE":
            continue
        if blueprint is None:
            issue("ERROR", "BLUEPRINT_REQUIRED_FOR_EVENT",
                  "RESEARCH_RECORD.md", start, kind)
        status = fields.get("BLUEPRINT_CHECK", "")
        if status not in ("UPDATED", "NO_CHANGE_NEEDED"):
            issue("ERROR", "BLUEPRINT_CHECK_MISSING_OR_INVALID",
                  "RESEARCH_RECORD.md", start, kind)
        raw_sections = fields.get("BLUEPRINT_SECTIONS", "")
        ids = set(SECR.findall(raw_sections))
        if not ids and not (status == "NO_CHANGE_NEEDED" and raw_sections == "NONE"):
            issue("ERROR", "BLUEPRINT_AFFECTED_SECTIONS_MISSING",
                  "RESEARCH_RECORD.md", start, raw_sections)
        if raw_sections != "NONE" and re.sub(
                r"[\s,;|/]+", "", SECR.sub("", raw_sections)):
            issue("ERROR", "BLUEPRINT_AFFECTED_SECTIONS_INVALID",
                  "RESEARCH_RECORD.md", start, raw_sections)
        for sid in sorted(ids - sections):
            issue("ERROR", "BLUEPRINT_AFFECTED_SECTION_UNKNOWN",
                  "RESEARCH_RECORD.md", start, sid)
        evidence = fields.get("BLUEPRINT_EVIDENCE", "")
        if evidence.upper() in NO_EVIDENCE or len(evidence) < 5:
            issue("ERROR", "BLUEPRINT_EVIDENCE_MISSING",
                  "RESEARCH_RECORD.md", start, kind)
        reason = fields.get("BLUEPRINT_REASON", "")
        if reason.upper() in NO_EVIDENCE or len(reason) < 12:
            issue("ERROR", "BLUEPRINT_REASON_MISSING",
                  "RESEARCH_RECORD.md", start, kind)


def _audit_claim_index(lines, sections, issue):
    inside = schema = False
    for n, line in lines:
        if line.startswith("## "):
            inside = ("Claim–Evidence–Section Index" in line or
                      "Claim-Evidence-Section Index" in line)
            schema = False
            continue
        if not inside or not line.startswith("|"):
            continue
        cells = [v.strip() for v in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        if "Claim ID" in cells[0] and "Section ID" in cells[1]:
            schema = True
            continue
        if not schema:
            continue
        m = re.match(r"^(C\d+|CLM-[A-Za-z0-9_-]+)\b", cells[0])
        if not m:
            continue
        cid = m.group(1)
        ids = set(SECR.findall(cells[1]))
        if not ids:
            issue("ERROR", "CLAIM_SECTION_MAPPING_MISSING",
                  "PAPER_BLUEPRINT.md", n, cid)
        for sid in sorted(ids - sections):
            issue("ERROR", "CLAIM_SECTION_MAPPING_UNKNOWN",
                  "PAPER_BLUEPRINT.md", n, cid + " -> " + sid)
        if cells[2].upper() in NO_EVIDENCE:
            if any(w in cells[3].upper() for w in ("SUPPORTED", "CONFIRMED", "VERIFIED")):
                issue("ERROR", "SUPPORTED_CLAIM_WITHOUT_EVIDENCE",
                      "PAPER_BLUEPRINT.md", n, cid)
            else:
                issue("WARN", "CLAIM_EVIDENCE_UNRESOLVED",
                      "PAPER_BLUEPRINT.md", n, cid)


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
    record_lines = []

    def issue(level, code, file, line=0, detail=""):
        findings.append(dict(level=level, code=code, file=file, line=line, detail=detail))

    if record is None:
        issue("INFO", "RECORD_NOT_PRESENT", "RESEARCH_RECORD.md",
              detail="Legacy/no project record: rely on genuine STATE/Run.")
    else:
        lines = _lines(record)
        record_lines = lines
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

    if blueprint is not None:
        bp_lines = _lines(blueprint)
        title = next((s for _, s in bp_lines if s.startswith("# ")), "")
        if re.match(r"^# PAPER_BLUEPRINT(?:\s|[｜:])", title):
            headings = [(int(m.group(1)), m.group(2).strip())
                        for _, s in bp_lines if
                        (m := re.match(r"^## (\d+)\. (.+)$", s))]
            if tuple(headings) != tuple(enumerate(DEFAULT_CHAPTERS, 1)):
                approval = re.search(
                    r"结构例外用户确认原始消息指针[^\n]*?：([^\n]+)", blueprint)
                has_ref = bool(approval and
                    approval.group(1).strip().upper() not in ("", "NONE", "UNKNOWN"))
                issue("WARN" if has_ref else "ERROR",
                      "BLUEPRINT_SIX_CHAPTER_DEVIATION", "PAPER_BLUEPRINT.md",
                      detail="Author-approved exceptions need original-message verification.")
            chapter_no = None
            for n, s in bp_lines:
                if s.startswith("## "):
                    m = CHAPTER.match(s)
                    chapter_no = int(m.group(1)) if m else None
                elif s.startswith("### ") and chapter_no in (1, 6):
                    issue("ERROR", "BLUEPRINT_INTRO_CONCLUSION_SUBSECTION",
                          "PAPER_BLUEPRINT.md", n, s)
        _audit_claim_index(bp_lines, section_ids, issue)
    if record is not None:
        _audit_blueprint_events(record_lines, blueprint, section_ids, issue)


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
