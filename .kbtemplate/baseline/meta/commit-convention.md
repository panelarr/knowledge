---
title: Knowledge commit convention
status: accepted
tags: [meta, git]
related: [meta/conventions.md, meta/session-protocol.md]
updated: 2026-10-11
---

# Knowledge commit convention

A knowledge-flavoured variant of [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/). The structure is the same, but the types describe **changes to knowledge** rather than to software. This applies to **this KB repo only**. Code repos keep their own convention.

```
<type>[(scope)][!]: <description>

[body: why this changed, which discussion it came from]

[footers]
```

`.githooks/commit-msg` enforces it (enable once per clone with `git config core.hooksPath .githooks`). In team mode, CI applies the same rule to PR/MR titles, because squash merges use the title as the commit header.

## Types

| Type | Use when… | Example |
|---|---|---|
| `idea` | A new idea enters the KB as `seed` | `idea(sync): capture offline-first editing` |
| `decide` | An ADR is added or changes status | `decide: accept ADR-0004 sqlite by default` |
| `question` | Questions added, reframed or answered | `question: answer Q-0007 export formats` |
| `refine` | Clarify, reword, split or merge **without changing meaning** | `refine(architecture): split storage doc` |
| `struct` | Folders, indexes, moves, renames | `struct: add research/competitors` |
| `input` | Owner inputs imported into `inputs/` | `input: import IN-0004 pricing call notes` |
| `meta` | Conventions, templates, tooling, protocols, playbooks | `meta: add release-notes template` |
| `journal` | Journal-only entries | `journal: log 2026-10-12 planning session` |
| `plan` | Roadmap, milestones, features, releases, status reports | `plan(m2): move import to milestone 3` |
| `goal` | Agent goal briefs and the session board | `goal: dispatch GOAL-0003 to the api session` |
| `qa` | Test plans, test reports, regression list | `qa: add test plan for FEAT-0012` |
| `support` | FAQ, known issues, reusable replies | `support: add known issue for safari login` |
| `ops` | Digests and outbox drafts worth keeping | `ops: record triage of week 41` |
| `revert` | Reverting an earlier commit | `revert: undo plan(m2) reorder` |

{{DOMAIN_COMMIT_TYPES}}

The live list is `commit.types` in `kb.config.json`. Add types there, not only here.

**Scope** (optional): lowercase topic, area or repo name (`sync`, `api`, `m2`). Nest with `/`: `design(building/materials)`.

## `!` = change to accepted knowledge

Append `!` when the commit **changes or contradicts something `accepted`**, and explain why in an `ACCEPTED-CHANGE:` footer:

```
arch(storage)!: store attachments outside the database

ACCEPTED-CHANGE: replaces in-database blobs from ADR-0006 at the owner's request.
Refs: ADR-0006, Q-0019
```

## Footers

| Footer | Meaning |
|---|---|
| `Refs: ADR-0004, Q-0012` | Related decisions or questions |
| `Input: IN-0002` | Owner input this distils |
| `Supersedes: ADR-0002` | Replaces a decision |
| `Session: <name>` | The change came from a coding session's REPORT/PROPOSE |
| `Implements: api@abc1234, web#12` | Code commits or PRs that implement this. Traceability runs KB → code |
| `ACCEPTED-CHANGE: …` | Required with `!` |

## Granularity

- **One commit per discussion** by default. Pick the dominant type and list the other touched areas in the body.
- Split commits when a discussion produced clearly separable changes (e.g. a `decide` plus an unrelated `research`).
- Indexes and the journal entry go in the same commit as the change. `kb.py check` blocks the commit otherwise.
- Whether the keeper may commit or push on its own is set in [authority](authority.md) (`kb_commit`, `kb_push`).
