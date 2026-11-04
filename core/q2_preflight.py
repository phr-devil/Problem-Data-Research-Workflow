"""Read-only structural preflight for a proposed Q2+ evidence packet.

Never certifies scientific novelty, a JCR quartile, submission chances, or
publication success. Human examination of original research and sources is
mandatory after a structurally complete packet.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

CLAIM_KEYS = (
    "claim", "source_run", "nearest_original_paper_ref",
    "unanswered_difference", "fair_comparator_ref",
    "effect_and_uncertainty_ref", "confirmation_scope_ref",
    "selection_history_ref", "limitations_ref",
)
VENUE_KEYS = (
    "journal", "jcr_edition", "subject_category", "quartile",
    "indexing", "quartile_source", "source_checked_on",
    "article_type", "scope_fit_rationale",
)


def preflight(packet: Any) -> dict:
    """Check evidence pointers and JCR metadata fields; NOT factual truth."""
    if not isinstance(packet, dict):
        return {"status": "INCOMPLETE", "missing": ["PACKET_OBJECT"],
                "human_science_review": "REQUIRED"}
    missing = [key for key in CLAIM_KEYS
               if not isinstance(packet.get(key), str) or not packet[key].strip()]
    venues = packet.get("venues")
    venue_candidates = []
    if not isinstance(venues, list) or not venues:
        missing.append("venues[Q1_or_Q2]")
    else:
        for index, venue in enumerate(venues):
            if not isinstance(venue, dict):
                missing.append(f"venues[{index}]")
                continue
            absent = [key for key in VENUE_KEYS if not isinstance(venue.get(key), str)
                      or not venue[key].strip()]
            analogs = venue.get("recent_comparable_articles")
            if not isinstance(analogs, list) or not analogs or not all(
                isinstance(p, str) and p.strip() for p in analogs
            ):
                absent.append("recent_comparable_articles")
            if absent:
                missing.extend(f"venues[{index}].{key}" for key in absent)
            elif venue["quartile"].upper() in {"Q1", "Q2"}:
                venue_candidates.append({"journal": venue["journal"],
                                         "quartile": venue["quartile"].upper(),
                                         "category": venue["subject_category"],
                                         "edition": venue["jcr_edition"]})
        if not venue_candidates:
            missing.append("VERIFIABLE_JCR_Q1_OR_Q2_VENUE_CANDIDATE")
    return {
        "status": "READY_FOR_HUMAN_SCIENTIFIC_AND_JCR_REVIEW" if not missing else "INCOMPLETE",
        "missing": sorted(set(missing)),
        "potential_target_candidates": venue_candidates,
        "q2_potential_supported": False,
        "human_science_review": "REQUIRED",
        "note": ("Completeness only; source authenticity, relevant JCR category, "
                 "novelty, effect validity, article comparability and user approval "
                 "cannot be proved from user-supplied strings.")
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_json", type=Path, help="Read-only evidence packet")
    args = parser.parse_args()
    payload = json.loads(args.evidence_json.read_text(encoding="utf-8"))
    print(json.dumps(preflight(payload), ensure_ascii=False, indent=2))
