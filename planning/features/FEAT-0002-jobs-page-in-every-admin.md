---
title: "FEAT-0002: Jobs page in every admin"
status: proposed
tags: [feature, admin, jobs, ops]
related: [decisions/ADR-0027-observability-baseline-for-every-service.md, modules/meta/overview.md, modules/mihon-source/overview.md]
inputs: [IN-0032]
milestone: ""
priority: P2
updated: 2026-10-11
---

# FEAT-0002: Jobs page in every admin

## Problem

"as both meta/mihou-sources have jobs it would be great to show in admin as list past runs statusses and maybe even manual trigger" (IN-0032). Both services run background work:
- **meta:** provider syncs, the entry rebuild after migrations, stale-entry refresh; next, duplicates (GOAL-0004) and search rebuilds (GOAL-0006).
- **mihon-source:** store refresh and the per-source health self-check.

Only meta's syncs have a visible history today.

## Outcome

Each admin has a **Jobs** page. It lists every background job with its schedule, last result and next run. It shows the past runs with status, duration, counts and errors, and has a **Run now** button. The page looks and behaves the same in every Panelarr admin.

## Scope

- **In:**
  - a common job and run model and API (same shapes in every service);
  - run history with retention;
  - manual trigger (with "already running" handling) and cancel where the job supports it;
  - metrics per job (ADR-0027);
  - the Jobs page in each admin.
- **Out:**
  - editing schedules in the UI (schedules stay in config; the page shows them; a later feature);
  - jobs in the future server (it follows the same model when it exists);
  - a cross-service jobs dashboard.

## Acceptance criteria

- [ ] **AC1, list:** `ListJobs` returns every background job with id, name, description, schedule (cron/interval or "manual only", enabled), whether it is running, the last run summary and the next run time.
- [ ] **AC2, history:** `ListJobRuns(job, page)` and `GetJobRun(id)` return runs with trigger (`schedule`, `manual`, `startup`), start and finish, status (`running`, `succeeded`, `failed`, `cancelled`, `skipped`), counts/summary, error message, and bounded log or notice lines. History is kept with a bounded retention (suggestion: last 100 runs per job, configurable).
- [ ] **AC3, run now:** `RunJob(job, options)` starts a run and returns its id at once; if the job is already running it answers "already running" (HTTP 409 / `ALREADY_EXISTS`) with the current run ID. Jobs that take parameters accept them (e.g. a provider, `force`).
- [ ] **AC4, cancel:** `CancelJobRun(id)` stops a running run where the job supports it; others report "not cancellable".
- [ ] **AC5, admin page:** the Jobs page lists jobs (status badge, last run, next run, Run now) and opens a run's details; it polls while a run is active; it uses the shared look of both admins.
- [ ] **AC6, safety:** only the `admin` scope can list, run or cancel; manual runs respect the job's own limits (rate limits, a single run at a time); runs survive a service restart as history, and runs interrupted by a restart are marked `failed` (interrupted).
- [ ] **AC7, metrics:** `<service>_job_runs_total{job,status,trigger}` and `<service>_job_duration_seconds{job}` with bounded labels; a "running" gauge per job.

## Design notes

- **Same API shape in both services:** the draft contract is [contracts/jobs.md](../../contracts/jobs.md) (`MihonJobsService` / `MetaJobsService` with identical messages and REST paths), so a shared `panelarr.jobs.v1` can be extracted later.
- **meta:** fold the existing `sync_runs` into the job model, a sync being one job per provider and ingestion kind, or map it onto it. Keep the existing sync API working.
- **mihon-source:** store history in files under `/data` with retention, like its other state.
- Logs per run: keep the notices and warnings the job emits (bounded), not full logs.

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| mihon-source | [GOAL-0007](../../agents/goals/GOAL-0007-mihon-source-jobs-page.md) | — | proposed |
| meta | [GOAL-0008](../../agents/goals/GOAL-0008-meta-jobs-page.md) | — | proposed |

## Open questions

- Editing schedules in the admin (later?).
