---
title: "GOAL-0020: source plugins: jobs, package origins and details"
status: accepted
tags: [goal, agents, source-api, source-mihon, mihon-source]
related: [planning/features/FEAT-0013-connected-services-admin-inside-panelarr.md, contracts/jobs.md, contracts/source-plugin.md]
inputs: [IN-0039, IN-0063, IN-0064, IN-0065]
repos: [source-api, source-mihon, mihon-source]
session: "panelarr-mihon-source"
features: [FEAT-0013]
updated: 2026-10-12
---

# GOAL-0020: source plugins: jobs, package origins and details

The brief a coding session works from. Read this file and follow it.

## Status

`accepted` (2026-10-12): the owner accepted [FEAT-0013](../../planning/features/FEAT-0013-connected-services-admin-inside-panelarr.md) (IN-0064). Design by `panelarr-server`, accepted by the keeper (see GOAL-0019's history).

## Context

- Read [FEAT-0013](../../planning/features/FEAT-0013-connected-services-admin-inside-panelarr.md), [contracts/jobs.md](../../contracts/jobs.md), [contracts/source-plugin.md](../../contracts/source-plugin.md).
- **Decided:** everything in mihon-source's and meta's admin (apart from their API clients and keys) is usable from Panelarr's admin; mihon-source is reached **generically through source-mihon and source.v1** (capabilities, like packages), not with a mihon-source admin key; meta is proxied by the server with its admin key; one Jobs view for the server, plugins and meta; network resources stay Panelarr's, with custom solvers, proxies and profiles per plugin kept in Panelarr's store (IN-0065).
- Same working rules as before: slices, gated checks, merge to local main, never push, `REPORT:` per slice; every merge is redeployed for the owner (IN-0056).

## Objective

1. **Jobs capability** in source.v1 (`PLUGIN_CAPABILITY_JOBS`): ListJobs, GetJob, ListJobRuns, GetJobRun, RunJob, CancelJobRun with contracts/jobs.md's messages; ideally a shared `panelarr.jobs.v1` package that meta can adopt later (propose where it lives). SDK, fake, conformance.
2. **source-mihon** serves mihon-source's jobs (store refresh, health checks with `source_ids` and `steps` params) plus its own.
3. **Packages capability additions**: ListOrigins (id, name, url, last refresh, error, package count, pinned fingerprint) and RefreshOrigin; optional `details` on Package (signing fingerprint, lib version, load error); ReloadPackage (or explain why Update covers it).
4. Health-check schedule in source-mihon's config schema; per-source on/off for checks as a per-source setting (or propose better).
5. List anything in mihon-source's admin the server's design missed.

## Definition of Done

- [ ] Jobs capability in source.v1 with SDK, fake and conformance
- [ ] source-mihon serves mihon-source's jobs
- [ ] Origins, package details and reload
- [ ] Health-check settings reachable through source.v1
- [ ] Docs; checks green; leak-check clean
- [ ] `DONE:` with evidence per box

## History

- 2026-10-12: brief written from the accepted server design.
