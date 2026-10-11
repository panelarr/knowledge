"""`kb.py check`: keep the knowledge base healthy.

Checks:
  1. Knowledge docs have frontmatter with the required keys, a valid status and an ISO `updated`.
  2. `related:` paths in frontmatter exist.
  3. Relative Markdown links resolve (code blocks and HTML comments are ignored).
  4. Every doc is linked from its nearest README.md; every sub-folder README from its parent README.
  5. The status shown in an index row matches the doc's frontmatter status.
  6. Every ID reference (ADR-, Q-, IN-, FEAT-, GOAL-, ... from kb.config.json) exists.
  7. No duplicate ID numbers (two branches racing for the same ADR number).
  8. A superseded doc names its replacement.
  9. No `{{PLACEHOLDER}}` left once the KB is initialized.
 10. Outbox drafts have valid frontmatter.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import md
from .config import Config

ROOT_FILES = {"README.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md", "CONTRIBUTING.md", "SETUP.md", "NOTICE.md", "CHANGELOG.md"}
DEFAULT_REF_SKIP = ("inputs/", "meta/templates/", "ops/digests/", "agents/inbox/")
OUTBOX_ACTIONS = {"comment", "review", "label", "assign", "open_issue", "close", "merge"}
OUTBOX_STATES = {"draft", "approved", "posted", "discarded"}


class Checker:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.root = cfg.root
        self.errors: list[str] = []
        self.warnings: list[str] = []

    # -- helpers -----------------------------------------------------------
    def rel(self, p: Path) -> str:
        return p.relative_to(self.root).as_posix()

    def is_knowledge_doc(self, p: Path) -> bool:
        r = self.rel(p)
        if "/" not in r or p.name == "README.md":
            return False
        return not r.startswith(self.cfg.non_knowledge)

    def index_for(self, p: Path) -> Path | None:
        """The README that must index `p`: nearest README above it (own folder first)."""
        d = p.parent.parent if p.name == "README.md" else p.parent
        while True:
            cand = d / "README.md"
            if cand.exists() and cand.resolve() != p.resolve():
                return cand.resolve()
            if d.resolve() == self.root:
                return None
            d = d.parent

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    # -- run ---------------------------------------------------------------
    def run(self) -> int:
        cfg = self.cfg
        files = md.all_md(self.root, cfg.skip_dirs)
        texts = {p: p.read_text(encoding="utf-8") for p in files}
        statuses: dict[Path, str] = {}
        status_set = set(cfg.statuses)

        # 1 + 2: frontmatter
        for p in files:
            if not self.is_knowledge_doc(p):
                continue
            fm = md.parse_frontmatter(texts[p])
            r = self.rel(p)
            if fm is None:
                self.err(f"{r}: missing frontmatter")
                continue
            for key in cfg.required:
                if not fm.get(key):
                    self.err(f"{r}: frontmatter missing '{key}'")
            st = fm.get("status", "")
            if st and st not in status_set:
                self.err(f"{r}: invalid status '{st}' (allowed: {', '.join(cfg.statuses)})")
            statuses[p.resolve()] = st
            upd = fm.get("updated", "")
            if upd and not re.match(r"^\d{4}-\d{2}-\d{2}$", upd) and not (not cfg.initialized and md.PLACEHOLDER_RE.search(upd)):
                self.err(f"{r}: 'updated' must be YYYY-MM-DD")
            for target in md.parse_list(fm.get("related", "")):
                if md.PLACEHOLDER_RE.search(target):
                    continue
                if not (self.root / target).exists():
                    self.err(f"{r}: related path not found: {target}")

        # 3: links
        linked_from: dict[Path, set[Path]] = {}
        for p in files:
            for target in md.links_in(texts[p]):
                dest = (p.parent / target).resolve()
                if not dest.exists():
                    self.err(f"{self.rel(p)}: broken link -> {target}")
                    continue
                linked_from.setdefault(dest, set()).add(p.resolve())

        # 4 + 5: index completeness and status consistency
        for p in files:
            r = self.rel(p)
            if "/" not in r or r.startswith(cfg.unindexed):
                continue
            idx = self.index_for(p)
            if idx is None:
                continue
            if idx not in linked_from.get(p.resolve(), set()):
                self.err(f"{r}: not indexed in {self.rel(idx)}")
                continue
            st = statuses.get(p.resolve())
            if not st:
                continue
            for line in texts.get(idx, idx.read_text(encoding="utf-8")).splitlines():
                if not line.startswith("|"):
                    continue
                if not any((idx.parent / t).resolve() == p.resolve() for t in md.links_in(line)):
                    continue
                cells = {c.strip().strip("`*_ ") for c in line.strip().strip("|").split("|")}
                shown = cells & status_set
                if shown and st not in shown:
                    self.err(f"{r}: status '{st}' but index shows {sorted(shown)}")

        # 6 + 7: IDs
        known: dict[str, set[str]] = {}
        for prefix, spec in cfg.ids.items():
            nums: dict[str, list[str]] = {}
            d = self.root / spec.get("dir", "")
            if d.is_dir():
                for f in sorted(d.glob(f"{prefix}-*.md")):
                    m = re.match(rf"{re.escape(prefix)}-(\d{{4}})\b", f.name)
                    if m:
                        nums.setdefault(m.group(1), []).append(self.rel(f))
            if spec.get("kind") == "file":
                for n, paths in nums.items():
                    if len(paths) > 1:
                        self.err(f"duplicate {prefix}-{n}: {', '.join(paths)}")
            ids = set(nums)
            if spec.get("kind") == "register":
                reg = self.root / spec.get("index", "")
                if reg.exists():
                    rows = re.findall(rf"^\|\s*\[?{re.escape(prefix)}-(\d{{4}})\b", reg.read_text(encoding="utf-8"), re.M)
                    seen: set[str] = set()
                    for n in rows:
                        if n in seen:
                            self.err(f"{self.rel(reg)}: duplicate row {prefix}-{n}")
                        seen.add(n)
                    ids |= seen
            known[prefix] = ids

        ref_skip = tuple(cfg.get("ref_skip", DEFAULT_REF_SKIP))
        for p in files:
            r = self.rel(p)
            if r.startswith(ref_skip):
                continue
            body = md.strip_code(md.strip_comments(texts[p]))
            for prefix, ids in known.items():
                for n in sorted(set(re.findall(rf"\b{re.escape(prefix)}-(\d{{4}})\b", body)) - ids):
                    if n != "0000":
                        self.err(f"{r}: references missing {prefix}-{n}")

        # 8: superseded docs name a replacement
        prefixes = "|".join(re.escape(k) for k in cfg.ids)
        for p, st in statuses.items():
            if st != "superseded":
                continue
            own = re.match(rf"({prefixes})-(\d{{4}})", p.name) if prefixes else None
            body = md.strip_code(p.read_text(encoding="utf-8"))
            refs = set(re.findall(rf"\b(?:{prefixes})-\d{{4}}\b", body)) if prefixes else set()
            if own:
                refs.discard(own.group(0))
            if not refs and not re.search(r"(?i)superseded by\s*[:\-]?\s*\[", body):
                self.err(f"{self.rel(p)}: superseded but names no replacement")

        # 9: placeholders
        if cfg.initialized:
            for p in files:
                r = self.rel(p)
                if r.startswith("meta/templates/"):
                    continue
                hits = sorted(set(md.PLACEHOLDER_RE.findall(md.strip_code(texts[p]))))
                if hits:
                    self.err(f"{r}: unfilled placeholder(s) {', '.join(hits)}")

        # 10: outbox drafts
        outbox = self.root / cfg.ops.get("outbox_dir", "ops/outbox")
        if outbox.is_dir():
            for f in sorted(outbox.glob("*.md")):
                if f.name == "README.md":
                    continue
                fm = md.parse_frontmatter(f.read_text(encoding="utf-8"))
                r = self.rel(f)
                if fm is None:
                    self.err(f"{r}: outbox draft missing frontmatter")
                    continue
                for key in ("forge", "repo", "action", "state"):
                    if not fm.get(key):
                        self.err(f"{r}: outbox draft missing '{key}'")
                if fm.get("action") and fm["action"] not in OUTBOX_ACTIONS:
                    self.err(f"{r}: unknown action '{fm['action']}'")
                if fm.get("state") and fm["state"] not in OUTBOX_STATES:
                    self.err(f"{r}: unknown state '{fm['state']}'")
                if fm.get("state") == "posted" and not fm.get("posted_url"):
                    self.err(f"{r}: posted draft has no posted_url")

        # 11: aliases. Real terms behind aliases never appear in the KB (they live in .kb-aliases.env only)
        from . import aliases as al
        amap = al.load(cfg)
        if al.is_tracked(cfg):
            self.err(f"{al.path(cfg).name} is tracked by git. It must stay local: git rm --cached {al.path(cfg).name}")
        if amap:
            skip = {al.path(cfg).resolve(), (self.root / "meta/templates/kb-aliases.env").resolve(),
                    (self.root / "answers.json").resolve()}
            candidates = [f for f in self.root.rglob("*") if f.is_file() and ".git" not in f.relative_to(self.root).parts]
            if (self.root / ".git").exists():  # git-ignored files are never committed, so they can't leak
                import subprocess
                r = subprocess.run(["git", "-C", str(self.root), "check-ignore", "--stdin"], capture_output=True, text=True,
                                   input="\n".join(self.rel(f) for f in candidates))
                skip |= {(self.root / line).resolve() for line in r.stdout.splitlines() if line}
            for f in candidates:
                if not f.is_file() or f.resolve() in skip or f.suffix not in (".md", ".json", ".yml", ".yaml", ".txt", ".env", ".py", ".sh", ".svg", ".csv"):
                    continue
                parts = f.relative_to(self.root).parts
                if any(x in (".git", "node_modules", "__pycache__", ".kbtemplate", "tools") for x in parts):
                    continue
                for alias, line in al.find(f.read_text(encoding="utf-8", errors="replace"), amap):
                    self.err(f"{self.rel(f)}:{line}: contains the real term behind alias {alias}. Write {alias} instead")
        elif cfg.initialized and not al.path(cfg).exists() and cfg.privacy.get("aliases_expected"):
            self.warnings.append(f"no {al.path(cfg).name}: alias leak checks are off. Ask the owner for the file")

        for w in self.warnings:
            print(f"  ! {w}")

        # report
        docs = len(statuses)
        if self.errors:
            print(f"kb check: {len(self.errors)} problem(s) in {len(files)} files\n")
            for e in self.errors:
                print(f"  ✗ {e}")
            return 1
        by_status: dict[str, int] = {}
        for s in statuses.values():
            by_status[s] = by_status.get(s, 0) + 1
        summary = ", ".join(f"{k} {v}" for k, v in sorted(by_status.items())) or "none"
        id_summary = ", ".join(f"{len(v)} {k}" for k, v in known.items())
        mode = "" if cfg.initialized else " [template mode: placeholders allowed]"
        print(f"kb check: OK. {len(files)} markdown files, {docs} knowledge docs ({summary}); {id_summary}{mode}")
        return 0


def run(cfg: Config) -> int:
    return Checker(cfg).run()
