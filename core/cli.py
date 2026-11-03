"""Small offline CLI; nothing here downloads, trains, or approves."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from core.comparison import compare_runs
from core.contracts import ContractError
from core.state import initialize, record_event, recover, status

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PD-RW evidence index and comparison")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--root", type=Path, required=True)
    init.add_argument("--project-id", required=True)
    for action in ("record", "status", "recover"):
        p = sub.add_parser(action)
        p.add_argument("--root", type=Path, required=True)
        if action == "record":
            p.add_argument("--kind", choices=["note", "run", "claim"], required=True)
            p.add_argument("--artifact")
            p.add_argument("--note", default="")
    compare = sub.add_parser("compare")
    compare.add_argument("--champion", type=Path, required=True)
    compare.add_argument("--challenger", type=Path, required=True)
    compare.add_argument("--metric", required=True)
    compare.add_argument("--lower-is-better", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = initialize(args.root, args.project_id)
        elif args.command == "record":
            result = record_event(args.root, args.kind, artifact=args.artifact, note=args.note)
        elif args.command == "status":
            result = status(args.root)
        elif args.command == "recover":
            result = recover(args.root)
        else:
            a = json.loads(args.champion.read_text(encoding="utf-8"))
            b = json.loads(args.challenger.read_text(encoding="utf-8"))
            result = compare_runs(a, b, args.metric, lower_is_better=args.lower_is_better)
    except (ContractError, OSError, ValueError) as exc:
        parser.exit(2, f"Evidence check failed: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
