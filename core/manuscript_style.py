"""Heuristic manuscript style locator, not an AI detector.
Run: python -m core.manuscript_style scan paper.md --output style.json
     python -m core.manuscript_style compare before.json after.json
"""
from __future__ import annotations
import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

TOKEN = re.compile(r"\b[\w]+(?:[-'][\w]+)*\b", re.UNICODE)
SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z"“(\[])')
RULES = {
    "DOUBLE_HEDGE": re.compile(r"\b(?:may\s+potentially|might\s+possibly|could\s+possibly|may\s+perhaps)\b", re.I),
    "META_FILLER": re.compile(r"\b(?:it is worth noting that|it should be noted that|it is important to note that|it can be seen that)\b", re.I),
    "HYPE_WITHOUT_SPECIFICS": re.compile(r"\b(?:holds (?:great|immense) promise|plays a (?:crucial|pivotal) role|demonstrates (?:the )?(?:great|enormous) potential)\b", re.I),
    "GENERIC_BOILERPLATE": re.compile(r"\b(?:in (?:today's|the) rapidly (?:evolving|changing) (?:world|landscape)|this study underscores the importance of)\b", re.I),
    # High-confidence prose smells are contextual review prompts, not banned expressions.
    "CHAT_OUTLINE_LABEL": re.compile(
        r"^\s*(?:(?:the\s+)?(?:key\s+)?(?:challenge|solution|insight|our\s+advantages?|motivation|contribution|takeaway|evidence))\s*:\s+", re.I),
    "GENERIC_RESEARCH_PROMISE": re.compile(
        r"\b(?:paves? the way for|sheds? light on|opens? (?:up )?(?:new )?avenues? for future research)\b", re.I),
    "TEMPLATE_RESEARCH_FRAMING": re.compile(
        r"\b(?:with the rapid (?:advancement|development|evolution) of|our contributions? (?:are|can be summarized) as follows)\b", re.I),
}
TRANSITION = re.compile(r"^(moreover|furthermore|additionally|in addition)[,\s]+", re.I)
REFERENCES = re.compile(r"^(?:#{1,6}\s*)?(?:references|bibliography)\s*:?\s*$", re.I)
HEADING = re.compile(r"^\s*#{1,6}\s+")


def paragraphs_from_file(filename: str | Path) -> list[str]:
    path = Path(filename)
    if path.suffix.lower() == ".docx":
        uri = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        with zipfile.ZipFile(path) as archive:
            root = ET.fromstring(archive.read("word/document.xml"))
        body = root.find(f"{{{uri}}}body")
        if body is None:
            return []
        return ["".join(t.text or "" for t in p.iter(f"{{{uri}}}t")).strip()
                for p in body.iter(f"{{{uri}}}p")]
    if path.suffix.lower() not in (".md", ".txt"):
        raise ValueError("Accepts .md/.txt/.docx only; extract PDF separately")
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"(?ms)^\x60{3}.*?^\x60{3}\s*$", "", text)
    return [p.strip() for p in re.split(r"\n\s*\n+", text)]


def scan_paragraphs(paragraphs: list[str]) -> dict:
    sentences = []
    total_words = 0
    in_refs = False
    for p_index, paragraph in enumerate(paragraphs, 1):
        lines = [line.strip() for line in paragraph.splitlines()]
        if any(REFERENCES.fullmatch(line) for line in lines):
            in_refs = True
        if in_refs or not paragraph.strip():
            continue
        paragraph = "\n".join(line for line in lines if not HEADING.match(line))
        paragraph = re.sub(r"\[[A-Z]+:[^\]]+\]", "", paragraph)
        paragraph = re.sub(r"https?://\S+", "", paragraph)
        for number, sentence in enumerate(SPLIT.split(paragraph), 1):
            sentence = sentence.strip()
            words = len(TOKEN.findall(sentence))
            if not words:
                continue
            total_words += words
            flags = [name for name, pat in RULES.items() if pat.search(sentence)]
            if words > 55:
                flags.append("LONG_SENTENCE_REVIEW")
            sentences.append({"paragraph": p_index, "sentence": number, "text": sentence,
                              "words": words, "flags": flags})
    openers = {}
    for item in sentences:
        match = TRANSITION.match(item["text"])
        if match:
            openers.setdefault(match.group(1).lower(), []).append(item)
    for same in openers.values():
        if len(same) >= 3:
            for item in same:
                item["flags"].append("REPEATED_TRANSITION")
    flagged = [x for x in sentences if x["flags"]]
    flagged_words = sum(x["words"] for x in flagged)
    return {"format": "pdrw-style-audit-v1", "method": "HEURISTIC_LOCATOR_NOT_AI_DETECTOR",
            "total_prose_words": total_words, "flagged_sentence_words": flagged_words,
            "style_flagged_word_coverage_percent": round(100 * flagged_words / total_words, 2) if total_words else None,
            "external_ai_rate": None, "flagged_sentences": flagged,
            "limitations": "Heuristic English prose flags need contextual review. Coverage is not AI-authorship probability. DOCX extraction ignores footnotes and figures."}


def scan_file(filename: str | Path) -> dict:
    report = scan_paragraphs(paragraphs_from_file(filename))
    report["source"] = str(filename)
    return report


def compare_reports(before: dict, after: dict) -> dict:
    for report in (before, after):
        if report.get("format") != "pdrw-style-audit-v1":
            raise ValueError("Unsupported style report")
    b, a = before.get("style_flagged_word_coverage_percent"), after.get("style_flagged_word_coverage_percent")
    return {"before_coverage_percent": b, "after_coverage_percent": a,
            "change_percentage_points": round(a - b, 2) if a is not None and b is not None else None,
            "note": "Style metric only; scientific meaning, references and claims require separate review."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    scan = sub.add_parser("scan")
    scan.add_argument("file")
    scan.add_argument("--output")
    comp = sub.add_parser("compare")
    comp.add_argument("before")
    comp.add_argument("after")
    args = parser.parse_args()
    if args.command == "scan":
        result = scan_file(args.file)
        output = args.output
    else:
        result = compare_reports(json.loads(Path(args.before).read_text(encoding="utf-8")),
                                 json.loads(Path(args.after).read_text(encoding="utf-8")))
        output = None
    data = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if output:
        Path(output).write_text(data, encoding="utf-8")
    else:
        print(data, end="")


if __name__ == "__main__":
    main()
