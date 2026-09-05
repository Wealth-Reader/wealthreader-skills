#!/usr/bin/env python3
"""Offline structural check for the skills in this repository.

Verifies, for every ``skills/*/SKILL.md``:

- YAML frontmatter is present and closed.
- ``name`` matches the folder name and the Agent Skills naming rules.
- ``description`` is present and within the specification length limit.
- The SKILL.md body stays within the recommended 500-line budget.
- Relative Markdown links in SKILL.md and ``references/*.md`` resolve to files.

Runs with the Python 3 standard library only. Exit code 1 on any failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_BODY_LINES = 500


def parse_frontmatter(text: str) -> tuple[dict[str, str], str] | None:
    """Return top-level scalar frontmatter fields and the body, or None."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    raw = text[4:end]
    body = text[end + 4 :]
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        if not line or line.startswith((" ", "\t", "#")):
            continue
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip().strip("\"'")
    return fields, body


def check_links(md_file: Path, errors: list[str]) -> None:
    text = md_file.read_text(encoding="utf-8")
    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = (md_file.parent / target.split("#", 1)[0]).resolve()
        if not resolved.exists():
            errors.append(f"{md_file.relative_to(REPO_ROOT)}: broken link '{target}'")


def check_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    rel = skill_md.relative_to(REPO_ROOT)
    if not skill_md.is_file():
        return [f"{skill_dir.relative_to(REPO_ROOT)}: missing SKILL.md"]

    parsed = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    if parsed is None:
        return [f"{rel}: missing or unterminated YAML frontmatter"]
    fields, body = parsed

    name = fields.get("name", "")
    if not name:
        errors.append(f"{rel}: frontmatter 'name' is required")
    elif name != skill_dir.name:
        errors.append(f"{rel}: name '{name}' must match folder '{skill_dir.name}'")
    elif len(name) > MAX_NAME or not NAME_RE.match(name):
        errors.append(f"{rel}: name '{name}' violates naming rules")

    description = fields.get("description", "")
    if not description:
        errors.append(f"{rel}: frontmatter 'description' is required")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"{rel}: description exceeds {MAX_DESCRIPTION} characters")

    body_lines = len(body.strip().splitlines())
    if body_lines > MAX_BODY_LINES:
        errors.append(f"{rel}: body has {body_lines} lines, limit is {MAX_BODY_LINES}")

    for md_file in [skill_md, *sorted(skill_dir.glob("references/*.md"))]:
        check_links(md_file, errors)

    return errors


def main() -> int:
    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skill_dirs:
        print(f"No skills found under {SKILLS_DIR}")
        return 1

    failures = 0
    for skill_dir in skill_dirs:
        errors = check_skill(skill_dir)
        status = "FAIL" if errors else "OK"
        print(f"[{status}] {skill_dir.relative_to(REPO_ROOT)}")
        for error in errors:
            print(f"  - {error}")
        failures += len(errors)

    check_links(REPO_ROOT / "README.md", readme_errors := [])
    for error in readme_errors:
        print(f"  - {error}")
    failures += len(readme_errors)

    print("All checks passed." if failures == 0 else f"{failures} problem(s) found.")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
