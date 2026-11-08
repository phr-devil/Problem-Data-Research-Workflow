"""Offline *warning* checks for manuscript rewrites and claim provenance.

This is not a semantic verifier, scientific peer review, or independent confirmation.
No network, original experiment data, or SEALED access is used.

Usage:
  python -m core.manuscript_claim_guard compare original.md revised.md --output alerts.json
  python -m core.manuscript_claim_guard provenance declared_claim_sources.json --output alerts.json
"""
from __future__ import annotations

import argparse
from collections import Counter
from difflib import SequenceMatcher
import json
from pathlib import Path
import re

from core.manuscript_style import paragraphs_from_file

NUMERIC = re.compile(
    r"(?<![\w.])(?:[pP]\s*(?:=|<|>|≤|≥)\s*)?[+-]?(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?%?(?![\w])"
)
NEGATION = re.compile(r"\b(?:not|no|never|neither|without|cannot|failed to)\b", re.I)
CAUSAL = re.compile(r"\b(?:caus(?:e|es|ed)|driv(?:e|es|en)|results? in|leads? to|due to)\b", re.I)
ASSOCIATIVE = re.compile(r"\b(?:associated with|correlated with|linked to)\b", re.I)
SIGNIFICANT = re.compile(r"\b(?:statistically significant|significant|nonsignificant|non-significant)\b", re.I)
DATA_ROLE = re.compile(r"\b(?:DEV|VAL|VALIDATION|CONFIRMATION|SEALED|HELD.OUT|TEST)\b", re.I)
REF_HEADING = re.compile(r"^\s*(?:#{1,6}\s*)?(?:References|Bibliography)\s*:?\s*$", re.I)


def _prose(path: str) -> list[str]:
    paragraphs = paragraphs_from_file(path)
    result = []
    for paragraph in paragraphs:
        if any(REF_HEADING.fullmatch(line.strip()) for line in paragraph.splitlines()):
            break
        if paragraph.strip():
            result.append(paragraph)
    return result


def _tokens(regex: re.Pattern[str], text: str) -> Counter[str]:
    return Counter(re.sub(r"\s+", "", x.lower()) for x in regex.findall(text))


def _diff(before: str, after: str) -> list[str]:
    alerts = []
    if _tokens(NUMERIC, before) != _tokens(NUMERIC, after):
        alerts.append("NUMERIC_OR_STATISTIC_CHANGED")
    if _tokens(NEGATION, before) != _tokens(NEGATION, after):
        alerts.append("NEGATION_CHANGED")
    if _tokens(DATA_ROLE, before) != _tokens(DATA_ROLE, after):
        alerts.append("DATA_ROLE_WORD_CHANGED")
    if CAUSAL.search(after) and not CAUSAL.search(before):
        alerts.append("CAUSAL_LANGUAGE_ADDED")
    if ASSOCIATIVE.search(before) and not ASSOCIATIVE.search(after) and CAUSAL.search(after):
        alerts.append("ASSOCIATION_TO_CAUSAL_POSSIBLE")
    if _tokens(SIGNIFICANT, before) != _tokens(SIGNIFICANT, after):
        alerts.append("SIGNIFICANCE_LANGUAGE_CHANGED")
    return alerts


def compare_manuscripts(before: str, after: str) -> dict:
    old, new = _prose(before), _prose(after)
    matcher = SequenceMatcher(None, old, new, autojunk=False)
    changes = []
    for op, a0, a1, b0, b1 in matcher.get_opcodes():
        if op == "equal":
            continue
        old_text, new_text = "\n".join(old[a0:a1]), "\n".join(new[b0:b1])
        flags = _diff(old_text, new_text)
        if (a1 - a0) != (b1 - b0):
            flags.append("UNALIGNED_TEXT_REVIEW")
        if flags:
            changes.append({
                "before_paragraphs": [a0 + 1, a1],
                "after_paragraphs": [b0 + 1, b1],
                "flags": sorted(set(flags)),
                "before_excerpt": old_text[:240],
                "after_excerpt": new_text[:240],
            })
    return {
        "format": "pdrw-manuscript-guard-v1",
        "mode": "compare",
        "result": "REVIEW_REQUIRED" if changes else "NO_HEURISTIC_ALERT_NOT_PROOF",
        "flagged_changed_blocks": changes,
        "limitations": (
            "Coarse changed-paragraph lexical heuristic; not semantic equivalence. "
            "False positives and false negatives possible. Must inspect changes, "
            "scientific sources, and any major rewrite manually."
        ),
    }


def check_provenance(packet: dict) -> dict:
    """Validate declared metadata, not underlying split or experiment truth.

    Schema: {"claims":[{"claim_id":"C01","text_anchor":"...","asserted_role":
    "INDEPENDENT_CONFIRMATION","source_role":"DEV|VAL|CONFIRMATION|EXTERNAL_INDEPENDENT",
    "split_id":"S3","development_split_ids":["S1"],"selected_on_source":false,
    "protocol_frozen":true,"evidence_ref":"run/path"}]}.
    """
    rows = []
    for idx, claim in enumerate(packet.get("claims", []), 1):
        ref = claim.get("claim_id") or f"ITEM-{idx}"
        asserted = str(claim.get("asserted_role", "")).upper()
        source = str(claim.get("source_role", "")).upper()
        split = claim.get("split_id")
        development_splits = claim.get("development_split_ids", [])
        failures, unknowns = [], []
        if not isinstance(development_splits, list) or any(not isinstance(x, str) for x in development_splits):
            unknowns.append("INVALID_DEVELOPMENT_SPLIT_LIST")
            development_splits = []
        if "selected_on_source" in claim and not isinstance(claim["selected_on_source"], bool):
            unknowns.append("INVALID_SELECTION_FLAG")
        if "protocol_frozen" in claim and not isinstance(claim["protocol_frozen"], bool):
            unknowns.append("INVALID_PROTOCOL_FROZEN_FLAG")
        if asserted == "INDEPENDENT_CONFIRMATION":
            if source in {"DEV", "VALIDATION", "VAL", "EXPLORATORY"}:
                failures.append("DEVELOPMENT_OR_VALIDATION_MISLABELED_INDEPENDENT")
            if split and split in development_splits:
                failures.append("SPLIT_REUSED_FOR_DEVELOPMENT")
            if claim.get("selected_on_source") is True:
                failures.append("SELECTION_USED_CONFIRMATION_SOURCE")
            if source not in {"CONFIRMATION", "EXTERNAL_INDEPENDENT"} and not failures:
                unknowns.append("SOURCE_ROLE_NOT_INDEPENDENT_CONFIRMATION")
            for field in ("text_anchor", "evidence_ref", "split_id", "development_split_ids",
                          "selected_on_source", "protocol_frozen"):
                if field not in claim or claim[field] is None or (field != "development_split_ids" and claim[field] == ""):
                    unknowns.append("MISSING_" + field.upper())
            if claim.get("protocol_frozen") is False:
                failures.append("CONFIRMATION_PROTOCOL_NOT_FROZEN")
        else:
            unknowns.append("NOT_AN_INDEPENDENT_CONFIRMATION_ASSERTION")
        verdict = "BLOCK" if failures else ("REVIEW_REQUIRED" if unknowns else "DECLARED_METADATA_NO_CONFLICT_NOT_PROOF")
        rows.append({"claim_id": ref, "verdict": verdict, "reasons": failures + unknowns})
    return {
        "format": "pdrw-manuscript-guard-v1",
        "mode": "provenance",
        "result": "NOT_CHECKED" if not rows else ("BLOCK" if any(x["verdict"] == "BLOCK" for x in rows)
                 else "REVIEW_REQUIRED" if any(x["verdict"] == "REVIEW_REQUIRED" for x in rows)
                 else "DECLARED_METADATA_NO_CONFLICT_NOT_PROOF"),
        "items": rows,
        "limitations": (
            "Checks only supplied claim-source metadata. Cannot establish that all prose "
            "claims were mapped, that source IDs/selection history are true, or that "
            "SEALED access was authorized. Scientific and permission audit remains required."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    compare = sub.add_parser("compare")
    compare.add_argument("before")
    compare.add_argument("after")
    compare.add_argument("--output")
    provenance = sub.add_parser("provenance")
    provenance.add_argument("packet")
    provenance.add_argument("--output")
    args = parser.parse_args()
    if args.mode == "compare":
        report = compare_manuscripts(args.before, args.after)
    else:
        report = check_provenance(json.loads(Path(args.packet).read_text(encoding="utf-8")))
    out = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(out + "\n", encoding="utf-8")
    else:
        print(out)


if __name__ == "__main__":
    main()
