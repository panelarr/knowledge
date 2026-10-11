"""`kb.py init`: turn the template into your knowledge base.

Answers come from (later wins): an example's answers.json, --answers FILE (written by an agent
following SETUP.md), --preset, then an interactive questionnaire for anything still missing
(skipped with --yes, which takes defaults). Then init:

  1. applies the domain preset (areas, starter docs, templates, commit types)
  2. removes the parts of disabled roles, and unused forge/agent/CI files
  3. overlays the example's content (when starting from one)
  4. writes kb.config.json, README.md, NOTICE.md, IN-0001 (the answers), IN-0002 (seed text)
  5. renders {{PLACEHOLDERS}}, prunes links to anything removed
  6. removes template-only files, optionally runs git init + hooks, runs the check

It never commits.
"""
from __future__ import annotations

import copy
import datetime as _dt
import json
import re
import shutil
import subprocess
from pathlib import Path

from . import md
from .config import Config
from .new import append_row, slugify

ROLE_KEYS = ["product_owner", "project_manager", "agent_manager", "qa", "docs_writer", "support"]
ROLE_LABELS = {
    "product_owner": "Product owner (features, acceptance criteria, scope)",
    "project_manager": "Project manager (roadmap, milestones, status reports)",
    "agent_manager": "Agent manager (goal briefs, coding sessions, worktrees)",
    "qa": "QA / tester (test plans, verification, bug reports)",
    "docs_writer": "Docs writer (public docs, release notes)",
    "support": "Support (issue triage, replies, FAQ)",
}
ROLE_PATHS = {
    "product_owner": ["planning/features", "playbooks/product-owner.md", ".claude/skills/kb-product-owner", "meta/templates/feature.md"],
    "project_manager": ["planning/roadmap.md", "planning/status", "playbooks/project-manager.md", ".claude/skills/kb-project-manager",
                        "meta/templates/status-report.md"],
    "agent_manager": ["agents/goals", "playbooks/agent-manager.md", "playbooks/onboarding-a-code-repo.md", ".claude/skills/kb-agent-manager",
                      ".claude/skills/kb-onboard-repo", "meta/templates/goal.md", "kits"],
    "qa": ["qa", "playbooks/qa.md", ".claude/skills/kb-qa", "meta/templates/test-plan.md", "meta/templates/test-report.md", "meta/templates/bug.md"],
    "docs_writer": ["playbooks/docs-writer.md", ".claude/skills/kb-docs-writer"],
    "support": ["support", "playbooks/support.md", ".claude/skills/kb-support", "meta/templates/reply.md"],
}
OPS_AREAS = {
    "planning": ("Roadmap, milestones, features with acceptance criteria, releases, status reports", "What gets delivered, and when?"),
    "agents": ("Coding-session board, goal briefs, inbox for session messages", "Who is working on what?"),
    "qa": ("Test plans, test reports, regression list", "Does it work, and how do we know?"),
    "support": ("FAQ, known issues, reusable replies", "What do users ask, and what do we answer?"),
    "ops": ("Forge digests and the outbox of drafted comments and reviews", "What's happening on the forges?"),
    "playbooks": ("How the agent performs each role", "How does the agent do its job?"),
}
CORE_AREAS = {
    "decisions": ("Decision records (ADRs)", "What did we decide, and what did we reject?"),
    "questions": ("Open-question register", "What don't we know yet?"),
    "inputs": ("The owner's words, verbatim and immutable", "Where did an idea come from?"),
    "journal": ("One entry per working session", "What happened in each session?"),
    "meta": ("Conventions, commit convention, protocols, authority, glossary, templates", "How does this KB work?"),
}
FORGE_FILES = {
    "github": [".github"],
    "gitlab": [".gitlab", ".gitlab-ci.yml"],
    "gitea": [".forgejo"],
    "bitbucket": ["bitbucket-pipelines.yml"],
}
DEFAULT_AUTHORITY = {
    "kb_commit": "ask", "kb_push": "never", "comment": "draft", "review": "draft", "label": "draft", "assign": "draft",
    "open_issue": "draft", "close": "never", "merge": "never", "push_code": "never", "dispatch_session": "draft",
    "create_worktree": "draft",
}
UNIVERSAL_TYPES = {
    "idea": "A new idea enters the KB as seed",
    "decide": "An ADR is added or changes status",
    "question": "Questions added, reframed or answered",
    "refine": "Clarify, reword, split or merge without changing meaning",
    "struct": "Folders, indexes, moves, renames",
    "input": "Owner inputs imported into inputs/",
    "meta": "Conventions, templates, tooling, protocols, playbooks",
    "journal": "Journal-only entries",
}
TEMPLATE_URL = "https://github.com/aurimasniekis/llm-knowledge-base-template"
TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".txt"}


# -- answers -------------------------------------------------------------------
def deep_merge(base: dict, over: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        val = input(f"{prompt}{suffix}: ").strip()
    except EOFError:
        val = ""
    return val or default


def ask_bool(prompt: str, default: bool) -> bool:
    val = ask(prompt + " (y/n)", "y" if default else "n").lower()
    return val.startswith("y")


def ask_choice(prompt: str, choices: list[str], default: str) -> str:
    while True:
        val = ask(f"{prompt} ({' / '.join(choices)})", default)
        if val in choices:
            return val
        print(f"  choose one of: {', '.join(choices)}")


def questionnaire(root: Path, a: dict) -> dict:
    """Interactive version of SETUP.md. Only asks what isn't answered yet."""
    print("\nKnowledge base setup. Press Enter to accept the [default]. Full guide: SETUP.md\n")
    p = a.setdefault("project", {})
    print("1/7 Project")
    p["name"] = p.get("name") or ask("  Project name", "My Project")
    p["pitch"] = p.get("pitch") or ask("  One-line pitch (what is it, for whom?)", "")
    p["owner"] = p.get("owner") or ask("  Owner: who decides what becomes accepted (name or @handle)", "Owner")
    presets = sorted(d.name for d in (root / "presets").iterdir() if (d / "preset.json").exists())
    a["preset"] = a.get("preset") or ask_choice("  Kind of project", presets, "software")
    a["mode"] = a.get("mode") or ask_choice("  Who works in it", ["solo", "agents", "team"], "agents")

    print("\n2/7 Roles the agent performs")
    preset_roles = json.loads((root / "presets" / a["preset"] / "preset.json").read_text())["roles"]
    roles = a.setdefault("roles", {})
    for key in ROLE_KEYS:
        if key not in roles:
            roles[key] = ask_bool(f"  {ROLE_LABELS[key]}", preset_roles.get(key, True))

    print("\n3/7 Agents")
    if "agents" not in a:
        a["agents"] = [x.strip() for x in ask("  Agents you use (claude, codex, cursor, gemini, other)", "claude,codex").split(",") if x.strip()]
    p["keeper_session"] = p.get("keeper_session") or ask("  Name of the keeper session", f"{slugify(p['name'])}-knowledge")

    print("\n4/7 Authority (never / ask / draft / auto). Details: meta/authority.md")
    auth = a.setdefault("authority", {})
    if "kb_commit" not in auth:
        auth["kb_commit"] = ask_choice("  May the agent commit in this KB", ["ask", "auto", "never"], "ask")
    if "kb_push" not in auth:
        auth["kb_push"] = ask_choice("  May it push the KB", ["never", "ask", "auto"], "never")
    if "comment" not in auth:
        lvl = ask_choice("  Comments, reviews, labels on issues/PRs", ["draft", "never", "auto"], "draft")
        for k in ("comment", "review", "label", "assign", "open_issue"):
            auth.setdefault(k, lvl)

    print("\n5/7 Forge and collaboration")
    a["forge"] = a.get("forge") or ask_choice("  Where the repos live", ["github", "gitlab", "gitea", "bitbucket", "none"], "github")
    col = a.setdefault("collaboration", {})
    if "templates" not in col:
        col["templates"] = a["forge"] != "none" and ask_bool("  Issue/PR templates + CONTRIBUTING for contributors", a["mode"] == "team")
    if "ci_check" not in col:
        col["ci_check"] = a["forge"] != "none" and ask_bool("  CI that runs the KB check on PRs", True)
    if "ci_agent" not in col:
        col["ci_agent"] = a["forge"] not in ("none", "bitbucket") and ask_bool("  Optional scheduled agent rounds in CI (needs API key secrets)", False)
    kb = a.setdefault("kb", {})
    if "visibility" not in kb:
        kb["visibility"] = ask_choice("  Is this KB repo public or private", ["private", "public"], "private")
    if "url" not in kb:
        kb["url"] = ask("  Web URL of this KB repo (blank if none yet)", "")

    print("\n6/7 Privacy")
    priv = a.setdefault("privacy", {})
    if "enabled" not in priv:
        priv["enabled"] = kb["visibility"] == "private" and ask_bool(
            "  Privacy mode: code repos are public and must never mention this KB", False)
    if "secrets" not in a:
        a["secrets"] = ask_bool("  Secrets area for owner-only truths (story secrets, unannounced plans)", False)
    if "license" not in a:
        a["license"] = ask_choice("  Licence for this KB", ["keep", "own-open", "proprietary", "none"], "proprietary" if kb["visibility"] == "private" else "own-open")

    print("\n7/7 Git and seed")
    g = a.setdefault("git", {})
    if "init" not in g and not (root / ".git").exists():
        g["init"] = ask_bool("  Run git init", True)
    if "hooks" not in g:
        g["hooks"] = ask_bool("  Enable the git hooks (check + commit message)", True)
    if "seed" not in a:
        print("  Paste your idea dump / project notes (finish with a line containing only END), or just END to skip:")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line.strip() == "END":
                break
            lines.append(line)
        a["seed"] = {"title": "Initial idea dump", "text": "\n".join(lines).strip()}
    return a


def normalize(a: dict, root: Path) -> dict:
    p = a.setdefault("project", {})
    p.setdefault("name", "My Project")
    p.setdefault("slug", slugify(p["name"]))
    p.setdefault("pitch", "")
    p.setdefault("owner", "Owner")
    p.setdefault("keeper_session", f"{p['slug']}-knowledge")
    p.setdefault("language", "en")
    a.setdefault("preset", "software")
    if not (root / "presets" / a["preset"] / "preset.json").exists():
        raise SystemExit(f"init: unknown preset '{a['preset']}'")
    a.setdefault("mode", "agents")
    preset_roles = json.loads((root / "presets" / a["preset"] / "preset.json").read_text())["roles"]
    roles = a.setdefault("roles", {})
    for k in ROLE_KEYS:
        roles.setdefault(k, preset_roles.get(k, True))
    a.setdefault("agents", ["claude", "codex"])
    a.setdefault("repos", [])
    a["authority"] = dict(DEFAULT_AUTHORITY, **a.get("authority", {}))
    a.setdefault("forge", "github")
    if a["forge"] in ("forgejo", "codeberg"):
        a["forge"] = "gitea"
    col = a.setdefault("collaboration", {})
    col.setdefault("templates", a["mode"] == "team")
    col.setdefault("ci_check", a["forge"] != "none")
    col.setdefault("ci_agent", False)
    col.setdefault("codeowners", "")
    kb = a.setdefault("kb", {})
    kb.setdefault("visibility", "private")
    kb.setdefault("url", "")
    priv = a.setdefault("privacy", {})
    priv.setdefault("enabled", False)
    priv.setdefault("extra_patterns", [])
    a.setdefault("secrets", False)
    a.setdefault("license", "proprietary" if kb["visibility"] == "private" else "own-open")
    areas = a.setdefault("areas", {})
    areas.setdefault("add", [])
    areas.setdefault("remove", [])
    g = a.setdefault("git", {})
    g.setdefault("init", False)
    g.setdefault("hooks", True)
    a.setdefault("seed", {})
    return a


# -- file operations -----------------------------------------------------------
class Plan:
    def __init__(self, root: Path, dry_run: bool):
        self.root = root
        self.dry = dry_run
        self.removed: set[Path] = set()
        self.log: list[str] = []

    def rm(self, rel: str) -> None:
        path = self.root / rel
        if not path.exists():
            return
        self.removed.add(path.resolve())
        self.log.append(f"remove  {rel}")
        if self.dry:
            return
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()

    def copytree(self, src: Path, dst_rel: str = "") -> None:
        for f in sorted(src.rglob("*")):
            if f.is_dir() or f.name == ".DS_Store":
                continue
            rel = (Path(dst_rel) / f.relative_to(src)).as_posix()
            self.log.append(f"write   {rel}")
            if not self.dry:
                dst = self.root / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)

    def write(self, rel: str, text: str) -> None:
        self.log.append(f"write   {rel}")
        if not self.dry:
            dst = self.root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(text, encoding="utf-8")


def text_files(root: Path) -> list[Path]:
    skip = {".git", "node_modules", "__pycache__"}
    return [p for p in root.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES
            and not any(part in skip for part in p.relative_to(root).parts)]


def prune_links(root: Path, removed: set[Path]) -> None:
    """Unlink references to removed files: drop index rows that point at them, keep other link labels as text."""
    if not removed:
        return

    def gone(target: Path) -> bool:
        t = target.resolve()
        return any(t == r or r in t.parents for r in removed)

    link = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)\)")
    for p in root.rglob("*.md"):
        if ".git" in p.parts:
            continue
        text = p.read_text(encoding="utf-8")
        new_lines = []
        changed = False
        for line in text.splitlines():
            targets = [m.group(3).split("#")[0] for m in link.finditer(line) if not re.match(r"^[a-z]+:", m.group(3))]
            dead = [t for t in targets if t and gone(p.parent / t)]
            if dead and line.lstrip().startswith("|") and targets and targets[0] in dead:
                changed = True
                continue
            if dead:
                def repl(m):
                    tgt = m.group(3).split("#")[0]
                    if tgt and not re.match(r"^[a-z]+:", m.group(3)) and gone(p.parent / tgt):
                        return m.group(2)
                    return m.group(0)
                line = link.sub(repl, line)
                changed = True
            if line.startswith("related:"):
                items = md.parse_list(line[len("related:"):])
                kept = [i for i in items if not gone(root / i)]
                if kept != items:
                    line = f"related: [{', '.join(kept)}]"
                    changed = True
            new_lines.append(line)
        if changed:
            p.write_text("\n".join(new_lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")


def render_all(root: Path, values: dict[str, str]) -> None:
    for p in text_files(root):
        rel = p.relative_to(root).as_posix()
        if rel.startswith(("meta/templates/", "kits/")):
            continue
        text = p.read_text(encoding="utf-8")
        if "template-only:begin" in text:
            new_text = re.sub(r"\n*<!-- template-only:begin -->.*?<!-- template-only:end -->\n*", "\n\n", text, flags=re.S)
            p.write_text(new_text, encoding="utf-8")
            text = new_text
        if "{{" not in text:
            continue
        new = text
        for k, v in values.items():
            new = new.replace("{{" + k + "}}", v)
        if new != text:
            p.write_text(new, encoding="utf-8")


# -- generated content ---------------------------------------------------------
def areas_table(areas: list[dict]) -> str:
    rows = ["| Folder | Holds | Question it answers |", "|---|---|---|"]
    for a in areas:
        rows.append(f"| `{a['path']}/` | {a['holds']} | {a.get('question', '')} |")
    return "\n".join(rows)


def readme(cfg: dict, a: dict, root: Path) -> str:
    p = cfg["project"]
    domain = [x for x in cfg["areas"] if x.get("role") == "domain"]
    ops = [x for x in cfg["areas"] if x.get("role") not in ("domain", "core")]
    core = [x for x in cfg["areas"] if x.get("role") == "core"]
    lines = [f"# {p['name']}: knowledge base", ""]
    if p.get("pitch"):
        lines += [f"> {p['pitch']}", ""]
    lines += [
        f"The **single source of truth** for {p['name']}: what we're building and why, how, what's decided, what's open, "
        f"and how delivery is going. The agent session **`{p['keeper_session']}`** curates it and runs the project's day-to-day "
        f"roles ([playbooks](playbooks/README.md)). **{p['owner']}** decides what becomes `accepted`.",
        "",
        "## Start here", "",
    ]
    start = []
    for x in domain[:2]:
        if (root / x["path"] / "README.md").exists():
            start.append(f"[{x['path']}/]({x['path']}/README.md): {x['holds']}")
    start += ["[Decisions](decisions/README.md): what is settled", "[Open questions](questions/README.md): what isn't"]
    if (root / "planning/roadmap.md").exists():
        start.append("[Roadmap](planning/roadmap.md): what's next")
    start.append("[AGENTS.md](AGENTS.md): how agents work here · [Conventions](meta/conventions.md)")
    lines += [f"{i}. {s}" for i, s in enumerate(start, 1)] + [""]

    # map
    lines += ["## Map", "", "```mermaid", "flowchart TB"]
    ids = {}
    for i, x in enumerate(domain):
        ids[x["path"]] = f"D{i}"
        lines.append(f"    D{i}[{x['path']}/]")
    for i in range(len(domain) - 1):
        lines.append(f"    D{i} --> D{i + 1}")
    lines.append("    IN[(inputs/<br/>owner's words)] -.distilled into.-> " + (" & ".join(ids.values()) if ids else "Q"))
    if ids:
        lines.append(f"    {' & '.join(ids.values())} -.-> Q[questions/]")
    lines.append("    Q -.resolved by.-> ADR[decisions/]")
    if ids:
        lines.append(f"    ADR -.governs.-> {' & '.join(ids.values())}")
    if (root / "planning").exists():
        lines.append("    ADR --> PL[planning/<br/>features · roadmap]")
        if (root / "agents").exists():
            lines.append("    PL --> AG[agents/<br/>goals · sessions]")
            lines.append("    AG -->|REPORT / DONE| QA[qa/]" if (root / "qa").exists() else "")
    lines += ["```", ""]
    lines = [l for l in lines if l != ""] if False else [l for l in lines]

    lines += ["## Areas", "", "| Area | Holds | Index |", "|---|---|---|"]
    for x in domain + ops + core:
        if "/" not in x["path"] and (root / x["path"] / "README.md").exists():
            lines.append(f"| **{x['path']}/** | {x['holds']} | [{x['path']}/README.md]({x['path']}/README.md) |")
    lines.append("")

    enabled = [k for k in ROLE_KEYS if cfg["roles"].get(k)]
    if enabled:
        lines += ["## Roles the agent performs", "", ", ".join(ROLE_LABELS[k].split(" (")[0] for k in enabled) +
                  f". What it may do on its own is set in [authority](meta/authority.md). Default: everything that leaves this repo is drafted for approval.", ""]

    if cfg.get("repos"):
        lines += ["## Repositories", "", "| Repo | Forge | Visibility | Session |", "|---|---|---|---|"]
        for r in cfg["repos"]:
            lines.append(f"| `{r.get('name')}` | {r.get('forge', cfg['forge'])} `{r.get('slug', '')}` | {r.get('visibility', '')} | `{r.get('session', '')}` |")
        lines.append("")

    lines += [
        "## Working here", "",
        "```sh",
        "python3 tools/kb.py check                 # health check (the pre-commit hook runs it)",
        "python3 tools/kb.py new adr \"Use X for Y\"  # next free ID + template + index row",
        "python3 tools/kb.py ops digest            # issues and PRs across registered repos",
        "git config core.hooksPath .githooks       # once per clone",
        "```", "",
        "Conventions: [meta/conventions.md](meta/conventions.md) · Commits: [meta/commit-convention.md](meta/commit-convention.md) · "
        "Agents: [AGENTS.md](AGENTS.md)" + (" · Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)" if (root / "CONTRIBUTING.md").exists() else ""),
        "",
        "---", "",
        f"*Built from [llm-knowledge-base-template]({TEMPLATE_URL}) ([NOTICE](NOTICE.md)).*", "",
    ]
    return "\n".join(lines)


def notice(a: dict) -> str:
    return (
        "# Notice\n\n"
        f"This knowledge base was created from [llm-knowledge-base-template]({TEMPLATE_URL}) by Aurimas Niekis.\n\n"
        "- The template's code (`tools/`, `.githooks/`, CI workflow logic) is licensed under the **MIT License**.\n"
        "- The template's documentation, templates and playbooks are licensed under **CC BY 4.0** "
        "(https://creativecommons.org/licenses/by/4.0/).\n\n"
        "Those parts remain under their licences, and this notice is the required attribution. "
        "Everything the project adds is owned by the project and licensed as stated in `LICENSE` (if present).\n"
    )


def setup_answers_md(a: dict) -> str:
    shown = copy.deepcopy(a)
    shown.get("seed", {}).pop("text", None)
    if shown.get("privacy", {}).get("aliases"):
        shown["privacy"]["aliases"] = sorted(shown["privacy"]["aliases"])  # names only; terms stay in .kb-aliases.env
    return "```json\n" + json.dumps(shown, indent=2, ensure_ascii=False) + "\n```\n\nThe seed text, if any, is IN-0002."


def build_config(old: dict, a: dict, preset: dict, root: Path) -> dict:
    roles = a["roles"]
    cfg = copy.deepcopy(old)
    cfg["initialized"] = True
    cfg["project"] = {k: a["project"][k] for k in ("name", "slug", "pitch", "owner", "keeper_session", "language")}
    cfg["preset"] = preset["name"]
    cfg["mode"] = a["mode"]
    cfg["roles"] = {k: bool(roles[k]) for k in ROLE_KEYS}
    cfg["agents"] = a["agents"]

    areas = []
    for x in preset["areas"]:
        areas.append({"path": x["path"], "holds": x["holds"], "question": x.get("question", ""), "role": "domain"})
    for x in a["areas"]["add"]:
        areas.append({"path": x["path"], "holds": x.get("holds", ""), "question": x.get("question", ""), "role": "domain"})
    if a.get("secrets"):
        areas.append({"path": "secrets", "holds": "Owner-only truths; never published", "question": "What is really true behind the mysteries?", "role": "domain"})
    for path, (holds, q) in OPS_AREAS.items():
        if (root / path).exists():
            areas.append({"path": path, "holds": holds, "question": q, "role": "ops"})
    for path, (holds, q) in CORE_AREAS.items():
        areas.append({"path": path, "holds": holds, "question": q, "role": "core"})
    removed = set(a["areas"]["remove"])
    cfg["areas"] = [x for x in areas if x["path"] not in removed]

    types = dict(UNIVERSAL_TYPES)
    types.update(preset.get("commit_types", {}))
    if roles["product_owner"] or roles["project_manager"]:
        types["plan"] = "Roadmap, milestones, features, releases, status reports"
    if roles["agent_manager"]:
        types["goal"] = "Agent goal briefs and the session board"
    if roles["qa"]:
        types["qa"] = "Test plans, test reports, regression list"
    if roles["support"] or roles["docs_writer"]:
        types["support"] = "FAQ, known issues, replies"
    types["ops"] = "Digests and outbox drafts"
    types["revert"] = "Reverting an earlier commit"
    cfg["commit"]["types"] = types

    ids = cfg["ids"]
    if not roles["product_owner"]:
        ids.pop("FEAT", None)
    if not roles["agent_manager"]:
        ids.pop("GOAL", None)

    cfg["privacy"] = {"enabled": bool(a["privacy"]["enabled"]), "extra_patterns": a["privacy"].get("extra_patterns", []),
                      "scan": a["privacy"].get("scan", []), "aliases_file": ".kb-aliases.env",
                      "aliases_expected": bool(a["privacy"].get("aliases"))}
    cfg["forge"] = a["forge"]
    cfg["repos"] = a["repos"]
    cfg["authority"] = a["authority"]
    t = old.get("template", {})
    version = (root / ".kbtemplate" / "VERSION")
    cfg["template"] = {"upstream": t.get("upstream", TEMPLATE_URL), "slug": t.get("slug", "aurimasniekis/llm-knowledge-base-template"),
                       "forge": t.get("forge", "github"), "version": version.read_text().strip() if version.exists() else "unknown",
                       "synced": _dt.date.today().isoformat()}
    cfg["ops"]["kb_visibility"] = a["kb"]["visibility"]
    cfg["ops"]["kb_url"] = a["kb"]["url"]
    skip = [d for d in cfg["skip_dirs"] if d not in ("examples", "presets")]
    cfg["skip_dirs"] = skip
    return cfg


POLICY_TEXT = {
    "auto": "the keeper commits on its own after each discussion",
    "ask": "the keeper asks before each commit",
    "draft": "the keeper prepares the commit and asks before running it",
    "never": "the keeper never commits; the owner does",
}
PUSH_TEXT = {
    "auto": "the keeper may push",
    "ask": "only when the owner says so, each time",
    "draft": "only when the owner says so, each time",
    "never": "never by the agent",
}


# -- main ----------------------------------------------------------------------
def run(cfg: Config, answers_path: str | None, preset_arg: str | None, example: str | None,
        yes: bool, dry_run: bool) -> int:
    root = cfg.root
    if cfg.initialized:
        print("init: this knowledge base is already initialized (kb.config.json \"initialized\": true).")
        return 1
    if not (root / "presets").is_dir():
        print("init: presets/ is missing; this doesn't look like a fresh template.")
        return 1

    answers: dict = {}
    ex_dir = None
    if example:
        ex_dir = root / "examples" / example
        if not (ex_dir / "answers.json").exists():
            names = sorted(d.name for d in (root / "examples").iterdir() if (d / "answers.json").exists()) if (root / "examples").exists() else []
            raise SystemExit(f"init: unknown example '{example}' (available: {', '.join(names) or 'none'})")
        answers = json.loads((ex_dir / "answers.json").read_text(encoding="utf-8"))
    if answers_path:
        answers = deep_merge(answers, json.loads(Path(answers_path).read_text(encoding="utf-8")))
    if preset_arg:
        answers["preset"] = preset_arg
    if not yes and not answers_path and not example:
        answers = questionnaire(root, answers)
    a = normalize(answers, root)
    preset = json.loads((root / "presets" / a["preset"] / "preset.json").read_text(encoding="utf-8"))
    roles = a["roles"]
    plan = Plan(root, dry_run)
    from . import template as tpl
    sources = {} if dry_run else tpl.snapshot_sources(root, tpl.DEFAULT_MANAGED)

    # 1. preset
    plan.copytree(root / "presets" / a["preset"] / "areas")
    if (root / "presets" / a["preset"] / "templates").exists():
        plan.copytree(root / "presets" / a["preset"] / "templates", "meta/templates")
    if a.get("secrets"):
        plan.copytree(root / "presets" / "_optional" / "secrets", "secrets")
    for x in a["areas"]["add"]:
        if not (root / x["path"] / "README.md").exists():
            plan.write(f"{x['path']}/README.md", f"# {x['path'].split('/')[-1].replace('-', ' ').title()}\n\n{x.get('holds', '')}\n\n| Doc | What it holds | Status |\n|---|---|---|\n")
            parent = (root / x["path"]).parent
            if "/" in x["path"] and (parent / "README.md").exists() and not dry_run:
                name = x["path"].split("/")[-1]
                append_row(parent / "README.md", {"link": f"[{name}/]({name}/README.md)", "title": x.get("holds", ""), "status": "—"})

    # 2. roles, agents, forges, collaboration
    for key in ROLE_KEYS:
        if not roles[key]:
            for rel in ROLE_PATHS[key]:
                plan.rm(rel)
    if not (roles["product_owner"] or roles["project_manager"] or roles["docs_writer"]):
        plan.rm("planning/releases")
        plan.rm("meta/templates/release-notes.md")
    if not (roles["product_owner"] or roles["project_manager"]):
        if not roles["docs_writer"]:
            plan.rm("planning")
    for rel in a["areas"]["remove"]:
        plan.rm(rel)
    if a["forge"] == "none":
        plan.rm("ops")
        plan.rm("playbooks/ops-round.md")
        plan.rm(".claude/skills/kb-ops-round")
    if not roles["agent_manager"] and a["mode"] == "solo":
        plan.rm("agents")
    if "claude" not in a["agents"]:
        plan.rm("CLAUDE.md")
        plan.rm(".claude")
    if "gemini" not in a["agents"]:
        plan.rm("GEMINI.md")

    forge = a["forge"]
    for f, paths in FORGE_FILES.items():
        if f != forge:
            for rel in paths:
                plan.rm(rel)
    col = a["collaboration"]
    if forge != "none" and not col["templates"]:
        for rel in (".github/ISSUE_TEMPLATE", ".github/PULL_REQUEST_TEMPLATE.md", ".github/CODEOWNERS",
                    ".gitlab/issue_templates", ".gitlab/merge_request_templates",
                    ".forgejo/issue_template", ".forgejo/pull_request_template.md"):
            plan.rm(rel)
    if not col["templates"] and a["mode"] != "team":
        plan.rm("CONTRIBUTING.md")
    if forge != "none" and not col["ci_check"]:
        for rel in (".github/workflows/kb-check.yml", ".github/workflows/pr-title.yml", ".forgejo/workflows", "bitbucket-pipelines.yml"):
            plan.rm(rel)
        if forge == "gitlab" and not col["ci_agent"]:
            plan.rm(".gitlab-ci.yml")
    if col["ci_agent"] and forge in ("github", "gitlab", "gitea"):
        if forge == "github":
            plan.write(".github/workflows/ops-round.yml", (root / "ci/agent/github-ops-round.yml").read_text())
        elif forge == "gitea":
            plan.write(".forgejo/workflows/ops-round.yml", (root / "ci/agent/forgejo-ops-round.yml").read_text())
        else:
            ci = root / ".gitlab-ci.yml"
            base = ci.read_text() if ci.exists() else "stages: [check]\n"
            plan.write(".gitlab-ci.yml", base.replace("# include:\n#   - local: ci/agent/gitlab-ops-round.yml",
                                                      "include:\n  - local: ci/agent/gitlab-ops-round.yml"))
    else:
        plan.rm("ci")

    # 3. example overlay
    if ex_dir and (ex_dir / "kb").exists():
        plan.copytree(ex_dir / "kb")

    # 4. template-only files
    for rel in cfg.get("template", {}).get("remove_on_init", []):
        plan.rm(rel)

    if dry_run:
        print("\n".join(plan.log))
        print(f"\ninit (dry run): preset {a['preset']}, roles {[k for k in ROLE_KEYS if roles[k]]}, forge {forge}")
        return 0

    # 5. config, generated docs
    new_cfg = build_config(cfg.data, a, preset, root)
    (root / "kb.config.json").write_text(json.dumps(new_cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    today = _dt.date.today().isoformat()
    domain_types = {k: v for k, v in new_cfg["commit"]["types"].items()
                    if k in preset.get("commit_types", {}) and k not in UNIVERSAL_TYPES}
    dt = ""
    if domain_types:
        dt = "Domain types for this KB:\n\n| Type | Use when… |\n|---|---|\n" + "".join(f"| `{k}` | {v} |\n" for k, v in domain_types.items())
    p = a["project"]
    values = {
        "PROJECT_NAME": p["name"], "PROJECT_SLUG": p["slug"], "PROJECT_PITCH": p["pitch"] or "(pitch to be written)",
        "OWNER": p["owner"], "KEEPER_SESSION": p["keeper_session"], "TODAY": today,
        "KB_COMMIT_POLICY": POLICY_TEXT.get(a["authority"]["kb_commit"], a["authority"]["kb_commit"]),
        "KB_PUSH_POLICY": PUSH_TEXT.get(a["authority"]["kb_push"], a["authority"]["kb_push"]),
        "AREAS_TABLE": areas_table(new_cfg["areas"]),
        "DOMAIN_COMMIT_TYPES": dt.rstrip(),
        "SETUP_ANSWERS": setup_answers_md(a),
    }

    # licence + notice
    lic = a["license"]
    year = today[:4]
    if lic == "own-open":
        for f in ("LICENSE", "LICENSE-docs"):
            fp = root / f
            if fp.exists():
                fp.write_text(fp.read_text().replace("Copyright (c) 2026 Aurimas Niekis", f"Copyright (c) {year} {p['owner']}"), encoding="utf-8")
    elif lic == "proprietary":
        (root / "LICENSE").write_text(f"Copyright (c) {year} {p['owner']}. All rights reserved.\n\n"
                                      "Parts derived from llm-knowledge-base-template are used under MIT / CC BY 4.0; see NOTICE.md.\n", encoding="utf-8")
        plan.rm("LICENSE-docs")
    elif lic == "none":
        plan.rm("LICENSE")
        plan.rm("LICENSE-docs")
    (root / "NOTICE.md").write_text(notice(a), encoding="utf-8")

    # forge config details
    url = a["kb"]["url"].rstrip("/")
    for cfgfile, suffix in ((root / ".github/ISSUE_TEMPLATE/config.yml", "/blob/main/CONTRIBUTING.md"),
                            (root / ".forgejo/issue_template/config.yaml", "/src/branch/main/CONTRIBUTING.md")):
        if cfgfile.exists():
            t = cfgfile.read_text()
            if url:
                t = re.sub(r"url: \S+CONTRIBUTING\.md", f"url: {url}{suffix}", t)
            else:
                t = re.sub(r"contact_links:\n(?:[ -].*\n?)*", "contact_links: []\n", t)
            cfgfile.write_text(t)
    owners = (root / ".github/CODEOWNERS")
    if owners.exists() and col.get("codeowners"):
        handle = col["codeowners"]
        t = owners.read_text()
        for path in ("/decisions/", "/meta/", "/kb.config.json"):
            t = re.sub(rf"^# ({re.escape(path)}\s+)@OWNER", rf"\g<1>{handle}", t, flags=re.M)
        owners.write_text(t)

    render_all(root, values)

    # aliases: local, git-ignored file from the template (+ any aliases given during setup)
    from . import aliases as al
    alias_file = root / ".kb-aliases.env"
    if not alias_file.exists():
        al.write_initial(alias_file, root / "meta/templates/kb-aliases.env", a["privacy"].get("aliases") or {})

    # IN-0002 seed
    seed = a.get("seed") or {}
    if seed.get("text"):
        title = seed.get("title") or "Initial idea dump"
        path = root / "inputs" / f"IN-0002-{slugify(title)}.md"
        if not path.exists():
            path.write_text(f"# IN-0002: {title}\n\n- **Received:** {today}\n- **From:** {p['owner']}\n"
                            f"- **Distilled into:** (to be filled when the keeper distils it)\n\n---\n\n{seed['text'].rstrip()}\n",
                            encoding="utf-8")
            append_row(root / "inputs" / "README.md", {"link": f"[IN-0002]({path.name})", "title": title, "date": today,
                                                       "distilled into": "—"})

    # README last, once the tree is final
    (root / "README.md").write_text(readme(new_cfg, a, root), encoding="utf-8")

    prune_links(root, plan.removed)
    n = tpl.write_baseline(root, sources, a["preset"], values, tpl.DEFAULT_MANAGED)
    print(f"init: recorded template baseline for {n} managed file(s) in .kbtemplate/ (for `kb.py template plan`)")
    stray = root / "ops" / ".state.json"
    if stray.exists():
        stray.unlink()

    # git
    g = a["git"]
    if g.get("init") and not (root / ".git").exists():
        subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=False)
        print("init: git init done (branch main)")
    if g.get("hooks") and (root / ".git").exists():
        subprocess.run(["git", "-C", str(root), "config", "core.hooksPath", ".githooks"], check=False)
        print("init: git hooks enabled (core.hooksPath = .githooks)")

    if answers_path and Path(answers_path).resolve().parent == root.resolve():
        Path(answers_path).unlink()
        print("init: removed answers.json (recorded as IN-0001; aliases are in .kb-aliases.env)")

    from . import check, config
    print(f"\ninit: done. Preset {a['preset']}, roles: {', '.join(k for k in ROLE_KEYS if roles[k]) or 'none'}, forge: {forge}.")
    result = check.run(config.load(root))
    steps = ["Read README.md and AGENTS.md, then open your agent in this folder."]
    if seed.get("text"):
        steps.append("Ask the agent: \"Distil IN-0002 into the KB\" (your seed text).")
    if forge != "none":
        where = " (playbooks/onboarding-a-code-repo.md)" if (root / "playbooks/onboarding-a-code-repo.md").exists() else ""
        steps.append(f"Register code repos in kb.config.json repos[]{where}, then: python3 tools/kb.py ops repos")
    if col["templates"] and forge != "none":
        steps.append("Create the issue labels used by the forms: idea, question, decision, conflict, research, kb-tooling, kb-maintenance, needs-triage")
    steps.append("Confidential names? Put ALIAS=real term lines in .kb-aliases.env (git-ignored) and write only the alias in docs.")
    print("\nNext:")
    for i, st in enumerate(steps, 1):
        print(f"  {i}. {st}")
    print("\nSuggested first commit (init never commits):")
    print("  git add -A && git commit -m \"meta: bootstrap knowledge base from template\"")
    return result
