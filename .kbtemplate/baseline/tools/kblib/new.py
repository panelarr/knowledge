"""`kb.py new`: create a doc from a template with the next free ID and add its index row."""
from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

from . import md
from .config import Config

KIND_TO_PREFIX = {"adr": "ADR", "question": "Q", "input": "IN", "feature": "FEAT", "goal": "GOAL"}


def slugify(title: str, limit: int = 60) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:limit].rstrip("-") or "untitled"


def today() -> str:
    return _dt.date.today().isoformat()


def next_number(cfg: Config, prefix: str) -> int:
    spec = cfg.ids[prefix]
    nums = [0]
    d = cfg.root / spec.get("dir", "")
    if d.is_dir():
        for f in d.glob(f"{prefix}-*.md"):
            m = re.match(rf"{re.escape(prefix)}-(\d{{4}})", f.name)
            if m:
                nums.append(int(m.group(1)))
    idx = cfg.root / spec.get("index", "")
    if idx.exists():
        nums += [int(n) for n in re.findall(rf"\b{re.escape(prefix)}-(\d{{4}})\b", idx.read_text(encoding="utf-8"))]
    return max(nums) + 1


def render(text: str, values: dict[str, str]) -> str:
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def base_values(cfg: Config) -> dict[str, str]:
    p = cfg.project
    return {
        "PROJECT_NAME": p.get("name", ""),
        "PROJECT_SLUG": p.get("slug", ""),
        "OWNER": p.get("owner", ""),
        "KEEPER_SESSION": p.get("keeper_session", ""),
        "TODAY": today(),
    }


def append_row(index: Path, values: dict[str, str], table: int = 0) -> None:
    """Append a row to the `table`-th Markdown table in `index`, matching columns by header name."""
    lines = index.read_text(encoding="utf-8").splitlines()
    tables, i = [], 0
    while i < len(lines) - 1:
        if lines[i].startswith("|") and re.match(r"^\|\s*:?-{2,}", lines[i + 1]):
            start = i
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            tables.append((start, j))
            i = j
        else:
            i += 1
    if not tables:
        lines += ["", "| Doc | Holds | Status |", "|---|---|---|"]
        tables.append((len(lines) - 2, len(lines)))
    start, end = tables[min(table, len(tables) - 1)]
    headers = [h.strip().lower() for h in lines[start].strip().strip("|").split("|")]
    cells = []
    for h in headers:
        if h in ("id", "adr", "doc", "entry", "goal", "feature", "input", "file", "test plan", "report"):
            cells.append(values.get("link", ""))
        elif h in ("status", "state"):
            cells.append(values.get("status", ""))
        elif h in ("date", "received", "updated", "created"):
            cells.append(values.get("date", ""))
        elif h in ("pri", "priority"):
            cells.append(values.get("pri", "P2"))
        elif h == "area":
            cells.append(values.get("area", ""))
        elif h in ("raised in", "source"):
            cells.append(values.get("raised", "—"))
        elif h in ("distilled into", "answer", "owner", "session", "milestone"):
            cells.append(values.get(h, "—"))
        else:
            cells.append(values.get("title", ""))
    lines.insert(end, "| " + " | ".join(cells) + " |")
    index.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_template(cfg: Config, name: str) -> str:
    path = cfg.root / "meta" / "templates" / name
    if not path.exists():
        raise SystemExit(f"new: template meta/templates/{name} not found")
    return path.read_text(encoding="utf-8")


def run(cfg: Config, kind: str, title: str, area: str | None, status: str | None,
        pri: str | None, template: str | None, with_file: bool) -> int:
    values = base_values(cfg)
    values.update({"TITLE": title, "SLUG": slugify(title), "AREA": area or ""})
    date = values["TODAY"]

    if kind == "journal":
        path = cfg.root / "journal" / f"{date}-{slugify(title)}.md"
        text = render(load_template(cfg, "journal.md"), values)
        _write_new(path, text)
        append_row(cfg.root / "journal" / "README.md",
                   {"date": date, "link": f"[{title}]({path.name})", "title": "—"})
        return _done(cfg, path)

    if kind == "doc":
        if not area:
            raise SystemExit("new doc: pass --area <folder> (e.g. product, architecture/api)")
        folder = cfg.root / area
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{slugify(title)}.md"
        values["STATUS"] = status or "seed"
        text = render(load_template(cfg, template or "concept.md"), values)
        text = md.set_frontmatter(text, {"status": values["STATUS"]})
        _write_new(path, text)
        index = folder / "README.md"
        if not index.exists():
            index.write_text(f"# {area.split('/')[-1].replace('-', ' ').title()}\n\n| Doc | Holds | Status |\n|---|---|---|\n", encoding="utf-8")
        append_row(index, {"link": f"[{path.name}]({path.name})", "title": title, "status": values["STATUS"]})
        return _done(cfg, path)

    prefix = KIND_TO_PREFIX.get(kind)
    if not prefix or prefix not in cfg.ids:
        raise SystemExit(f"new: unknown kind '{kind}' (or its ID family is not enabled in kb.config.json)")
    spec = cfg.ids[prefix]
    num = f"{next_number(cfg, prefix):04d}"
    ident = f"{prefix}-{num}"
    values["ID"] = ident
    st = status or {"ADR": "proposed", "Q": "draft", "FEAT": "draft", "GOAL": "draft"}.get(prefix, "draft")
    values["STATUS"] = st
    index = cfg.root / spec["index"]
    d = cfg.root / spec["dir"]
    d.mkdir(parents=True, exist_ok=True)

    if spec.get("kind") == "register":
        link = ident
        path = None
        if with_file:
            path = d / f"{ident}-{slugify(title)}.md"
            _write_new(path, render(load_template(cfg, spec["template"]), values))
            link = f"[{ident}]({path.name})"
        append_row(index, {"link": link, "title": title, "area": area or "", "pri": pri or "P2", "raised": "—"})
        print(f"new: registered {ident} in {spec['index']}")
        return _done(cfg, path) if path else 0

    path = d / f"{ident}-{slugify(title)}.md"
    text = render(load_template(cfg, spec["template"]), values)
    if prefix != "IN":
        text = md.set_frontmatter(text, {"status": st})
    _write_new(path, text)
    rel_link = Path(path).relative_to(index.parent).as_posix()
    append_row(index, {"link": f"[{ident}]({rel_link})", "title": title, "status": st, "date": date})
    return _done(cfg, path)


def _write_new(path: Path, text: str) -> None:
    if path.exists():
        raise SystemExit(f"new: {path} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _done(cfg: Config, path: Path | None) -> int:
    if path:
        print(f"new: created {path.relative_to(cfg.root).as_posix()} (index updated; fill it in, then run kb.py check)")
    return 0
