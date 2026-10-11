---
title: "GOAL-0007: mihon-source jobs page"
status: proposed
tags: [goal, agents, mihon-source, admin, jobs]
related: [planning/features/FEAT-0002-jobs-page-in-every-admin.md, modules/mihon-source/overview.md, decisions/ADR-0027-observability-baseline-for-every-service.md]
inputs: [IN-0032]
repos: [mihon-source]
session: "panelarr-mihon-source"
features: [FEAT-0002]
updated: 2026-10-11
---

# GOAL-0007: mihon-source jobs page

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0007 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`proposed`: written from IN-0032 for the owner to review. Can start right away (the session is idle).

## Context

- Code: `~/Projects/Panelarr/mihon-source` · branches `<type>/<scope>-<slug>` · the same rules as its earlier goals (merge your own branches before the first release after `make check` passes, never push, leak-check, aliases).
- **Read first:** [FEAT-0002](../../planning/features/FEAT-0002-jobs-page-in-every-admin.md). Its acceptance criteria are the DoD. Also [ADR-0027](../../decisions/ADR-0027-observability-baseline-for-every-service.md) (metrics).
- **Match the other admin:** both services get identical job/run messages and the same Jobs page UX. Build against the draft shared contract [contracts/jobs.md](../../contracts/jobs.md); REPORT any change you make to it so the other admin copies it.

## Objective

A Jobs page in the mihon-source admin listing background jobs with schedule, last result and next run, a run history with details, **Run now** and cancel where supported (IN-0032).

## Jobs to register

store refresh (all stores; optional single store), source health self-check round (optional source list and steps); keep the compatibility checker a CLI (it can show as a manual-only job if cheap).

## Storage

files under `/data` with retention (e.g. last 100 runs per job).

## Definition of Done

- [ ] FEAT-0002 AC1–AC7 met for mihon-source, with test evidence
- [ ] Same job/run API shape as the other admin (or agreed via the keeper)
- [ ] Docs updated; `make check` green; leak-check clean
- [ ] `DONE:` with evidence per AC

## History

- 2026-10-11: brief written from IN-0032 (`proposed`).
