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
    ("DESIGN_REVIEW_CHANGE", lambda s: s.get("design", {}).get("review")),
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
    "GLOBAL_DESIGN_QA_UNVERIFIED": ("GLOBAL_DESIGN_QA",),
    "DESIGN_REVIEW_CHANGE": ("GLOBAL_DESIGN_QA", "REASSESS_LAYOUT_ROUTE"),
    "REVISION_STALLED": ("DIAGNOSE_STAGNATION", "SWITCH_EDIT_STRATEGY"),
}


def _validate(spec: dict) -> None:
    if not isinstance(spec, dict) or spec.get("schema_version") != SCHEMA:
        raise ValueError("expected pd-rw-figure-spec-v1 JSON object")
    if not isinstance(spec.get("figure_id"), str) or not spec["figure_id"].strip():
        raise ValueError("nonempty figure_id required")
    for key in ("scientific", "sources", "design", "outputs", "qa"):
        if not isinstance(spec.get(key), dict):
            raise ValueError(f"{key} must be a JSON object")
    review = spec["design"].get("review", {})
    if not isinstance(review, dict):
        raise ValueError("design.review must be an object when present")
    if review.get("issue_scope", "UNKNOWN") not in {
        "UNKNOWN", "NONE", "LOCAL", "GLOBAL_LAYOUT", "GLOBAL_CONCEPT",
        "VISUAL_ANCHORING", "SCIENTIFIC_TOPOLOGY",
    }:
        raise ValueError("invalid design.review.issue_scope")
    if not isinstance(review.get("stalled", False), bool):
        raise ValueError("design.review.stalled must be boolean")


def advise(before: dict | None, after: dict) -> dict:
    """Suggest scoped checks and a design route from declared spec state, never image pixels."""
    _validate(after)
    if before is not None:
        _validate(before)
        if before["figure_id"] != after["figure_id"]:
            raise ValueError("cannot compare different figure IDs")

    qa = after["qa"]
    review = after["design"].get("review", {})
    issue_scope = review.get("issue_scope", "UNKNOWN")
    stalled = review.get("stalled", False)
    fingerprint = after["sources"].get("source_fingerprint")
    source_unknown = not isinstance(fingerprint, str) or not fingerprint.strip() or fingerprint == "UNKNOWN"

    if before is None:
        flags = ["FIRST_RENDER"]
        checks = ["REAL_SOURCE_AND_CLAIMS", "ALL_MUST_SHOW_AND_SCIENCE",
                  "ALL_CONNECTORS", "GLOBAL_LAYOUT", "GLOBAL_DESIGN_QA",
                  "FINAL_PAPER_WIDTH_VISUAL", "OUTPUT_PAIR_INTEGRITY"]
        if source_unknown:
            flags.append("SOURCE_UNVERIFIED")
        mode = "INITIAL_DESIGN"
    else:
        flags = [name for name, selector in GROUPS
                 if selector(before) != selector(after)]
        if source_unknown:
            flags.append("SOURCE_UNVERIFIED")
        if any(qa.get(key) != "PASS" for key in ("science_qa", "connectors_qa", "visual_qa")):
            flags.append("PRIOR_QA_UNVERIFIED")
        # Absent on legacy specs: do not force bulk migration or unrelated rework.
        if "global_design_qa" in qa and qa["global_design_qa"] != "PASS":
            flags.append("GLOBAL_DESIGN_QA_UNVERIFIED")
        if stalled:
            flags.append("REVISION_STALLED")

        # Treat the stated issue as input evidence to *inspect*, not proof of visual failure.
        if "SCIENTIFIC_CHANGE" in flags or issue_scope in {
            "SCIENTIFIC_TOPOLOGY", "GLOBAL_CONCEPT", "VISUAL_ANCHORING",
        }:
            mode = "FULL_REDESIGN"
        elif issue_scope == "GLOBAL_LAYOUT" or qa.get("global_design_qa") == "FAIL":
            mode = "LAYOUT_REBUILD"
        else:
            mode = "LOCAL_EDIT"

        checks = []
        for name in flags:
            checks.extend(CHECKS.get(name, ()))
        if mode in {"LAYOUT_REBUILD", "FULL_REDESIGN"}:
            checks.extend(("REBUILD_GLOBAL_LAYOUT_WITHOUT_OLD_GEOMETRY",
                           "GLOBAL_DESIGN_QA", "ALL_AFFECTED_CONNECTORS"))
        if flags:
            checks.extend(("FINAL_PAPER_WIDTH_VISUAL", "OUTPUT_PAIR_INTEGRITY"))

    return {
        "figure_id": after["figure_id"],
        "change_flags": flags or ["NO_SPEC_CHANGE"],
        "recommended_mode": mode,
        "needs_new_design": mode in {"INITIAL_DESIGN", "LAYOUT_REBUILD", "FULL_REDESIGN"},
        "discard_prior_global_layout": mode in {"LAYOUT_REBUILD", "FULL_REDESIGN"},
        "needs_strategy_switch": bool(stalled),
        "suggested_checks": list(dict.fromkeys(checks)),
        "note": ("Read-only hint from declared spec/QA values; NOT an image-quality "
                 "measurement or rendering permission. Verify actual figure, true "
                 "scientific sources, user authorization, and final visual output. "
                 "No file is rendered or modified."),
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
