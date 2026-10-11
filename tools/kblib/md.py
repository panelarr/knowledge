"""Markdown helpers: frontmatter, links, code stripping."""
from __future__ import annotations

import re
from pathlib import Path

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)|!\[[^\]]*\]\(([^)\s]+)\)")
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (frontmatter block or None, body)."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    after = text.find("\n", end + 4)
    body = "" if after == -1 else text[after + 1:]
    return text[4:end], body


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Flat `key: value` frontmatter. Lists stay as raw strings; use parse_list()."""
    block, _ = split_frontmatter(text)
    if block is None:
        return None
    fm: dict[str, str] = {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            value = m.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
                value = value.replace('\\"', '"') if m.group(2).startswith('"') else value.replace("''", "'")
            fm[m.group(1)] = value
    return fm


def parse_list(value: str) -> list[str]:
    value = (value or "").strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [v.strip().strip("'\"") for v in value.split(",") if v.strip()]


def set_frontmatter(text: str, updates: dict[str, str]) -> str:
    """Replace or append keys in an existing frontmatter block."""
    block, body = split_frontmatter(text)
    if block is None:
        lines: list[str] = []
        body = text
    else:
        lines = block.splitlines()
    for key, value in updates.items():
        for i, line in enumerate(lines):
            if re.match(rf"^{re.escape(key)}:", line):
                lines[i] = f"{key}: {value}"
                break
        else:
            lines.append(f"{key}: {value}")
    return "---\n" + "\n".join(lines) + "\n---\n" + body


def strip_code(text: str) -> str:
    """Blank out fenced code blocks and inline code so links/IDs inside them are ignored."""
    out, fenced = [], False
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else re.sub(r"`[^`]*`", "", line))
    return "\n".join(out)


def strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def links_in(text: str) -> list[str]:
    """Relative link targets (no scheme, no pure anchors), anchor removed."""
    found = []
    for m in LINK_RE.finditer(strip_code(strip_comments(text))):
        target = m.group(1) or m.group(2)
        if not target or target.startswith(("#", "/", "mailto:")) or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue
        target = target.split("#", 1)[0]
        if target and not PLACEHOLDER_RE.search(target):
            found.append(target)
    return found


def all_md(root: Path, skip_dirs: set[str]) -> list[Path]:
    return sorted(
        p for p in root.rglob("*.md")
        if not any(part in skip_dirs for part in p.relative_to(root).parts[:-1])
    )
