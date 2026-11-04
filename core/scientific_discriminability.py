"""Descriptive crossed-factor screen for already-permitted DEV/public metadata.

No fitting, downloads, data access authorization, causal inference, or Q2 verdict.
The caller must independently verify source provenance and effective group unit.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import json
from pathlib import Path

MAX_ROWS = 50_000
MAX_LEVELS = 32
ROLES = {"DEV", "PUBLIC_METADATA"}


def screen_discriminability(rows: list[dict], *, factor_a: str,
                           factor_b: str, group_key: str,
                           role: str) -> dict:
    """Return descriptive factor crossing; never claim causal identifiability."""
    if role not in ROLES:
        raise PermissionError("Only declared DEV or PUBLIC_METADATA; no sealed confirmation")
    fields = (factor_a, factor_b, group_key)
    if len(set(fields)) != 3 or not all(isinstance(k, str) and k.strip() for k in fields):
        raise ValueError("Provide three distinct nonempty column names")
    if not isinstance(rows, list) or not 1 <= len(rows) <= MAX_ROWS:
        raise ValueError("Expected 1..50000 pre-extracted metadata rows")
    cells: dict[tuple[str, str], set[str]] = defaultdict(set)
    group_a: dict[str, set[str]] = defaultdict(set)
    group_b: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Each metadata row must be an object")
        values = [row.get(k) for k in fields]
        if any(isinstance(v, bool) or not isinstance(v, (str, int))
               or not str(v).strip() for v in values):
            raise ValueError("All metadata factors and group IDs must be nonempty strings/integers")
        a, b, g = (str(v) for v in values)
        cells[(a, b)].add(g)
        group_a[g].add(a)
        group_b[g].add(b)
    levels_a = sorted({a for a, _ in cells})
    levels_b = sorted({b for _, b in cells})
    if max(len(levels_a), len(levels_b)) > MAX_LEVELS:
        raise ValueError("Too many factor levels: scope an interpretable scientific contrast")
    full = len(levels_a) * len(levels_b)
    observed = len(cells)
    if min(len(levels_a), len(levels_b)) < 2:
        status = "NO_TWO_FACTOR_CONTRAST"
    elif observed < full and (all(len({b for a, b in cells if a == x}) == 1 for x in levels_a)
                             or all(len({a for a, b in cells if b == x}) == 1 for x in levels_b)):
        status = "STRUCTURALLY_NESTED_OR_CONFOUNDED"
    elif observed < full:
        status = "PARTIALLY_CROSSED"
    elif min(len(v) for v in cells.values()) < 2:
        status = "CROSSED_THIN_DECLARED_GROUPS"
    else:
        status = "DESCRIPTIVELY_CROSSED"
    a_fixed = len(levels_a) > 1 and all(len(v) == 1 for v in group_a.values())
    b_fixed = len(levels_b) > 1 and all(len(v) == 1 for v in group_b.values())
    return {
        "status": status,
        "role_declaration": role,
        "columns": {"factor_a": factor_a, "factor_b": factor_b, "group": group_key},
        "levels": {"factor_a": levels_a, "factor_b": levels_b},
        "cells_observed": observed,
        "cells_possible": full,
        "distinct_declared_groups_total": len(group_a),
        "counts": [{"a": a, "b": b, "groups": len(cells.get((a, b), set()))}
                   for a in levels_a for b in levels_b],
        "each_declared_group_fixed_within_factor": {
            "factor_a": a_fixed, "factor_b": b_fixed
        },
        "science_verified": False,
        "causal_identification_verified": False,
        "independence_verified": False,
        "note": ("Crossing, group IDs and declared role are descriptive, not authenticated. "
                 "No causal inference, label validity, sufficient power, clean selection history "
                 "or sealed holdout eligibility is established.")
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, required=True,
                        help="JSON array of already-permitted factor/group metadata; not predictions")
    parser.add_argument("--factor-a", required=True)
    parser.add_argument("--factor-b", required=True)
    parser.add_argument("--group", required=True)
    parser.add_argument("--role", choices=sorted(ROLES), required=True)
    args = parser.parse_args(argv)
    rows = json.loads(args.metadata.read_text(encoding="utf-8"))
    print(json.dumps(screen_discriminability(
        rows, factor_a=args.factor_a, factor_b=args.factor_b,
        group_key=args.group, role=args.role), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
