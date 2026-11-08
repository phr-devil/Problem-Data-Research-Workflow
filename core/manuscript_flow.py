"""Read-only structural locator for manuscript Introduction prose (.md/.txt/.docx).

This is NOT a scientific quality, originality, or AI-authorship detector.
It never accesses research datasets, writes the manuscript, or decides
paragraph importance. Paragraph lengths are descriptive only.
Run: python -m core.manuscript_flow MANUSCRIPT_TEXT.md [--output report.json]
"""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

HEADING = re.compile(r"^\s*(#{1,6})\s+(.+?)\s*#*\s*$")
BULLET = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")
NUMBER = re.compile(r"^\d+(?:\.\d+)*(?:\.)?\s+")
WORD = re.compile(r"\b[\w]+(?:[-'][\w]+)*\b", re.UNICODE)
MAIN_SECTIONS = {
    "related work", "background", "literature review", "methods", "materials and methods",
    "methodology", "proposed method", "proposed approach", "experiments",
    "experimental evaluation", "experimental results", "results", "results and discussion",
    "discussion", "conclusion", "conclusions", "references", "bibliography",
    "acknowledgments", "acknowledgements", "declarations", "figures",
}
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def clean_title(text: str) -> str:
    return NUMBER.sub("", text.strip()).strip().rstrip(":").casefold()


def _read_markdown(path: Path) -> list[dict]:
    rows = []
    pending = []
    first = None

    def flush():
        nonlocal pending, first
        if pending:
            rows.append({"kind": "prose", "text": " ".join(pending),
                         "location": first, "level": None})
            pending, first = [], None

    for i, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        h = HEADING.fullmatch(raw)
        if h:
            flush()
            rows.append({"kind": "heading", "text": h.group(2).strip(),
                         "location": i, "level": len(h.group(1))})
        elif not line:
            flush()
        elif BULLET.match(raw):
            flush()
            rows.append({"kind": "list", "text": line, "location": i, "level": None})
        elif path.suffix.lower() == ".txt" and (
                clean_title(line) in MAIN_SECTIONS | {"introduction"} or
                re.match(r"^\d+(?:\.\d+)+\s+\S", line)):
            flush()
            rows.append({"kind": "heading", "text": line, "location": i,
                         "level": 1 if re.match(r"^\d+\.\s", line) else 2})
        else:
            if not pending:
                first = i
            pending.append(line)
    flush()
    return rows


def _read_docx(path: Path) -> list[dict]:
    with zipfile.ZipFile(path) as docx:
        root = ET.fromstring(docx.read("word/document.xml"))
    body = root.find(W + "body")
    if body is None:
        return []
    rows = []
    for i, para in enumerate(body.iter(W + "p"), 1):
        value = "".join(x.text or "" for x in para.iter(W + "t")).strip()
        if not value:
            continue
        ppr = para.find(W + "pPr")
        style = ppr.find(W + "pStyle") if ppr is not None else None
        style_id = (style.get(W + "val", "") if style is not None else "").casefold()
        numbered = ppr.find(W + "numPr") is not None if ppr is not None else False
        if style_id.startswith("heading") or clean_title(value) in MAIN_SECTIONS | {"introduction"}:
            match = re.search(r"\d+", style_id)
            level = int(match.group()) if match else 1
            kind = "heading"
        elif numbered or style_id.startswith(("list", "bullet")) or BULLET.match(value):
            kind, level = "list", None
        else:
            kind, level = "prose", None
        rows.append({"kind": kind, "text": value, "location": i, "level": level})
    return rows


def inspect_blocks(rows: list[dict]) -> dict:
    """Locate Introduction section and actionable formatting flags; no quality score."""
    active = False
    found = False
    intro_level = None
    flags = []
    lengths = []
    for row in rows:
        title = clean_title(row["text"]) if row["kind"] == "heading" else None
        if not active:
            if row["kind"] == "heading" and title == "introduction":
                found, active, intro_level = True, True, row["level"]
            continue
        if row["kind"] == "heading":
            # A new major recognized section ends the Introduction. A smaller
            # heading nested within the Introduction is a formatting risk.
            is_explicit_subsection = bool(re.match(r"^\\d+\\.\\d+(?:\\.|\\s)", row["text"]))
            if (title in MAIN_SECTIONS and not is_explicit_subsection and
                    (row["level"] is None or row["level"] <= intro_level)):
                break
            flags.append({"code": "INTRO_SUBHEADING", "location": row["location"],
                          "excerpt": row["text"][:180]})
        elif row["kind"] == "list":
            flags.append({"code": "INTRO_LIST_ITEM", "location": row["location"],
                          "excerpt": row["text"][:180]})
        elif row["kind"] == "prose":
            lengths.append(len(WORD.findall(row["text"])))
    return {
        "format": "pdrw-manuscript-flow-v1",
        "scope": "INTRODUCTION_STRUCTURAL_LOCATOR_ONLY",
        "intro_identified": found,
        "status": ("INTRO_NOT_IDENTIFIED" if not found else
                   "INTRO_FORMAT_REVIEW_REQUIRED" if flags else
                   "INTRO_NO_STRUCTURAL_FLAGS"),
        "intro_paragraph_count": len(lengths),
        "intro_paragraph_word_counts": lengths,
        "word_counts_are": "DESCRIPTIVE_ONLY_NOT_LENGTH_TARGETS",
        "findings": flags,
        "note": ("A title or list flag requires contextual review and respects approved "
                 "structure and journal rules. No finding does NOT verify scientific logic, "
                 "innovation depth, paragraph quality or user authorization. "
                 "No fixed paragraph-length or uniformity threshold is applied.")
    }


def scan_file(filename: str | Path) -> dict:
    path = Path(filename)
    ext = path.suffix.lower()
    if ext not in {".md", ".txt", ".docx"}:
        raise ValueError("Only .md/.txt/.docx; PDF requires a separate authorized text extraction")
    blocks = _read_docx(path) if ext == ".docx" else _read_markdown(path)
    result = inspect_blocks(blocks)
    result["source"] = str(path)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = scan_file(args.file)
    payload = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
