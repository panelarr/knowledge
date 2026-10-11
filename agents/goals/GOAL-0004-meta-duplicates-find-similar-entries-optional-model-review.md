---
title: "GOAL-0004: meta duplicates: find similar entries, optional model review"
status: accepted
tags: [goal, agents, meta, matching, duplicates]
related: [research/decision-models.md, modules/meta/overview.md, contracts/metadata-schema.md, agents/goals/GOAL-0003-meta-admin-clients-integrations-and-admin-ui.md, architecture/search.md]
inputs: [IN-0022, IN-0023, IN-0024]
repos: [meta]
session: "panelarr-meta"
features: []
updated: 2026-10-11
---

# GOAL-0004: meta duplicates: find similar entries, optional model review

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0004 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`accepted` (owner's go, IN-0024 §2). Queued for `panelarr-meta` to start **after GOAL-0003 is done**, since its review list lives in GOAL-0003's admin UI.

## Context

- Code: `~/Projects/Panelarr/meta` · branches `<type>/<scope>-<slug>`
- **Read first:** [modules/meta/overview.md](../../modules/meta/overview.md) ("Duplicates" and "Matcher (later)") and [contracts/metadata-schema.md](../../contracts/metadata-schema.md). The linking rules are working assumptions: same-provider records are never joined, and name-only persons are shared by name. Also read meta's `internal/catalog` and `internal/textnorm`.
- Real scale: about 306k active entries, plus about 258k merged MangaBaka rows ([research](../../research/mangabaka.md)).

## Objective

Find entries in meta that are **probably the same work** but aren't linked, and give the user a list to review (IN-0022). It runs in two stages:

1. **Candidates (always):** meta's own comparison finds the most similar pairs.
2. **Model review (optional, configurable):** the top candidates go to a **decision model** API, which returns the probability that they are the same work (and whether they are only related), with a confidence.

The hoster chooses whether stage 1 alone is enough ("just first is enough for user to compare") or whether stage 2 runs too.

## Design sketch (for the session to refine)

- **Candidate generation:** block by normalized title keys (all languages and romanizations) and trigram similarity on titles; score with title similarity, author/artist overlap (normalized names), year proximity, type, original language, and shared or conflicting external IDs. A conflicting ID from the same provider is a strong "different". Skip pairs a provider already says are distinct (same-provider rule) and pairs already dismissed. Keep it set-based in Postgres; it must handle about 300k entries incrementally (new or changed entries since the last run), not all pairs.
- **Model judge (optional):** a `DecisionJudge` interface with two adapters ([decision models](../../research/decision-models.md), Q-0035): **OpenAI Decisions** (`POST /v1/decisions`, `gpt-6-luna`; `input` + `questions[]`, `predicate`), and a **state + questions-map** adapter for **TypeSafe** (`/v1/systemone`, `jev-latest`) and **Cloudflare Workers AI Clef** (`@cf/cloudflare/clef`; `state` + `questions{}`, `noul`/`choice`/`score`). Each is configured by base URL, model and key. Ask a yes/no "same work?" plus a `choice` of same work / related work (sequel, spin-off, adaptation, edition) / different. The state is a compact JSON of both entries; covers go in as images where supported (OpenAI, Clef). Store probabilities and confidence. These models give **no written reason**. Cap tokens per run, back off on 429/529, cache verdicts by the pair's content hash. Off by default; sending provider data is fine for the owner's personal, non-commercial use (Q-0036).
- **Review list:** stored candidates with scores, signals, the model's probabilities if any, and status (open, confirmed, dismissed). API in `MetaAdminService` (list, get, confirm, dismiss, run now) and a page in the GOAL-0003 admin UI showing both entries side by side. **Confirm** links them: a manual link that merges into one entry, with redirects, reusing meta's merge path. **Dismiss** records "distinct" so the pair never comes back. Nothing is merged without a human.
- **Jobs:** a scheduled, configurable job (cron, thresholds, model on or off, max pairs per run), visible in sync-run-style history.
- **Reuse:** the same candidate scoring is what later matches source series (from server) to entries ("Matcher (later)").

## When something isn't decided

- `ASK:` the keeper; then `PROPOSE:` a working assumption, built cheap to change.
- Answered: Q-0035 (the three decision-model APIs), Q-0036 (sending data is fine for personal, non-commercial use).

## Constraints

- As in GOAL-0003: merge your own branches before the first release, never push; public repo; aliases; leak-check.
- **Opt-in:** without a model configured, everything works on stage 1 alone. No model call ever happens unless the hoster turned it on.
- Keys for model APIs are secrets: encrypted at rest, never returned.
- No real catalogue data in tests; synthetic near-duplicates only.

## Definition of Done

- [ ] Incremental candidate generation with scores and signals; scale test on synthetic data at about 300k entries
- [ ] Optional decision-model judge: one interface, OpenAI Decisions adapter plus state/questions adapter (TypeSafe, Clef), tested against mock servers; token caps, back-off, verdict cache; fully off by default
- [ ] Review list API (list, confirm, dismiss, run now); confirm merges through meta's merge path with redirects; dismiss is remembered
- [ ] Admin UI page (side by side, signals, model probabilities) in the GOAL-0003 admin
- [ ] Configurable schedule and thresholds; docs; `make check` green; leak-check clean
- [ ] `DONE:` with evidence per box

## History

- 2026-10-11: brief written from IN-0022 (`proposed`).
- 2026-10-11: model judge specified against the three decision-model APIs the owner linked; Q-0035 and Q-0036 answered (IN-0023).
- 2026-10-11: owner's go (IN-0024 §2): `accepted`, queued after GOAL-0003.
