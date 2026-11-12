"""Optional local existence/path check for a declared PD-RW delivery.

Does not inspect scientific truth, file contents, SEALED provenance, authorization,
user-visible links or whether an Agent actually followed the workflow. Read-only.
Use on an existing output directory; no manifest or additional report is required.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def check_delivery(root: Path, primary: str, files: list[str] | None = None) -> dict:
    """Check paths without reading files or following symlinks outside root."""
    files = files or []
    root = Path(root).resolve()
    errors: list[str] = []
    checked: list[str] = []
    if not root.is_dir():
        return {
            "result": "FAIL", "errors": ["DELIVERY_ROOT_MISSING"],
            "checked_paths": [], "verification": "PATHS_ONLY_NOT_SCIENCE_OR_AUTH",
        }
    items = [("PRIMARY", primary)] + [("FILE", p) for p in files]
    for role, raw in items:
        if not isinstance(raw, str) or not raw.strip():
            errors.append(f"{role}_PATH_EMPTY")
            continue
        relative = Path(raw)
        # A declared path must be inside the explicit output directory.
        if relative.is_absolute():
            errors.append(f"{role}_ABSOLUTE_PATH_NOT_ALLOWED:{raw}")
            continue
        target = (root / relative).resolve()
        if not target.is_relative_to(root):
            errors.append(f"{role}_OUTSIDE_DELIVERY_ROOT:{raw}")
        elif not target.exists():
            errors.append(f"{role}_MISSING:{raw}")
        elif not target.is_file() and not target.is_dir():
            errors.append(f"{role}_NOT_FILE_OR_DIRECTORY:{raw}")
        else:
            checked.append(raw)
    return {
        "result": "PASS_PATHS_ONLY" if not errors else "FAIL",
        "errors": errors, "checked_paths": checked,
        "verification": "PATHS_ONLY_NOT_SCIENCE_OR_AUTH",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only declared delivery path check")
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--primary", required=True)
    parser.add_argument("--file", action="append", default=[], dest="files")
    args = parser.parse_args()
    result = check_delivery(args.root, args.primary, args.files)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["result"] == "PASS_PATHS_ONLY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
