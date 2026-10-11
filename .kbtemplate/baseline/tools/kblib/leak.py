"""`kb.py leak-check`: privacy mode. Make sure public repos never reference the private KB.

Scans tracked files AND all commit messages of each repo for KB identifiers, the keeper
session name, the KB's folder name and any extra patterns from kb.config.json.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from .config import Config


def ere(term: str) -> str:
    """Escape for POSIX extended regex (git grep -E), which differs from Python's re.escape."""
    return re.sub(r"([.\[\]{}()\\*+?^$|])", r"\\\1", term)


def patterns(cfg: Config, kb_refs: bool = True) -> str:
    from . import aliases as al
    terms = [ere(t) for ts in al.load(cfg).values() for t in ts]
    if not kb_refs:
        return "(" + "|".join(terms) + ")" if terms else "(?!x)x"
    pats = []
    if cfg.ids:
        pats.append(f"({'|'.join(map(re.escape, cfg.ids))})-[0-9]{{4}}")
    keeper = cfg.project.get("keeper_session", "")
    if keeper and "{{" not in keeper:
        pats.append(re.escape(keeper))
    pats.append(re.escape(f"{cfg.root.parent.name}/{cfg.root.name}"))
    pats.append("^KB: ")
    pats += cfg.privacy.get("extra_patterns", [])
    pats += terms
    return "(" + "|".join(pats) + ")"


def targets(cfg: Config, args: list[str]) -> list[Path]:
    if args:
        return [Path(a).expanduser().resolve() for a in args]
    scan = cfg.privacy.get("scan") or [r["path"] for r in cfg.repos if r.get("path") and r.get("visibility", "public") == "public"]
    if not cfg.privacy.get("enabled"):  # aliases only: scan every registered local repo
        scan = cfg.privacy.get("scan") or [r["path"] for r in cfg.repos if r.get("path")]
    return [(cfg.root / s).expanduser().resolve() for s in scan]


def run(cfg: Config, args: list[str]) -> int:
    from . import aliases as al
    amap = al.load(cfg)
    if not cfg.privacy.get("enabled") and not args and not amap:
        print("leak-check: privacy mode is off (kb.config.json privacy.enabled); nothing to do")
        return 0
    repos = targets(cfg, args)
    if not repos:
        print("leak-check: no public repos registered; nothing to scan")
        return 0
    pattern = patterns(cfg, kb_refs=bool(cfg.privacy.get("enabled")))
    found = 0
    for repo in repos:
        if not (repo / ".git").exists():
            print(f"? {repo}: not a git repo, skipped")
            continue
        files = subprocess.run(["git", "-C", str(repo), "-c", "color.ui=never", "grep", "-niIE", pattern],
                               capture_output=True, text=True).stdout.strip()
        if files:
            print(f"✗ {repo.name}: tracked files reference the private KB or a confidential term:")
            print("\n".join("    " + al.mask(l, amap) for l in files.splitlines()))
            found = 1
        log = subprocess.run(["git", "-C", str(repo), "log", "--all", "--format=%h %s%n%b"],
                             capture_output=True, text=True).stdout
        rx = re.compile(pattern, re.M | re.I)
        hits = [l for l in log.splitlines() if rx.search(l)]
        if hits:
            print(f"✗ {repo.name}: commit messages reference the private KB or a confidential term:")
            print("\n".join("    " + al.mask(l, amap) for l in hits))
            found = 1
    if not found:
        print(f"leak-check: OK ({len(repos)} repo(s) clean)")
    return found
