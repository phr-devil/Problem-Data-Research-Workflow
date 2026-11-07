"""Off-repository private evaluation pack: format checks and redacted task export.

No model invocation, sandbox enforcement, signature checking or tool execution.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def external(path: Path, *, require_file: bool = False) -> Path:
    resolved, repo = path.resolve(), ROOT.resolve()
    if path.is_symlink() or resolved == repo or repo in resolved.parents:
        raise ValueError("private pack/export must remain outside the public repository")
    if require_file and not path.is_file():
        raise ValueError("private pack file missing")
    return resolved

def validate(pack: object) -> list[dict]:
    if not isinstance(pack, dict) or pack.get("format") != "pdrw-private-pack-v1":
        raise ValueError("invalid private pack format")
    if pack.get("visibility") != "EXTERNAL_PRIVATE" or not isinstance(pack.get("pack_id"), str) or not pack["pack_id"].strip():
        raise ValueError("private pack visibility/id required")
    cases = pack.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("nonempty case list required")
    ids = set()
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("case_id"), str) or not case["case_id"].strip():
            raise ValueError("case ID required")
        if case["case_id"] in ids:
            raise ValueError("duplicate case ID")
        ids.add(case["case_id"])
        task, reference = case.get("agent_task"), case.get("reference")
        if not isinstance(task, dict) or not isinstance(reference, dict):
            raise ValueError("separate agent_task and private reference required")
        if not isinstance(task.get("prompt"), str) or not task["prompt"].strip():
            raise ValueError("task prompt required")
        if not isinstance(task.get("allowed_effects"), list) or not all(isinstance(z,str) and z.strip() for z in task["allowed_effects"]):
            raise ValueError("allowed_effects list required")
        if not isinstance(task.get("budget_id"), str) or not task["budget_id"].strip():
            raise ValueError("budget_id required")
        if not isinstance(reference.get("rubric_version"), str) or not reference["rubric_version"].strip():
            raise ValueError("rubric_version required")
        criteria=reference.get("review_criteria")
        if not isinstance(criteria,list) or not criteria or not all(isinstance(z,str) and z.strip() for z in criteria):
            raise ValueError("private review criteria required")
    return cases

def public_tasks(pack: dict) -> dict:
    cases=validate(pack)
    data={"format":"pdrw-private-agent-tasks-v1","pack_id":pack["pack_id"],
          "cases":[{"case_id":c["case_id"],"agent_task":c["agent_task"]} for c in cases],
          "scope":"NOT_REAL_AUTHORIZATION_OR_VERIFIED_BLINDNESS"}
    data["task_sha256"]=hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    return data

def main(argv=None) -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command",choices=("validate","export"))
    ap.add_argument("--pack",type=Path,required=True)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args(argv)
    external(args.pack,require_file=True)
    pack=json.loads(args.pack.read_text(encoding="utf-8"))
    cases=validate(pack)
    if args.command=="validate":
        response={"status":"FORMAT_VALID_NOT_AUTHENTICATED","case_count":len(cases),
                  "blindness":"NOT_CERTIFIED"}
    else:
        if args.output is None:
            ap.error("export requires --output")
        output=external(args.output)
        if output.exists():
            raise ValueError("refusing to overwrite private evaluation export")
        output.parent.mkdir(parents=True,exist_ok=True)
        public=public_tasks(pack)
        output.write_text(json.dumps(public,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        response={"status":"TASKS_EXPORTED_NOT_SANDBOXED",
                  "output":str(output),"case_count":len(cases)}
    print(json.dumps(response,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
