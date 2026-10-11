---
title: "GOAL-0007: mihon-source jobs page"
status: accepted
tags: [goal, agents, mihon-source, admin, jobs]
related: [planning/features/FEAT-0002-jobs-page-in-every-admin.md, modules/mihon-source/overview.md, decisions/ADR-0027-observability-baseline-for-every-service.md]
inputs: [IN-0032, IN-0033]
repos: [mihon-source]
session: "panelarr-mihon-source"
features: [FEAT-0002]
updated: 2026-10-11
---

# GOAL-0007: mihon-source jobs page

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0007 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`accepted`, **Done 2026-10-11** (verified; [test report](../../qa/reports/goal-0007-mihon-source-jobs-done-verification.md)). Dispatched on 2026-10-11 (owner's go, IN-0033).

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

- [x] FEAT-0002 AC1–AC7 met for mihon-source, with test evidence
- [x] Same job/run API shape as the other admin (or agreed via the keeper)
- [x] Docs updated; `make check` green; leak-check clean
- [x] `DONE:` with evidence per AC

## History

- 2026-10-11: brief written from IN-0032 (`proposed`).
- 2026-10-11: owner's go (IN-0033): `accepted`, dispatched.
- 2026-10-11: **DONE received and verified** (`898723f`: 152 JUnit + 81 Vitest). Jobs `store-refresh` and `source-health`, history in `data/jobs/` (last 100). Additive extras: `JobParam.choices`, an ErrorInfo on 409. Behaviour change: scheduled health checks run as rounds per interval.
- 2026-10-11: **Follow-up (owner, IN-0036):** the health check should cover random or selected languages, not every source. `MIHON_HEALTH_CHECK_LANGS` (comma list; unset = all languages); `MIHON_HEALTH_CHECK_SAMPLE` (random N per round, rotating so every source is eventually covered; **suggested default 10**; `all` = every source); combined = N random from those languages. The same as Run-now params (langs, sample, source_ids). Off by default and per-source opt-out unchanged. Defaults are suggestions; the owner can adjust.
- 2026-10-11: REPORT: **health-check selection merged** (`17eb971`; 158 JUnit + 81 Vitest). `MIHON_HEALTH_CHECK_LANGS` and `MIHON_HEALTH_CHECK_SAMPLE` (default 10, or `all`); least-recently-checked first so rounds rotate; Run-now params `source_ids`, `langs`, `sample`, `steps` default to the configured selection; explicit source_ids override. Message e.g. "9 of 10 sources OK (10 of 57 eligible)".
- 2026-10-11: **Flaky scheduler test fixed** at the cause (`323691d`: two races in JobRunner). The keeper re-ran it 12/12 green on a clean clone. Added to the regression list.
