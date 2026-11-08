"""Batch DOI metadata check; requires explicit --allow-network.
Input JSON: {"expected_count": 2, "references": [{"ref_id":"R1","doi":"10...","title":"...","year":2026,"first_author":"..."}, ...]}
Only DOI is sent to Crossref/DataCite. Passage-level support is NEVER auto-certified.
"""
from __future__ import annotations
import argparse
import json
from collections import Counter
from pathlib import Path
from core.literature import verify_reference_metadata


def audit_batch(payload: dict, *, fetch=None) -> dict:
    refs = payload.get("references")
    if not isinstance(refs, list):
        raise ValueError("references must be a list")
    n = payload.get("expected_count")
    if type(n) is not int or n < 0:
        raise ValueError("expected_count must be the independently counted bibliography size")
    if len(refs) != n:
        return {"status": "REFERENCE_SET_INCOMPLETE", "expected_count": n,
                "extracted_count": len(refs), "references": []}
    checked = []
    seen = set()
    seen_ids = set()
    for i, ref in enumerate(refs, 1):
        if not isinstance(ref, dict):
            raise ValueError("each reference must be an object")
        result = (verify_reference_metadata(ref, fetch=fetch)
                  if fetch is not None else verify_reference_metadata(ref))
        result["ref_id"] = str(ref.get("ref_id") or f"R{i}")
        if result["ref_id"] in seen_ids:
            result["duplicate_ref_id"] = True
        seen_ids.add(result["ref_id"])
        if result.get("doi"):
            if result["doi"] in seen:
                result["duplicate_doi"] = True
            seen.add(result["doi"])
        checked.append(result)
    counts = Counter(x["status"] for x in checked)
    duplicate_dois = sum(bool(x.get("duplicate_doi")) for x in checked)
    duplicate_ids = sum(bool(x.get("duplicate_ref_id")) for x in checked)
    all_matched = (all(x["status"] == "METADATA_MATCH" for x in checked)
                   and not duplicate_dois and not duplicate_ids)
    return {"status": "DOI_METADATA_AUDITED_NOT_CLAIMS", "expected_count": n,
            "extracted_count": len(refs), "status_counts": dict(counts),
            "duplicate_doi_count": duplicate_dois,
            "duplicate_ref_id_count": duplicate_ids,
            "metadata_integrity": ("ALL_MATCHED_NOT_CLAIM_VERIFIED" if all_matched
                                   else "ISSUES_REQUIRE_MANUAL_REVIEW"),
            "source_claim_support": "NOT_CHECKED",
            "references": checked,
            "remaining_work": "Check all original publication records, corrections/retractions, and cited claims by source passages."}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", help="JSON list prepared from a checked bibliography")
    p.add_argument("--output", required=True)
    p.add_argument("--allow-network", action="store_true", help="Explicitly authorize public DOI-only API lookups")
    args = p.parse_args()
    if not args.allow_network:
        p.error("No public DOI lookup without --allow-network")
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = audit_batch(payload)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                 encoding="utf-8")


if __name__ == "__main__":
    main()
