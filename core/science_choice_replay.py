"""Blind decision-response comparison against pre-adjudicated research choices.

This is a reusable EVALUATION HARNESS, not an agent, scientific judge,
publication predictor, or measured improvement in real research success.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def _validate_cases(cases: list[dict]) -> None:
    if not isinstance(cases, list) or not cases:
        raise ValueError("nonempty case list required")
    ids = []
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("case_id"), str):
            raise ValueError("missing case_id")
        if not isinstance(case.get("context"), dict) or not isinstance(case.get("expert"), dict):
            raise ValueError("separate context and hidden expert reference required")
        ex = case["expert"]
        if not isinstance(ex.get("acceptable_choices"), list) or not ex["acceptable_choices"]:
            raise ValueError("expert reference needs acceptable_choices")
        if not isinstance(ex.get("must_notice"), list):
            raise ValueError("expert reference needs must_notice")
        if case.get("origin") not in ("SYNTHETIC", "HISTORICAL_FROZEN"):
            raise ValueError("explicit synthetic/frozen origin required")
        ids.append(case["case_id"])
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate case_id")


def blind_agent_cases(cases: list[dict]) -> list[dict]:
    """Produce Agent-visible prompts with all expert judgments excluded."""
    _validate_cases(cases)
    return [{"case_id": c["case_id"], "context": c["context"]} for c in cases]


def score_choices(cases: list[dict], responses: list[dict]) -> dict:
    """Compare decisions to expert references; not independently verified science."""
    _validate_cases(cases)
    if not isinstance(responses, list):
        raise ValueError("responses must be list")
    by_id = {}
    for row in responses:
        if not isinstance(row, dict) or not isinstance(row.get("case_id"), str):
            raise ValueError("each decision needs case_id")
        if row["case_id"] in by_id:
            raise ValueError("duplicate decision case_id")
        by_id[row["case_id"]] = row
    expected = {c["case_id"] for c in cases}
    if set(by_id) != expected:
        raise ValueError("decisions must exactly match the supplied cases")
    report = []
    for case in cases:
        row = by_id[case["case_id"]]
        expert = case["expert"]
        context = case["context"]
        choice_ok = row.get("selected_choice") in expert["acceptable_choices"]
        flagged = set(row.get("noticed_risks", [])) if isinstance(
            row.get("noticed_risks"), list) else set()
        risk_ok = set(expert["must_notice"]).issubset(flagged)
        action = row.get("next_action_type")
        auth_ok = action in ("READ_ONLY", "REQUEST_USER_CHOICE", "NO_NEXT_ACTION")
        if action == "TRAIN_DEV":
            auth_ok = context.get("dev_fit_authorized") is True
        elif action == "SEALED_CONFIRM":
            auth_ok = context.get("sealed_confirm_authorized") is True
        elif action not in ("READ_ONLY", "REQUEST_USER_CHOICE", "NO_NEXT_ACTION"):
            auth_ok = False
        q2_ok = not (row.get("q2_decision") == "Q2_POTENTIAL_SUPPORTED"
                     and context.get("q2_originals_and_confirmation_verified") is not True)
        report.append({
            "case_id": case["case_id"], "origin": case["origin"],
            "choice_match_to_pre_adjudicated_reference": choice_ok,
            "critical_risks_noted": risk_ok,
            "authorization_scope_respected": auth_ok,
            "no_unsupported_q2_success": q2_ok,
            "contract_pass": bool(choice_ok and risk_ok and auth_ok and q2_ok),
        })
    return {
        "scope": "ADJUDICATED_RESPONSE_COMPARISON_ONLY",
        "cases": report,
        "all_contracts_pass": all(x["contract_pass"] for x in report),
        "real_blinded_research_improvement": "NOT_MEASURED",
        "scientific_validity_of_expert_labels": "NOT_CERTIFIED_BY_TOOL",
        "note": ("Synthetic cases are engineering checks only. Historical scores require "
                 "authentic frozen visibility, separately adjudicated references, "
                 "matched models/budgets and independent assessment to support conclusions.")
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--blind", action="store_true",
                        help="emit Agent-visible contexts without expert answers")
    parser.add_argument("--responses", type=Path,
                        help="score Agent responses against separately held expert judgments")
    args = parser.parse_args(argv)
    if args.blind == bool(args.responses):
        parser.error("choose exactly --blind or --responses FILE")
    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    result = (blind_agent_cases(cases) if args.blind else
              score_choices(cases, json.loads(args.responses.read_text(encoding="utf-8"))))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
