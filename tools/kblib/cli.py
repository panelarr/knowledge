"""Argument parsing for tools/kb.py."""
from __future__ import annotations

import argparse
import sys

from . import config


def build() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="kb.py", description="Knowledge base tooling: check, scaffold, set up, operate.")
    ap.add_argument("--root", help="KB root (default: the folder above tools/)")
    sub = ap.add_subparsers(dest="cmd", metavar="command")

    sub.add_parser("check", help="health check: frontmatter, links, indexes, IDs, placeholders")

    n = sub.add_parser("new", help="create a doc from a template with the next free ID")
    n.add_argument("kind", choices=["adr", "question", "input", "feature", "goal", "journal", "doc"])
    n.add_argument("title")
    n.add_argument("--area", help="folder for `doc` (e.g. product), or the area column for questions")
    n.add_argument("--status", help="initial status (default depends on kind)")
    n.add_argument("--pri", help="question priority P1/P2/P3")
    n.add_argument("--template", help="template file in meta/templates/ for `doc` (default concept.md)")
    n.add_argument("--file", action="store_true", help="for `question`: also create questions/Q-NNNN-slug.md")

    c = sub.add_parser("commit-msg", help="validate a commit message (used by .githooks/commit-msg)")
    c.add_argument("file", nargs="?")
    c.add_argument("--title", help="validate a PR/MR title instead of a message file")

    lk = sub.add_parser("leak-check", help="privacy mode: scan public repos for KB references")
    lk.add_argument("repos", nargs="*")

    al = sub.add_parser("aliases", help="list alias names from .kb-aliases.env (values hidden)")
    al.add_argument("--show", action="store_true", help="also print the real terms (local terminal only)")

    i = sub.add_parser("init", help="turn this template into your knowledge base")
    i.add_argument("--answers", help="answers JSON (written by an agent following SETUP.md)")
    i.add_argument("--preset", help="software | platform | game | research | minimal")
    i.add_argument("--from-example", dest="example", help="start from examples/<name>")
    i.add_argument("--yes", action="store_true", help="accept defaults for anything not answered")
    i.add_argument("--dry-run", action="store_true", help="show what would change")

    t = sub.add_parser("template", help="sync with the upstream template (see playbooks/template-sync.md)")
    tsub = t.add_subparsers(dest="top", metavar="op")
    tsub.add_parser("status", help="upstream, version, last sync")
    tp = tsub.add_parser("plan", help="fetch upstream and classify changes")
    tp.add_argument("--source", help="upstream git URL or a local template checkout")
    tp.add_argument("--ref", help="branch or tag to fetch")
    tp.add_argument("--no-fetch", action="store_true", help="reuse .kbtemplate/upstream")
    ta = tsub.add_parser("apply", help="apply upstream changes to files (3-way merge when you changed them too)")
    ta.add_argument("paths", nargs="+")
    ta.add_argument("--new", action="store_true", help="install new upstream files")
    tr = tsub.add_parser("resolve", help="mark files resolved after fixing merge conflicts")
    tr.add_argument("paths", nargs="+")
    td = tsub.add_parser("diff", help="what upstream changed in a file since your baseline")
    td.add_argument("path")
    tsub.add_parser("finish", help="adopt the upstream version after the sync")

    o = sub.add_parser("ops", help="forge + worktree operations (digest, PR/issue context, outbox)")
    osub = o.add_subparsers(dest="op", metavar="op")
    osub.add_parser("repos", help="registered repos and whether their forge is reachable")
    d = osub.add_parser("digest", help="open issues/PRs across repos -> ops/digests/")
    d.add_argument("--since", help="last | 24h | 7d | 2w | ISO date (default: show all open, flag new since last)")
    d.add_argument("--repo")
    d.add_argument("--stdout", action="store_true")
    p = osub.add_parser("pr", help="context bundle for reviewing a PR/MR")
    p.add_argument("repo")
    p.add_argument("number", type=int)
    p.add_argument("--diff", action="store_true")
    p.add_argument("--out")
    s = osub.add_parser("issue", help="context bundle for triaging an issue")
    s.add_argument("repo")
    s.add_argument("number", type=int)
    s.add_argument("--out")
    dr = osub.add_parser("draft", help="create an outbox draft (comment, review, label, ...)")
    dr.add_argument("action", choices=["comment", "review", "label", "assign", "open_issue", "close", "merge"])
    dr.add_argument("repo")
    dr.add_argument("number", type=int, nargs="?")
    dr.add_argument("--kind", choices=["pr", "issue"])
    dr.add_argument("--event", choices=["comment", "approve", "request_changes"])
    dr.add_argument("--labels", help="comma-separated labels (or users for assign)")
    dr.add_argument("--title")
    osub.add_parser("outbox", help="list outbox drafts")
    ap_ = osub.add_parser("approve", help="mark a draft approved (only on the operator's word)")
    ap_.add_argument("file")
    po = osub.add_parser("post", help="post an approved draft")
    po.add_argument("file")
    po.add_argument("--dry-run", action="store_true")
    se = osub.add_parser("sessions", help="refresh the worktree table in agents/sessions.md")
    se.add_argument("--stdout", action="store_true")
    return ap


def main(argv: list[str] | None = None) -> int:
    ap = build()
    args = ap.parse_args(argv)
    if not args.cmd:
        ap.print_help()
        return 0
    try:
        cfg = config.load(args.root)
    except config.ConfigError as e:
        print(f"kb.py: {e}", file=sys.stderr)
        return 2

    if args.cmd == "check":
        from . import check
        return check.run(cfg)
    if args.cmd == "new":
        from . import new
        return new.run(cfg, args.kind, args.title, args.area, args.status, args.pri, args.template, args.file)
    if args.cmd == "commit-msg":
        from . import commitmsg
        return commitmsg.run(cfg, args.file, args.title)
    if args.cmd == "leak-check":
        from . import leak
        return leak.run(cfg, args.repos)
    if args.cmd == "aliases":
        from . import aliases
        return aliases.cmd_list(cfg, args.show)
    if args.cmd == "init":
        from . import init
        return init.run(cfg, args.answers, args.preset, args.example, args.yes, args.dry_run)
    if args.cmd == "template":
        from . import template as tpl
        if args.top == "status":
            return tpl.cmd_status(cfg)
        if args.top == "plan":
            return tpl.cmd_plan(cfg, args.source, args.ref, args.no_fetch)
        if args.top == "apply":
            return tpl.cmd_apply(cfg, args.paths, args.new)
        if args.top == "resolve":
            return tpl.cmd_resolve(cfg, args.paths)
        if args.top == "diff":
            return tpl.cmd_diff(cfg, args.path)
        if args.top == "finish":
            return tpl.cmd_finish(cfg)
        ap.parse_args(["template", "--help"])
    if args.cmd == "ops":
        from . import ops
        from .forges import ForgeError
        try:
            if args.op == "repos":
                return ops.cmd_repos(cfg)
            if args.op == "digest":
                return ops.cmd_digest(cfg, args.since, args.repo, args.stdout)
            if args.op == "pr":
                return ops.cmd_pr(cfg, args.repo, args.number, args.diff, args.out)
            if args.op == "issue":
                return ops.cmd_issue(cfg, args.repo, args.number, args.out)
            if args.op == "draft":
                return ops.cmd_draft(cfg, args.action, args.repo, args.number, args.kind, args.event, args.labels, args.title)
            if args.op == "outbox":
                return ops.cmd_outbox(cfg)
            if args.op == "approve":
                return ops.cmd_approve(cfg, args.file)
            if args.op == "post":
                return ops.cmd_post(cfg, args.file, args.dry_run)
            if args.op == "sessions":
                return ops.cmd_sessions(cfg, args.stdout)
        except (ForgeError, config.ConfigError) as e:
            print(f"kb.py ops: {e}", file=sys.stderr)
            return 1
        ap.parse_args(["ops", "--help"])
    return 0
