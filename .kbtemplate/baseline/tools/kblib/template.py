"""`kb.py template`: stay in sync with the upstream template, without a blind pull.

A KB made from the template has diverged on purpose (rendered names, removed roles, local edits),
so upstream changes can't simply be merged. At init, kb.py records a baseline in .kbtemplate/:

    .kbtemplate/VERSION          template version this KB is based on
    .kbtemplate/manifest.json    per managed file: upstream source path, hash as shipped, hash as installed,
                                 plus the placeholder values used to render it
    .kbtemplate/baseline/        the shipped (unrendered) copy of each managed file

`template plan` fetches upstream and classifies every managed file:

    safe        upstream changed, you didn't        -> `apply` re-renders the new upstream version
    merge       both changed                         -> `apply` tries a 3-way merge; conflicts are left
                                                        with markers for the agent and operator to resolve
    new         new upstream file                    -> offered; `apply --new` installs it
    removed     upstream deleted it                  -> listed; you decide
    local-only  you removed it (e.g. a disabled role) -> left alone

The agent follows playbooks/template-sync.md and never applies anything the operator hasn't agreed to.
"""
from __future__ import annotations

import fnmatch
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from .config import Config

STATE_DIR = ".kbtemplate"
DEFAULT_UPSTREAM = "https://github.com/aurimasniekis/llm-knowledge-base-template"
DEFAULT_MANAGED = [
    "tools/kb.py", "tools/kblib/*", "tools/kblib/forges/*", ".githooks/*",
    "meta/templates/*", "meta/conventions.md", "meta/commit-convention.md", "meta/session-protocol.md",
    "meta/authority.md", "meta/README.md", "playbooks/*", ".claude/skills/*/SKILL.md", "kits/code-repo/*",
    "ci/agent/*", ".github/ISSUE_TEMPLATE/*", ".github/PULL_REQUEST_TEMPLATE.md", ".github/workflows/kb-check.yml",
    ".github/workflows/pr-title.yml", ".gitlab/issue_templates/*", ".gitlab/merge_request_templates/*", ".gitlab-ci.yml",
    ".forgejo/issue_template/*", ".forgejo/pull_request_template.md", ".forgejo/workflows/*", "bitbucket-pipelines.yml",
    "AGENTS.md", "CLAUDE.md", "GEMINI.md", "CONTRIBUTING.md", "agents/inbox/README.md", "ops/README.md",
    "ops/digests/README.md", "ops/outbox/README.md", f"{STATE_DIR}/CHANGELOG.md",
]
# Installed path -> upstream source path, when they differ.
SOURCE_ALIASES = {
    ".github/workflows/ops-round.yml": "ci/agent/github-ops-round.yml",
    ".forgejo/workflows/ops-round.yml": "ci/agent/forgejo-ops-round.yml",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def is_managed(rel: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(rel, p) for p in patterns) and "__pycache__" not in rel and not rel.endswith(".pyc")


def snapshot_sources(root: Path, patterns: list[str]) -> dict[str, bytes]:
    """Read every managed file of a pristine template (call before init changes anything)."""
    out: dict[str, bytes] = {}
    for p in root.rglob("*"):
        if not p.is_file() or ".git" in p.parts:
            continue
        rel = p.relative_to(root).as_posix()
        if is_managed(rel, patterns) or rel.startswith(("presets/", "ci/agent/")):
            out[rel] = p.read_bytes()
    return out


def render(text: str, values: dict[str, str]) -> str:
    for k, v in values.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def source_for(rel: str, preset: str, sources: dict[str, bytes]) -> str | None:
    if rel in SOURCE_ALIASES:
        return SOURCE_ALIASES[rel]
    if rel.startswith("meta/templates/"):
        alt = f"presets/{preset}/templates/{rel.split('/')[-1]}"
        if alt in sources:
            return alt
    return rel if rel in sources else None


def write_baseline(root: Path, sources: dict[str, bytes], preset: str, values: dict[str, str], patterns: list[str]) -> int:
    """Called at the end of init: record what was shipped and what was installed."""
    state = root / STATE_DIR
    base = state / "baseline"
    if base.exists():
        shutil.rmtree(base)
    files = {}
    for p in sorted(root.rglob("*")):
        if not p.is_file() or ".git" in p.parts or STATE_DIR + "/baseline" in p.as_posix():
            continue
        rel = p.relative_to(root).as_posix()
        if not (is_managed(rel, patterns) or rel in SOURCE_ALIASES):
            continue
        src = source_for(rel, preset, sources)
        if src is None:
            continue
        shipped = sources[src]
        dst = base / src
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(shipped)
        files[rel] = {"source": src, "shipped": sha(shipped), "installed": sha(p.read_bytes())}
    installed_sources = {e["source"] for e in files.values()}
    excluded = sorted(src for src in sources if is_managed(src, patterns) and src not in installed_sources
                      and not (root / src).exists())
    manifest = {"preset": preset, "values": values, "managed": patterns, "files": files, "excluded": excluded}
    (state / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(files)


# -- commands --------------------------------------------------------------------
def load_manifest(root: Path) -> dict:
    p = root / STATE_DIR / "manifest.json"
    if not p.exists():
        raise SystemExit("template: no .kbtemplate/manifest.json. This KB has no baseline "
                         "(made before sync support, or still a fresh template). See playbooks/template-sync.md, 'No baseline'.")
    return json.loads(p.read_text(encoding="utf-8"))


def upstream_dir(cfg: Config) -> Path:
    return cfg.root / STATE_DIR / "upstream"


def fetch(cfg: Config, source: str | None, ref: str | None) -> Path:
    """Clone (or copy, for a local path) the upstream template into .kbtemplate/upstream (git-ignored)."""
    t = cfg.get("template", {})
    src = source or t.get("upstream") or DEFAULT_UPSTREAM
    dst = upstream_dir(cfg)
    if dst.exists():
        shutil.rmtree(dst)
    if Path(src).expanduser().is_dir():
        shutil.copytree(Path(src).expanduser(), dst, ignore=shutil.ignore_patterns(".git", "__pycache__", "upstream", "baseline", "manifest.json"))
    else:
        cmd = ["git", "clone", "-q", "--depth", "1"] + (["--branch", ref] if ref else []) + [src, str(dst)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"template: could not fetch {src}: {r.stderr.strip()}")
    return dst


def classify(cfg: Config, up: Path) -> dict[str, list]:
    man = load_manifest(cfg.root)
    patterns = man.get("managed", DEFAULT_MANAGED)
    res: dict[str, list] = {"safe": [], "merge": [], "new": [], "removed": [], "local-only": [], "same": [], "not-applicable": []}
    known_sources = set()
    for rel, ent in sorted(man["files"].items()):
        src = ent["source"]
        known_sources.add(src)
        local = cfg.root / rel
        upf = up / src
        if not local.exists():
            res["local-only"].append(rel)
            continue
        if not upf.exists():
            res["removed"].append(rel)
            continue
        if sha(upf.read_bytes()) == ent["shipped"]:
            res["same"].append(rel)
            continue
        if sha(local.read_bytes()) == ent["installed"]:
            res["safe"].append(rel)
        else:
            res["merge"].append(rel)
    preset = man.get("preset", "")
    excluded = set(man.get("excluded", []))
    # whole folders left out at setup (another forge's files, a disabled role's folder)
    excluded_dirs = {e.rsplit("/", 1)[0] for e in excluded if "/" in e and not (cfg.root / e.rsplit("/", 1)[0]).exists()}
    for p in sorted(up.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(up).as_posix()
        if rel in known_sources or not is_managed(rel, patterns):
            continue
        if rel in excluded or any(rel.startswith(d + "/") for d in excluded_dirs):
            res["not-applicable"].append(rel)
            continue
        if not (cfg.root / rel).exists():
            res["new"].append(rel)
    pt = up / "presets" / preset / "templates"
    if pt.is_dir():
        for p in sorted(pt.iterdir()):
            src = p.relative_to(up).as_posix()
            if src not in known_sources and not (cfg.root / "meta/templates" / p.name).exists():
                res["new"].append(f"meta/templates/{p.name}  (from {src})")
    return res


def version_of(path: Path) -> str:
    v = path / STATE_DIR / "VERSION"
    return v.read_text().strip() if v.exists() else "unknown"


def cmd_status(cfg: Config) -> int:
    t = cfg.get("template", {})
    print(f"template upstream: {t.get('upstream', DEFAULT_UPSTREAM)}")
    print(f"based on version:  {version_of(cfg.root)}")
    print(f"last synced:       {t.get('synced', 'never')}")
    man = cfg.root / STATE_DIR / "manifest.json"
    print(f"baseline:          {'yes' if man.exists() else 'missing'}")
    return 0


def cmd_plan(cfg: Config, source: str | None, ref: str | None, no_fetch: bool) -> int:
    up = upstream_dir(cfg) if no_fetch and upstream_dir(cfg).exists() else fetch(cfg, source, ref)
    res = classify(cfg, up)
    cur, new = version_of(cfg.root), version_of(up)
    lines = [f"# Template sync plan: {cur} → {new}", ""]
    labels = {
        "safe": "Safe updates (upstream changed, you didn't): `template apply <file>` re-renders them",
        "merge": "Both changed: `template apply <file>` tries a 3-way merge; resolve conflicts with the operator",
        "new": "New upstream files: offer them; install with `template apply --new <file>`",
        "removed": "Removed upstream: decide whether to delete locally",
        "local-only": "Removed locally (e.g. disabled roles): left alone",
    }
    for key, label in labels.items():
        lines += [f"## {label}", ""]
        lines += [f"- `{r}`" for r in res[key]] or ["- none"]
        lines.append("")
    lines.append(f"Unchanged upstream: {len(res['same'])} file(s). Not applicable (left out at setup): {len(res['not-applicable'])} file(s).")
    log = up / STATE_DIR / "CHANGELOG.md"
    if log.exists():
        lines += ["", "## Upstream changelog (read the entries after your version)", "", log.read_text(encoding="utf-8")[:6000]]
    report = "\n".join(lines) + "\n"
    (cfg.root / STATE_DIR / "sync-plan.md").write_text(report, encoding="utf-8")
    print(report)
    print(f"(saved to {STATE_DIR}/sync-plan.md)")
    return 0


def _rendered(cfg: Config, text: bytes, values: dict) -> bytes:
    try:
        return render(text.decode("utf-8"), values).encode("utf-8")
    except UnicodeDecodeError:
        return text


def cmd_apply(cfg: Config, paths: list[str], new: bool) -> int:
    man = load_manifest(cfg.root)
    up = upstream_dir(cfg)
    if not up.exists():
        raise SystemExit("template: run `kb.py template plan` first (it fetches upstream).")
    values = man.get("values", {})
    rc = 0
    for rel in paths:
        rel = rel.split("  (from ")[0].strip()
        local = cfg.root / rel
        if new:
            src = rel
            if not (up / src).exists() and rel.startswith("meta/templates/"):
                src = f"presets/{man.get('preset')}/templates/{rel.split('/')[-1]}"
            if not (up / src).exists():
                print(f"✗ {rel}: not in upstream")
                rc = 1
                continue
            data = _rendered(cfg, (up / src).read_bytes(), values)
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_bytes(data)
            _record(cfg, man, rel, src, up)
            print(f"✓ {rel}: installed from upstream")
            continue
        ent = man["files"].get(rel)
        if not ent:
            print(f"✗ {rel}: not a managed file (use --new for new upstream files)")
            rc = 1
            continue
        upf = up / ent["source"]
        new_r = _rendered(cfg, upf.read_bytes(), values)
        if sha(local.read_bytes()) == ent["installed"]:
            local.write_bytes(new_r)
            _record(cfg, man, rel, ent["source"], up)
            print(f"✓ {rel}: updated")
            continue
        base_file = cfg.root / STATE_DIR / "baseline" / ent["source"]
        base_r = _rendered(cfg, base_file.read_bytes(), values) if base_file.exists() else b""
        with tempfile.TemporaryDirectory() as td:
            b, n = Path(td) / "base", Path(td) / "upstream"
            b.write_bytes(base_r)
            n.write_bytes(new_r)
            r = subprocess.run(["git", "merge-file", "-L", "yours", "-L", "template (old)", "-L", "template (new)",
                                str(local), str(b), str(n)], capture_output=True, text=True)
        if r.returncode == 0:
            _record(cfg, man, rel, ent["source"], up)
            print(f"✓ {rel}: merged cleanly (review the result)")
        else:
            print(f"! {rel}: {r.returncode} conflict(s). Resolve the <<<<<<< markers, then `kb.py template resolve {rel}`")
            rc = 1
    _save(cfg, man)
    return rc


def cmd_resolve(cfg: Config, paths: list[str]) -> int:
    man = load_manifest(cfg.root)
    up = upstream_dir(cfg)
    for rel in paths:
        text = (cfg.root / rel).read_text(encoding="utf-8")
        if "<<<<<<< yours" in text:
            print(f"✗ {rel}: still has conflict markers")
            return 1
        _record(cfg, man, rel, man["files"][rel]["source"], up)
        print(f"✓ {rel}: marked resolved")
    _save(cfg, man)
    return 0


def cmd_diff(cfg: Config, rel: str) -> int:
    """What upstream changed in this file since your baseline (old template → new template)."""
    man = load_manifest(cfg.root)
    ent = man["files"].get(rel)
    src = ent["source"] if ent else rel
    old = cfg.root / STATE_DIR / "baseline" / src
    new = upstream_dir(cfg) / src
    r = subprocess.run(["git", "diff", "--no-index", "--", str(old) if old.exists() else "/dev/null", str(new)],
                       capture_output=True, text=True)
    print(r.stdout or "(no upstream change)")
    return 0


def cmd_finish(cfg: Config) -> int:
    """Adopt the upstream version once every planned change is applied, resolved or declined."""
    up = upstream_dir(cfg)
    v = up / STATE_DIR / "VERSION"
    if v.exists():
        (cfg.root / STATE_DIR / "VERSION").write_text(v.read_text())
    log = up / STATE_DIR / "CHANGELOG.md"
    if log.exists():
        (cfg.root / STATE_DIR / "CHANGELOG.md").write_text(log.read_text())
    import datetime as _dt
    cfg.data.setdefault("template", {})["synced"] = _dt.date.today().isoformat()
    cfg.data["template"]["version"] = version_of(cfg.root)
    cfg.save()
    shutil.rmtree(up, ignore_errors=True)
    print(f"template: now based on {version_of(cfg.root)}. Commit with: meta(template): sync with template {version_of(cfg.root)}")
    return 0


def _record(cfg: Config, man: dict, rel: str, src: str, up: Path) -> None:
    data = (up / src).read_bytes()
    base = cfg.root / STATE_DIR / "baseline" / src
    base.parent.mkdir(parents=True, exist_ok=True)
    base.write_bytes(data)
    man["files"][rel] = {"source": src, "shipped": sha(data), "installed": sha((cfg.root / rel).read_bytes())}


def _save(cfg: Config, man: dict) -> None:
    (cfg.root / STATE_DIR / "manifest.json").write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
