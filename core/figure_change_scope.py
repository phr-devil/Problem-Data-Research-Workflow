"""Read-only change-scope advice for one explicitly requested academic diagram.

Compares two compact per-figure JSON design specs. Never accesses research data,
imports a renderer, creates figures, or grants permissions. Agent must verify
source hashes against the current real files before trusting cached semantics.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SCHEMA = "pd-rw-figure-spec-v1"
GROUPS = (
    ("SCIENTIFIC_CHANGE", lambda s: s.get("scientific")),
    ("SOURCE_CHANGE", lambda s: s.get("sources")),
    ("LAYOUT_CHANGE", lambda s: (s.get("design", {}).get("reference_path"),
                                s.get("design", {}).get("layout_family"),
                                s.get("design", {}).get("nodes_geometry"))),
    ("LABEL_CHANGE", lambda s: s.get("design", {}).get("labels")),
    ("STYLE_OR_ICON_CHANGE", lambda s: (s.get("design", {}).get("theme_fingerprint"),
                                       s.get("design", {}).get("icons"))),
    ("EXPORT_TARGET_CHANGE", lambda s: s.get("outputs")),
)
CHECKS = {
    "SCIENTIFIC_CHANGE": ("ALL_MUST_SHOW_AND_SCIENCE", "ALL_CONNECTORS"),
    "SOURCE_CHANGE": ("REAL_SOURCE_AND_CLAIMS", "AFFECTED_SCIENCE_AND_CONNECTORS"),
    "SOURCE_UNVERIFIED": ("REAL_SOURCE_AND_CLAIMS",),
    "LAYOUT_CHANGE": ("ALL_AFFECTED_CONNECTORS", "GLOBAL_LAYOUT"),
    "LABEL_CHANGE": ("CHANGED_LABELS_BOXES_ADJACENT_CONNECTORS",),
    "STYLE_OR_ICON_CHANGE": ("FONT_COLOR_CONTRAST_AND_AFFECTED_LAYOUT",),
    "EXPORT_TARGET_CHANGE": ("OUTPUT_PAIR_INTEGRITY",),
    "PRIOR_QA_UNVERIFIED": ("RECHECK_PRIOR_UNVERIFIED_ITEMS",),
}


def _validate(spec: dict) -> None:
    if not isinstance(spec, dict) or spec.get("schema_version") != SCHEMA:
        raise ValueError("expected pd-rw-figure-spec-v1 JSON object")
    if not isinstance(spec.get("figure_id"), str) or not spec["figure_id"].strip():
        raise ValueError("nonempty figure_id required")
    for key in ("scientific", "sources", "design", "outputs", "qa"):
        if not isinstance(spec.get(key), dict):
            raise ValueError(f"{key} must be a JSON object")


def advise(before: dict | None, after: dict) -> dict:
    _validate(after)
    if before is not None:
        _validate(before)
        if before["figure_id"] != after["figure_id"]:
            raise ValueError("cannot compare different figure IDs")
    if before is None:
        flags = ["FIRST_RENDER"]
        checks = ["ALL_MUST_SHOW_AND_SCIENCE", "ALL_CONNECTORS",
                  "GLOBAL_LAYOUT", "FINAL_PAPER_WIDTH_VISUAL", "OUTPUT_PAIR_INTEGRITY"]
    else:
        flags = [name for name, selector in GROUPS
                 if selector(before) != selector(after)]
        fingerprint = after["sources"].get("source_fingerprint")
        if not isinstance(fingerprint, str) or not fingerprint.strip() or fingerprint == "UNKNOWN":
            flags.append("SOURCE_UNVERIFIED")
        qa = after["qa"]
        if any(qa.get(key) != "PASS" for key in ("science_qa", "connectors_qa", "visual_qa")):
            flags.append("PRIOR_QA_UNVERIFIED")
        checks = []
        for name in flags:
            checks.extend(CHECKS.get(name, ()))
        if flags:
            checks.extend(("FINAL_PAPER_WIDTH_VISUAL", "OUTPUT_PAIR_INTEGRITY"))
    return {
        "figure_id": after["figure_id"],
        "change_flags": flags or ["NO_SPEC_CHANGE"],
        "suggested_checks": list(dict.fromkeys(checks)),
        "needs_new_design": before is None or "SCIENTIFIC_CHANGE" in flags,
        "note": ("A scope hint only. Verify current real source references and original user "
                 "figure request; all actual final exports require visual inspection. "
                 "No file is rendered or modified.")
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", type=Path, help="previous saved spec, omitted on first design")
    parser.add_argument("--after", type=Path, required=True, help="current candidate spec")
    args = parser.parse_args()
    before = json.loads(args.before.read_text(encoding="utf-8")) if args.before else None
    after = json.loads(args.after.read_text(encoding="utf-8"))
    print(json.dumps(advise(before, after), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
