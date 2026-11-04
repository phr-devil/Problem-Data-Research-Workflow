"""Advisory pre-download research-choice preflight; no scientific ranking or authorization.

Takes Agent-authored public-source summaries ONLY. It checks omissions and
contradictions, not the truth of citations, novelty, causal identifiability,
Q2 likelihood or access to sealed data. No file reads except explicit CLI JSON.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MAX_CANDIDATES = 3
MAX_PACKET_BYTES = 256 * 1024


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def review_choice(packet: dict) -> dict:
    if not isinstance(packet, dict) or packet.get("format") != "pd-rw-search-choice-v1":
        raise ValueError("expected pd-rw-search-choice-v1 object")
    if not _nonempty(packet.get("user_scope")):
        raise ValueError("USER_SCOPE is required")
    candidates = packet.get("candidates")
    if not isinstance(candidates, list) or not 1 <= len(candidates) <= MAX_CANDIDATES:
        raise ValueError("1..3 nonempty research question candidates required")
    ids = []
    for row in candidates:
        if not isinstance(row, dict) or not all(_nonempty(row.get(k)) for k in
            ("id", "scientific_question", "importance_basis",
             "knowledge_delta_or_unknown", "decisive_unknown")):
            raise ValueError("candidate needs scientific question, importance and decisive unknown")
        ids.append(row["id"])
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate candidate id")
    chosen = packet.get("preferred_id")
    if chosen is not None and chosen not in ids:
        raise ValueError("preferred_id must refer to a candidate")
    coverage = packet.get("coverage")
    if not isinstance(coverage, dict):
        raise ValueError("coverage object required")
    rival = packet.get("contrasting_opportunity_search")
    if not isinstance(rival, dict):
        raise ValueError("contrasting_opportunity_search object required")
    data = packet.get("pre_download_data_fit")
    if not isinstance(data, dict):
        raise ValueError("pre_download_data_fit object required")

    flags = []
    if not _nonempty(coverage.get("query_families_ref")) or not _nonempty(
        coverage.get("source_families_ref")):
        flags.append("SEARCH_COVERAGE_UNDOCUMENTED")
    if coverage.get("critical_coverage_gaps"):
        flags.append("SEARCH_PARTIAL_CRITICAL_GAPS")
    contrast_status = rival.get("status")
    if contrast_status not in ("ALTERNATIVE_FOUND", "NO_BETTER_ALTERNATIVE_WITH_LIMITS",
                               "NOT_CHECKED"):
        raise ValueError("invalid contrasting search status")
    if contrast_status == "NOT_CHECKED" or not _nonempty(
        rival.get("different_premise_or_query")):
        flags.append("FIRST_SATISFICING_RISK")
    elif not _nonempty(rival.get("source_or_query_ref")):
        flags.append("CONTRASTING_SEARCH_UNSUPPORTED")
    if contrast_status == "ALTERNATIVE_FOUND" and len(candidates) == 1:
        flags.append("UNEXAMINED_COMPETING_OPPORTUNITY")
    if len(candidates) > 1 and chosen is not None and not _nonempty(
        packet.get("why_preferred_over_competitor")):
        flags.append("COMPARATIVE_REASON_MISSING")

    selected = next((r for r in candidates if r["id"] == chosen), None)
    if selected is not None:
        if selected.get("nearest_original_status") != "ORIGINAL_CHECKED" or not _nonempty(
            selected.get("nearest_original_ref")):
            flags.append("NEAREST_ORIGINAL_NOT_VERIFIED")
        if selected.get("counterevidence_status") != "CHECKED":
            flags.append("INNOVATION_FALSIFICATION_INCOMPLETE")
    else:
        flags.append("PREFERRED_NOT_SELECTED")

    fit = data.get("status")
    if fit not in ("OFFICIAL_METADATA_SUPPORTS", "UNKNOWN", "OFFICIAL_METADATA_CONTRADICTS",
                   "NOT_APPLICABLE_THEORY"):
        raise ValueError("invalid predownload data-fit status")
    if fit == "OFFICIAL_METADATA_CONTRADICTS":
        flags.append("D1_INCOMPATIBLE_WITH_PROPOSED_CLAIM")
    elif fit == "UNKNOWN":
        flags.append("D1_SCIENTIFIC_FIT_UNKNOWN")
    elif fit == "OFFICIAL_METADATA_SUPPORTS" and not all(_nonempty(data.get(k)) for k in
        ("official_source_ref", "needed_factors_and_truth", "independent_group_unit",
         "confounding_or_unknown", "legal_input_and_confirmation")):
        flags.append("D1_SCIENTIFIC_FIT_UNDOCUMENTED")

    if not _nonempty(packet.get("next_discriminating_check")):
        flags.append("NEXT_EVIDENCE_CHECK_MISSING")

    material = {"FIRST_SATISFICING_RISK", "UNEXAMINED_COMPETING_OPPORTUNITY",
                "D1_INCOMPATIBLE_WITH_PROPOSED_CLAIM", "COMPARATIVE_REASON_MISSING",
                "PREFERRED_NOT_SELECTED"}
    decision = ("REASSESS_OR_COMPARE_BEFORE_D1" if any(f in material for f in flags)
                else "PROVISIONAL_RESEARCH_CHOICE_WITH_LIMITATIONS" if flags
                else "STRUCTURALLY_READY_FOR_D1_PLANNING_ONLY")
    return {
        "decision": decision,
        "flags": sorted(set(flags)),
        "preferred_id_declared": chosen,
        "science_value_ranked": False,
        "scientific_novelty_verified": False,
        "q2_potential_verified": False,
        "download_authorized": False,
        "data_content_accessed": False,
        "note": ("Structural consistency only; references, actual alternate value, real dataset "
                 "conditions and eligibility need original-source review. No download, fit, "
                 "test access, topic-pivot or manuscript permission follows from this output.")
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--packet", required=True, type=Path,
                   help="Agent-written public-source opportunity comparison JSON")
    args = p.parse_args(argv)
    if args.packet.stat().st_size > MAX_PACKET_BYTES:
        p.error("comparison metadata exceeds 256 KiB")
    print(json.dumps(review_choice(json.loads(args.packet.read_text(encoding="utf-8"))),
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
