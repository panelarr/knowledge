---
title: "GOAL-0008: meta jobs page"
status: accepted
tags: [goal, agents, meta, admin, jobs]
related: [planning/features/FEAT-0002-jobs-page-in-every-admin.md, modules/meta/overview.md, decisions/ADR-0027-observability-baseline-for-every-service.md]
inputs: [IN-0032, IN-0033]
repos: [meta]
session: "panelarr-meta"
features: [FEAT-0002]
updated: 2026-10-11
---

# GOAL-0008: meta jobs page

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0008 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`accepted`: dispatched to `panelarr-meta` on 2026-10-11 (owner's go, IN-0033). **Runs before GOAL-0004**, so the duplicate finder registers as a job (keeper's ordering; the owner can swap it back).

## Context

- Code: `~/Projects/Panelarr/meta` · branches `<type>/<scope>-<slug>` · the same rules as its earlier goals (merge your own branches before the first release after `make check` passes, never push, leak-check, aliases).
- **Read first:** [FEAT-0002](../../planning/features/FEAT-0002-jobs-page-in-every-admin.md). Its acceptance criteria are the DoD. Also [ADR-0027](../../decisions/ADR-0027-observability-baseline-for-every-service.md) (metrics).
- **Match the other admin:** both services get identical job/run messages and the same Jobs page UX. Build against the draft shared contract [contracts/jobs.md](../../contracts/jobs.md); REPORT any change you make to it so the other admin copies it.

## Objective

A Jobs page in the meta admin listing background jobs with schedule, last result and next run, a run history with details, **Run now** and cancel where supported (IN-0032).

## Jobs to register

provider sync (one job per provider and ingestion kind, parameters `force`), entry rebuild (maintenance), stale-entry refresh; GOAL-0004's duplicate finder and GOAL-0006's search rebuild register as jobs when they land.

## Storage

Postgres (`job_runs`), folding in or mapping the existing `sync_runs` while keeping the sync API working.

## Definition of Done

- [ ] FEAT-0002 AC1–AC7 met for meta, with test evidence
- [ ] Same job/run API shape as the other admin (or agreed via the keeper)
- [ ] Docs updated; `make check` green; leak-check clean
- [ ] `DONE:` with evidence per AC

## History

- 2026-10-11: brief written from IN-0032 (`proposed`).
- 2026-10-11: owner's go (IN-0033): `accepted`, dispatched.
