---
title: "GOAL-0004: meta duplicates: find similar entries, optional model review"
status: proposed
tags: [goal, agents, meta, matching, duplicates]
related: [modules/meta/overview.md, contracts/metadata-schema.md, agents/goals/GOAL-0003-meta-admin-clients-integrations-and-admin-ui.md, architecture/search.md]
inputs: [IN-0022]
repos: [meta]
session: "panelarr-meta"
features: []
updated: 2026-10-11
---

# GOAL-0004: meta duplicates: find similar entries, optional model review

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0004 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`proposed`: written from IN-0022 for the owner to review. Suggested to start after GOAL-0003, since its review list lives in GOAL-0003's admin UI.

## Context

- Code: `~/Projects/Panelarr/meta` · branches `<type>/<scope>-<slug>`
- **Read first:** [modules/meta/overview.md](../../modules/meta/overview.md) ("Duplicates" and "Matcher (later)") and [contracts/metadata-schema.md](../../contracts/metadata-schema.md). The linking rules are working assumptions: same-provider records are never joined, and name-only persons are shared by name. Also read meta's `internal/catalog` and `internal/textnorm`.
- Real scale: about 306k active entries, plus about 258k merged MangaBaka rows ([research](../../research/mangabaka.md)).

## Objective

Find entries in meta that are **probably the same work** but aren't linked, and give the user a list to review (IN-0022). It runs in two stages:

1. **Candidates (always):** meta's own comparison finds the most similar pairs.
2. **Model review (optional, configurable):** the top candidates go to a model API, which judges "same work or not", with a confidence and a short reason.

The hoster chooses whether stage 1 alone is enough ("just first is enough for user to compare") or whether stage 2 runs too.

## Design sketch (for the session to refine)

- **Candidate generation:** block by normalized title keys (all languages and romanizations) and trigram similarity on titles; score with title similarity, author/artist overlap (normalized names), year proximity, type, original language, and shared or conflicting external IDs. A conflicting ID from the same provider is a strong "different". Skip pairs a provider already says are distinct (same-provider rule) and pairs already dismissed. Keep it set-based in Postgres; it must handle about 300k entries incrementally (new or changed entries since the last run), not all pairs.
- **Model judge (optional):** an adapter for a model API configured by base URL, model name and key ([Q-0035](../../questions/README.md); suggestion: OpenAI-compatible chat completions with structured JSON output). Send only the fields needed (titles, people, year, type, short description). Cap batch size, rate and cost per run; cache verdicts by the pair's content hash, so unchanged pairs aren't re-asked. Off by default; enabled per hoster, who accepts sending data to that provider ([Q-0036](../../questions/README.md)).
- **Review list:** stored candidates with scores, signals, the model verdict if any, and status (open, confirmed, dismissed). API in `MetaAdminService` (list, get, confirm, dismiss, run now) and a page in the GOAL-0003 admin UI showing both entries side by side. **Confirm** links them: a manual link that merges into one entry, with redirects, reusing meta's merge path. **Dismiss** records "distinct" so the pair never comes back. Nothing is merged without a human.
- **Jobs:** a scheduled, configurable job (cron, thresholds, model on or off, max pairs per run), visible in sync-run-style history.
- **Reuse:** the same candidate scoring is what later matches source series (from server) to entries ("Matcher (later)").

## When something isn't decided

- `ASK:` the keeper; then `PROPOSE:` a working assumption, built cheap to change.
- Open: [Q-0035](../../questions/README.md) (which model APIs), [Q-0036](../../questions/README.md) (sending provider data to a model).

## Constraints

- As in GOAL-0003: merge your own branches before the first release, never push; public repo; aliases; leak-check.
- **Opt-in:** without a model configured, everything works on stage 1 alone. No model call ever happens unless the hoster turned it on.
- Keys for model APIs are secrets: encrypted at rest, never returned.
- No real catalogue data in tests; synthetic near-duplicates only.

## Definition of Done

- [ ] Incremental candidate generation with scores and signals; scale test on synthetic data at about 300k entries
- [ ] Optional model judge behind one adapter interface; batching, rate and cost caps, verdict cache; fully off by default
- [ ] Review list API (list, confirm, dismiss, run now); confirm merges through meta's merge path with redirects; dismiss is remembered
- [ ] Admin UI page (side by side, signals, model reason) in the GOAL-0003 admin
- [ ] Configurable schedule and thresholds; docs; `make check` green; leak-check clean
- [ ] `DONE:` with evidence per box

## History

- 2026-10-11: brief written from IN-0022 (`proposed`).
