"""Aliases for sensitive terms: `.kb-aliases.env` (git-ignored, shared by hand).

    # ALIAS=real term            one per line; `|` separates spellings of the same term
    FB=foobar|Foo Bar Inc
    CLIENT_A=Globex Corporation

Docs, commits and anything public use only the alias (`FB`). The agent reads this file to know
what FB means. Checks fail when a real term shows up where it shouldn't, and every message
masks it as `[FB]` so the term is never echoed back into logs.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from .config import Config

DEFAULT_FILE = ".kb-aliases.env"


def path(cfg: Config) -> Path:
    return cfg.root / cfg.privacy.get("aliases_file", DEFAULT_FILE)


def load(cfg: Config) -> dict[str, list[str]]:
    p = path(cfg)
    if not p.exists():
        return {}
    out: dict[str, list[str]] = {}
    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key.startswith("export "):
            key = key[7:].strip()
        value = value.strip().strip("'\"")
        terms = [t.strip() for t in value.split("|") if len(t.strip()) >= 2]
        if key and terms:
            out[key] = terms
    return out


def _regex(term: str) -> re.Pattern:
    left = r"(?<![\w])" if term[0].isalnum() else ""
    right = r"(?![\w])" if term[-1].isalnum() else ""
    return re.compile(left + re.escape(term) + right, re.IGNORECASE)


def find(text: str, aliases: dict[str, list[str]]) -> list[tuple[str, int]]:
    """(alias, line number) for every real term found in `text`."""
    hits = []
    pats = [(a, _regex(t)) for a, terms in aliases.items() for t in terms]
    for n, line in enumerate(text.splitlines(), 1):
        for alias, rx in pats:
            if rx.search(line) and (alias, n) not in hits:
                hits.append((alias, n))
    return hits


def mask(text: str, aliases: dict[str, list[str]]) -> str:
    for alias, terms in aliases.items():
        for t in sorted(terms, key=len, reverse=True):
            text = _regex(t).sub(f"[{alias}]", text)
    return text


def is_tracked(cfg: Config) -> bool:
    p = path(cfg)
    if not (cfg.root / ".git").exists() or not p.exists():
        return False
    r = subprocess.run(["git", "-C", str(cfg.root), "ls-files", "--error-unmatch", p.name], capture_output=True)
    return r.returncode == 0


def write_initial(target: Path, template: Path, pairs: dict[str, str]) -> None:
    text = template.read_text(encoding="utf-8") if template.exists() else "# ALIAS=real term\n"
    if pairs:
        text = text.rstrip() + "\n\n" + "".join(f"{k}={v}\n" for k, v in pairs.items())
    target.write_text(text, encoding="utf-8")


def cmd_list(cfg: Config, show: bool) -> int:
    p = path(cfg)
    if not p.exists():
        print(f"aliases: no {p.name}. If this KB uses aliases (short names standing in for confidential terms), "
              f"ask the owner for the file and put it in the KB root. It is git-ignored.")
        return 0
    al = load(cfg)
    print(f"aliases: {len(al)} defined in {p.name}{' (TRACKED BY GIT, remove it: git rm --cached ' + p.name + ')' if is_tracked(cfg) else ''}")
    for k, terms in sorted(al.items()):
        print(f"  {k:<20} {' | '.join(terms) if show else f'({len(terms)} spelling(s); --show to reveal)'}")
    return 0
