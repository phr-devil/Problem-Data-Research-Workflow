"""Append-only evidence events and non-linear, recoverable project index.

No scientific decision, training, or authorization is performed here.
"""
from __future__ import annotations
import hashlib
import json
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from core.contracts import ContractError, validate_claim, validate_run, validate_state

STATE = "STATE.json"
EVENTS = "EVENTS.jsonl"

@contextmanager
def _writer_lock(root: Path):
    # Atomic creation works on Windows/Linux, with no third-party dependency.
    lock_path = root / ".evidence-write.lock"
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise ContractError("another writer or stale evidence lock; inspect project before retry") from exc
    try:
        yield
    finally:
        os.close(fd)
        lock_path.unlink()


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def _resolve(root: Path, path: str | Path) -> Path:
    base = root.resolve()
    candidate = (base / path).resolve()
    if not candidate.is_relative_to(base) or not candidate.is_file():
        raise ContractError(f"artifact path missing or outside root: {path}")
    return candidate

def _atomic_json(path: Path, data: dict) -> None:
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".state-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            json.dump(data, output, ensure_ascii=False, indent=2, sort_keys=True)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def _base_state(project_id: str) -> dict:
    if not project_id or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in project_id):
        raise ContractError("project_id must be a nonempty ASCII slug")
    return {"schema_version": "1.4", "project_id": project_id,
            "active_task_id": None, "latest_valid_run_id": None,
            "last_event_id": None, "evidence_refs": []}

def initialize(root: Path, project_id: str) -> dict:
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    if (root / STATE).exists() or (root / EVENTS).exists():
        raise ContractError("state/events already exist; no overwrite of project assets")
    state = _base_state(project_id)
    _atomic_json(root / STATE, state)
    (root / EVENTS).touch(exist_ok=False)
    return state

def _read_events(root: Path, *, check_hashes: bool = True) -> list[dict]:
    path = root / EVENTS
    if not path.exists():
        raise ContractError("missing EVENTS.jsonl")
    events = []
    prev = None
    ids = set()
    with path.open("r", encoding="utf-8") as source:
        for n, line in enumerate(source, 1):
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ContractError(f"bad event JSON on line {n}") from exc
            if not isinstance(event, dict) or event.get("prev_event_id") != prev:
                raise ContractError(f"event chain broken at line {n}")
            if not isinstance(event.get("event_id"), str) or event["event_id"] in ids:
                raise ContractError(f"duplicate/invalid event_id on line {n}")
            if event.get("kind") not in {"note", "run", "claim"}:
                raise ContractError(f"unexpected event kind on line {n}")
            ids.add(event["event_id"])
            prev = event["event_id"]
            if event["kind"] != "note" and check_hashes:
                actual = _sha(_resolve(root, event.get("artifact_path", "")))
                if actual != event.get("artifact_sha256"):
                    raise ContractError(f"artifact fingerprint mismatch at line {n}")
            events.append(event)
    return events

def _build_state(project_id: str, events: list[dict]) -> dict:
    state = _base_state(project_id)
    for e in events:
        if e.get("project_id") != project_id:
            raise ContractError("event project_id does not match STATE")
        state["last_event_id"] = e["event_id"]
        if e["kind"] != "note":
            ref = {"kind": e["kind"], "id": e["artifact_id"],
                   "path": e["artifact_path"], "sha256": e["artifact_sha256"]}
            state["evidence_refs"].append(ref)
            state["active_task_id"] = e["task_id"]
            if e["kind"] == "run" and e["status"] == "VALID" and e["split"] != "sealed":
                state["latest_valid_run_id"] = e["artifact_id"]
    return state

def status(root: Path) -> dict:
    root = Path(root)
    try:
        with (root / STATE).open(encoding="utf-8") as source:
            state = validate_state(json.load(source))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise ContractError("missing/corrupt STATE.json; inspect events before recovering") from exc
    events = _read_events(root)
    expected = _build_state(state["project_id"], events)
    if state != expected:
        raise ContractError("STATE vs EVENTS mismatch; inspect then run explicit recover")
    return {"status": "CONSISTENT", "project_id": state["project_id"],
            "last_event_id": state["last_event_id"],
            "evidence_count": len(state["evidence_refs"]),
            "active_task_id": state["active_task_id"],
            "latest_valid_run_id": state["latest_valid_run_id"]}

def _validate_linked(root: Path, kind: str, obj: dict, events: list[dict]) -> None:
    if kind == "run" and obj["status"] == "VALID":
        for ref in obj["artifact_refs"].values():
            _resolve(root, ref)
    if kind == "claim" and obj["status"] in {"SUPPORTED", "CONFIRMED"}:
        runs = {e["artifact_id"]: e for e in events if e["kind"] == "run"}
        for run_id in obj["evidence_run_ids"]:
            if run_id not in runs or runs[run_id]["status"] != "VALID" or runs[run_id]["task_id"] != obj["task_id"]:
                raise ContractError(f"claim references missing/invalid/mismatched Run: {run_id}")
        for ref in obj["artifact_refs"]:
            _resolve(root, ref)
        if obj["status"] == "CONFIRMED":
            for run_id in obj["confirmation_run_ids"]:
                event = runs.get(run_id)
                if not event or event["task_id"] != obj["task_id"] or event["split"] != "sealed" or event["status"] != "VALID":
                    raise ContractError(f"confirmation Run not valid/sealed: {run_id}")

def record_event(root: Path, kind: str, *, artifact: str | None = None,
                 note: str = "") -> dict:
    with _writer_lock(Path(root)):
        return _record_event_locked(Path(root), kind, artifact=artifact, note=note)

def _record_event_locked(root: Path, kind: str, *, artifact: str | None = None,
                         note: str = "") -> dict:
    if kind not in {"note", "run", "claim"}:
        raise ContractError("kind must be note/run/claim")
    current = status(root)
    with (root / STATE).open(encoding="utf-8") as source:
        state = json.load(source)
    events = _read_events(root, check_hashes=False)
    if kind == "note":
        if artifact:
            raise ContractError("note event cannot advance evidence")
        obj, path, digest = None, None, None
    else:
        if not artifact:
            raise ContractError("run/claim event requires a real JSON artifact")
        path_obj = _resolve(root, artifact)
        path = path_obj.relative_to(root.resolve()).as_posix()
        try:
            obj = json.loads(path_obj.read_text(encoding="utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise ContractError("invalid JSON artifact") from exc
        obj = validate_run(obj) if kind == "run" else validate_claim(obj)
        digest = _sha(path_obj)
        _validate_linked(root, kind, obj, events)
        if kind == "run":
            if any(e["kind"] == "run" and e["artifact_id"] == obj["run_id"] for e in events):
                raise ContractError("run_id already recorded; keep immutable run IDs")
        else:
            if any(e["kind"] == "claim" and e["artifact_id"] == obj["claim_id"] for e in events):
                raise ContractError("claim_id already recorded; version claims instead of overwriting")
    event = {"event_id": uuid4().hex, "prev_event_id": state["last_event_id"],
             "project_id": state["project_id"], "kind": kind,
             "recorded_at": datetime.now(timezone.utc).isoformat(), "note": note}
    if obj is not None:
        event.update({"artifact_id": obj["run_id" if kind == "run" else "claim_id"],
                      "artifact_path": path, "artifact_sha256": digest,
                      "task_id": obj["task_id"], "status": obj["status"]})
        if kind == "run":
            event["split"] = obj["split"]
    # Log-first: interruption between append and STATE save is detected by status().
    with (root / EVENTS).open("a", encoding="utf-8") as output:
        output.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        output.flush()
        os.fsync(output.fileno())
    new_state = _build_state(state["project_id"], events + [event])
    _atomic_json(root / STATE, new_state)
    return event

def recover(root: Path) -> dict:
    """Explicit reconciliation after inspecting real artifact/log history."""
    with _writer_lock(Path(root)):
        return _recover_locked(Path(root))

def _recover_locked(root: Path) -> dict:
    with (root / STATE).open(encoding="utf-8") as source:
        old = validate_state(json.load(source))
    events = _read_events(root)
    updated = _build_state(old["project_id"], events)
    _atomic_json(root / STATE, updated)
    return status(root)
