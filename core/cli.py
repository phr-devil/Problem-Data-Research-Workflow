"""Small evidence CLI. Only explicit literature-search performs network requests."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from core.comparison import compare_runs
from core.contracts import ContractError
from core.state import initialize, record_event, recover, status
from core.task_runtime import qualify_task, audit_run_reproducibility
from core.probes import review_probe
from core.literature import literature_search

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PD-RW evidence index and comparison")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--root", type=Path, required=True)
    init.add_argument("--project-id", required=True)
    for action in ("record", "status", "recover"):
        p = sub.add_parser(action)
        p.add_argument("--root", type=Path, required=True)
        if action == "status":
            p.add_argument("--deep", action="store_true", help="rehash original linked artifacts")
        if action == "record":
            p.add_argument("--kind", choices=["note", "run", "claim"], required=True)
            p.add_argument("--artifact")
            p.add_argument("--note", default="")
    compare = sub.add_parser("compare")
    compare.add_argument("--champion", type=Path, required=True)
    compare.add_argument("--challenger", type=Path, required=True)
    compare.add_argument("--metric", required=True)
    compare.add_argument("--lower-is-better", action="store_true")
    task = sub.add_parser("task-check", help="Read-only TaskSpec and split qualification")
    task.add_argument("--root", type=Path, required=True)
    task.add_argument("--spec", required=True, help="TaskSpec JSON path relative to root")
    runcheck = sub.add_parser("run-check", help="Read-only Run execution/reproducibility preflight")
    runcheck.add_argument("--root", type=Path, required=True)
    runcheck.add_argument("--run", required=True, help="Run JSON path relative to root")
    probe = sub.add_parser("probe-check", help="Review a proposed discriminating experiment")
    probe.add_argument("--file", type=Path, required=True)
    lit = sub.add_parser("literature-search", help="Explicit live metadata lookup (network)")
    lit.add_argument("--query", required=True)
    lit.add_argument("--limit", type=int, default=5)
    lit.add_argument("--output", type=Path, required=True, help="New JSON output file; never overwritten")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = initialize(args.root, args.project_id)
        elif args.command == "record":
            result = record_event(args.root, args.kind, artifact=args.artifact, note=args.note)
        elif args.command == "status":
            result = status(args.root, deep=args.deep)
        elif args.command == "recover":
            result = recover(args.root)
        elif args.command == "task-check":
            result = qualify_task(args.root, args.spec)
        elif args.command == "run-check":
            result = audit_run_reproducibility(args.root, args.run)
        elif args.command == "probe-check":
            result = review_probe(json.loads(args.file.read_text(encoding="utf-8")))
        elif args.command == "literature-search":
            if args.output.exists():
                raise ContractError("literature evidence output already exists; do not overwrite")
            result = literature_search(args.query, args.limit)
            with args.output.open("x", encoding="utf-8") as target:
                json.dump(result, target, ensure_ascii=False, indent=2)
                target.write("\n")
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
