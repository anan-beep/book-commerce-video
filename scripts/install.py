#!/usr/bin/env python3
"""Install the skill payload without overwriting an existing installation."""

import argparse
import os
from pathlib import Path
import shutil
import sys

PAYLOAD = ("SKILL.md", "LICENSE", "agents", "references", "evals")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    codex_root = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    parser.add_argument("--dest", type=Path, default=codex_root / "skills",
                        help="Parent directory for the installed skill")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    target = args.dest.expanduser().resolve() / "book-commerce-video"
    missing = [name for name in PAYLOAD if not (source / name).exists()]
    if missing:
        parser.error("Missing source payload: " + ", ".join(missing))
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        target.mkdir()
    except FileExistsError:
        print(f"Installation already exists; left untouched: {target}", file=sys.stderr)
        return 1
    try:
        for name in PAYLOAD:
            item = source / name
            if item.is_dir():
                shutil.copytree(item, target / name)
            else:
                shutil.copy2(item, target / name)
    except Exception:
        shutil.rmtree(target)
        raise
    print(f"Installed: {target}")
    print("Reopen your Codex session or refresh the skill list.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
