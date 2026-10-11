"""`kb.py commit-msg`: enforce the knowledge commit convention (meta/commit-convention.md)."""
from __future__ import annotations

import re
from pathlib import Path

from .config import Config

PASSTHROUGH = re.compile(r'^(Merge |Revert "|fixup! |squash! |amend! )')
# The template repo itself is software: contributors use plain Conventional Commits there.
TEMPLATE_TYPES = ["feat", "fix", "docs", "refactor", "test", "chore", "ci", "build", "perf", "style"]


def validate(cfg: Config, message: str, title_only: bool = False) -> list[str]:
    lines = [l for l in message.splitlines() if not l.startswith("#")]
    header = next((l for l in lines if l.strip()), "")
    if not header or PASSTHROUGH.match(header):
        return [] if header else ["empty commit message"]
    commit = cfg.commit
    types = list(commit.get("types", {}))
    if not cfg.initialized:
        types += [t for t in TEMPLATE_TYPES if t not in types]
    problems = []
    pattern = rf"^({'|'.join(map(re.escape, types))})(\([a-z0-9][a-z0-9/._-]*\))?(!)?: \S.*$"
    m = re.match(pattern, header)
    if not m:
        problems.append(
            f"header does not follow the commit convention:\n    {header}\n"
            f"  expected: <type>[(scope)][!]: <description>\n  types: {', '.join(types)}"
        )
    elif header.rstrip().endswith("."):
        problems.append("header must not end with a period")
    footer = commit.get("accepted_change_footer", "ACCEPTED-CHANGE")
    if m and m.group(3) and not title_only:
        if not any(l.startswith(f"{footer}:") for l in lines):
            problems.append(f"'!' (change to accepted knowledge) requires a '{footer}: …' footer")
    limit = int(commit.get("max_header", 72))
    if len(header) > limit:
        problems.append(f"header is {len(header)} chars; keep it ≤ {limit}")
    return problems


def run(cfg: Config, file: str | None, title: str | None) -> int:
    if title is not None:
        problems = validate(cfg, title, title_only=True)
    elif file:
        problems = validate(cfg, Path(file).read_text(encoding="utf-8"))
    else:
        print("commit-msg: pass a message file or --title")
        return 2
    for p in problems:
        print(f"✗ {p}")
    if problems:
        print("  see meta/commit-convention.md")
    return 1 if problems else 0
