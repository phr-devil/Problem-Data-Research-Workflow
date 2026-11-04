"""Read-only exploratory inventory of already-verified, matched DEV group metrics.

Input is a manually prepared, legally accessible summary, not an independent
metric verifier. Neither this script nor a 'candidate' flag proves a mechanism,
causality, novelty, Q2 potential, group independence or holdout eligibility.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

MAX_ROWS = 20000
MAX_CONDITIONS = 20
MAX_PACKET_BYTES = 5 * 1024 * 1024
ROLES = {"DEV", "PUBLIC_METADATA"}


def _required_text(data: dict, key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a nonempty string")
    return value.strip()


def _number(value: object, key: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be finite numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{key} must be finite numeric")
    return result


def inspect_existing_results(packet: dict) -> dict:
    """Describe a matched pair group comparison, never certify the science."""
    if not isinstance(packet, dict):
        raise ValueError("packet must be an object")
    if packet.get("role") not in ROLES:
        raise PermissionError("Only declared DEV or public metadata; sealed data prohibited")
    for field in ("task_id", "protocol_id", "metric", "group_unit",
                  "champion_run_ref", "baseline_run_ref", "selection_history_ref"):
        _required_text(packet, field)
    if type(packet.get("higher_is_better")) is not bool:
        raise ValueError("higher_is_better must be explicitly boolean")
    if packet.get("matched_information_and_evaluator") is not True:
        raise ValueError("Only declared matched-information/evaluator pairs can be compared")
    if packet["champion_run_ref"] == packet["baseline_run_ref"]:
        raise ValueError("champion and baseline cannot be the same Run")
    rows = packet.get("observations")
    if not isinstance(rows, list) or not 1 <= len(rows) <= MAX_ROWS:
        raise ValueError("observations must be 1..20000 matched DEV group records")
    grouped = defaultdict(list)
    groups = set()
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each observation must be an object")
        group = _required_text(row, "group")
        condition = _required_text(row, "condition")
        key = (condition, group)
        if key in seen:
            raise ValueError("duplicate group-condition: no pseudoreplicated rows")
        seen.add(key)
        base = _number(row.get("baseline"), "baseline")
        champ = _number(row.get("champion"), "champion")
        gain = (champ - base) * (1.0 if packet["higher_is_better"] else -1.0)
        grouped[condition].append(gain)
        groups.add(group)
    if len(grouped) > MAX_CONDITIONS:
        raise ValueError("scope at most 20 prespecified, meaningful conditions")
    cond = []
    for name in sorted(grouped):
        values = grouped[name]
        cond.append({
            "condition": name,
            "declared_independent_groups": len(values),
            "unweighted_mean_paired_gain": sum(values) / len(values),
            "min_paired_gain": min(values),
            "max_paired_gain": max(values),
            "groups_benefited": sum(x > 0 for x in values),
            "groups_harmed": sum(x < 0 for x in values),
            "groups_tied": sum(x == 0 for x in values),
        })
    clues = []
    means = [x["unweighted_mean_paired_gain"] for x in cond]
    if any(x > 0 for x in means) and any(x < 0 for x in means):
        clues.append("OPPOSITE_SIGN_ACROSS_CONDITIONS_EXPLORATORY")
    if any(x["groups_benefited"] > 0 and x["groups_harmed"] > 0 for x in cond):
        clues.append("WITHIN_CONDITION_GROUP_HETEROGENEITY_EXPLORATORY")
    if any(x["declared_independent_groups"] < 3 for x in cond):
        clues.append("THIN_DECLARED_GROUP_SUPPORT")
    if not clues:
        clues.append("NO_PREDEFINED_HETEROGENEITY_CLUE_DETECTED")
    costs = packet.get("measured_costs", [])
    if not isinstance(costs, list) or len(costs) > 8:
        raise ValueError("measured_costs must be 0..8 records")
    cost_records = []
    for c in costs:
        if not isinstance(c, dict):
            raise ValueError("cost must be an object")
        name, unit = _required_text(c, "name"), _required_text(c, "unit")
        b, m = _number(c.get("baseline"), "cost baseline"), _number(
            c.get("champion"), "cost champion")
        if b < 0 or m < 0:
            raise ValueError("resource costs must not be negative")
        cost_records.append({"name": name, "unit": unit, "baseline": b,
                             "champion": m, "difference": m - b,
                             "observed_lower_cost": m < b})
    if any(c["observed_lower_cost"] for c in cost_records):
        clues.append("MEASURED_RESOURCE_DIFFERENCE_EXPLORATORY")
    core = {k: v for k, v in packet.items() if k != "previous_packet_sha256"}
    digest = hashlib.sha256(json.dumps(core, sort_keys=True, ensure_ascii=False,
                                      separators=(",", ":"), allow_nan=False).encode(
                                          "utf-8")).hexdigest()
    previous = packet.get("previous_packet_sha256")
    if previous is not None and (not isinstance(previous, str) or
                                 len(previous) != 64 or
                                 any(c not in "0123456789abcdef" for c in previous.lower())):
        raise ValueError("previous_packet_sha256 must be a SHA256 hex string")
    return {
        "status": "UNCHANGED_INPUT_REUSE" if previous == digest else "EXPLORATORY_ONLY",
        "input_sha256": digest,
        "task_id": packet["task_id"],
        "protocol_id": packet["protocol_id"],
        "source_run_refs_declared": [packet["baseline_run_ref"], packet["champion_run_ref"]],
        "group_unit_declared": packet["group_unit"],
        "distinct_declared_groups_total": len(groups),
        "condition_summaries": cond,
        "cost_observations": cost_records,
        "candidate_clues": clues,
        "science_confirmed": False,
        "q2_potential_verified": False,
        "causal_mechanism_verified": False,
        "independent_groups_verified": False,
        "source_metrics_independently_verified": False,
        "limitations": (
            "Input roles, matched settings, predictions, coverage, independent group IDs, "
            "original baselines and selection history are caller declarations only. "
            "Unweighted group means are not pooled sample metrics or statistical tests; "
            "cross-condition differences may be confounded. Post-hoc exploration cannot "
            "confirm a law, causal mechanism or Q2+ contribution. Do not use sealed data."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--packet", type=Path, required=True,
                   help="small legally prepared DEV/public paired-group summary JSON")
    args = p.parse_args(argv)
    if args.packet.stat().st_size > MAX_PACKET_BYTES:
        p.error("packet exceeds 5 MiB summary limit")
    payload = json.loads(args.packet.read_text(encoding="utf-8"))
    print(json.dumps(inspect_existing_results(payload), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
