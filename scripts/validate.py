#!/usr/bin/env python3
"""Validate the distributable package; this does not generate or test videos."""

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

import yaml


def main():
    root = Path(__file__).resolve().parents[1]
    errors = []
    required = ("SKILL.md", "LICENSE", "README.md", "agents/openai.yaml",
                "references/research-and-script.md", "references/visual-and-assets.md",
                "references/chatcut-production.md", "references/qa-checklist.md",
                "evals/evals.json", "scripts/install.py")
    for name in required:
        if not (root / name).is_file():
            errors.append(f"Missing: {name}")
    try:
        text = (root / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
        if not match:
            raise ValueError("Invalid SKILL frontmatter")
        metadata = yaml.safe_load(match.group(1))
        if not isinstance(metadata, dict):
            raise ValueError("Frontmatter must be a mapping")
        if metadata.get("name") != "book-commerce-video":
            errors.append("Unexpected skill name")
        if not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
            errors.append("Missing skill description")
        if metadata.get("license") != "MIT":
            errors.append("Skill license must match LICENSE")
        ui = yaml.safe_load((root / "agents/openai.yaml").read_text(encoding="utf-8"))
        if "$book-commerce-video" not in ui["interface"]["default_prompt"]:
            errors.append("UI default_prompt must name the skill")
        data = json.loads((root / "evals/evals.json").read_text(encoding="utf-8"))
        if data["skill"] != metadata["name"]:
            errors.append("Eval skill name mismatch")
        seen = set()
        if not data["cases"]:
            errors.append("No behavioral eval cases")
        for case in data["cases"]:
            if case["id"] in seen:
                errors.append(f"Duplicate eval id: {case['id']}")
            seen.add(case["id"])
            for key in ("id", "type", "input", "expected"):
                if not isinstance(case.get(key), str) or not case[key].strip():
                    errors.append(f"Invalid eval field: {key}")
    except (ValueError, KeyError, TypeError, OSError, yaml.YAMLError) as exc:
        errors.append(f"Metadata: {exc}")
    markdown = [root / "README.md", root / "CONTRIBUTING.md", root / "SKILL.md"]
    for folder in ("references", "examples"):
        markdown.extend((root / folder).glob("*.md"))
    for file in markdown:
        if not file.is_file():
            errors.append(f"Missing Markdown: {file.relative_to(root)}")
            continue
        text = file.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)\s]+)\)", text):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            resolved = (file.parent / unquote(target.split("#", 1)[0])).resolve()
            if root not in resolved.parents and resolved != root:
                errors.append(f"Link escapes package: {file.name} -> {target}")
            elif not resolved.exists():
                errors.append(f"Broken link: {file.name} -> {target}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Package structure, metadata and local links passed.")
    print("Behavioral evals and video production have not been run by this check.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
