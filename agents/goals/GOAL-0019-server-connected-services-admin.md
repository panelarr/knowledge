---
title: "GOAL-0019: server: connected services' admin"
status: accepted
tags: [goal, agents, server]
related: [planning/features/FEAT-0013-connected-services-admin-inside-panelarr.md, contracts/jobs.md, contracts/source-plugin.md]
inputs: [IN-0039, IN-0063, IN-0064, IN-0065]
repos: [server]
session: "panelarr-server"
features: [FEAT-0013]
updated: 2026-10-12
---

# GOAL-0019: server: connected services' admin

The brief a coding session works from. Read this file and follow it.

## Status

`accepted` (2026-10-12): the owner accepted [FEAT-0013](../../planning/features/FEAT-0013-connected-services-admin-inside-panelarr.md) (IN-0064). Design by `panelarr-server`, accepted by the keeper (see GOAL-0019's history).

## Context

- Read [FEAT-0013](../../planning/features/FEAT-0013-connected-services-admin-inside-panelarr.md), [contracts/jobs.md](../../contracts/jobs.md), [contracts/source-plugin.md](../../contracts/source-plugin.md).
- **Decided:** everything in mihon-source's and meta's admin (apart from their API clients and keys) is usable from Panelarr's admin; mihon-source is reached **generically through source-mihon and source.v1** (capabilities, like packages), not with a mihon-source admin key; meta is proxied by the server with its admin key; one Jobs view for the server, plugins and meta; network resources stay Panelarr's, with custom solvers, proxies and profiles per plugin kept in Panelarr's store (IN-0065).
- Same working rules as before: slices, gated checks, merge to local main, never push, `REPORT:` per slice; every merge is redeployed for the owner (IN-0056).

## Objective

- **S1 meta admin** proxied under `/system/meta/...` (admin only): providers and sync runs, refresh entry, jobs, duplicates (list, get, confirm, dismiss, reopen) and the decision judge, search engine settings (key write-only).
- **S2 custom solvers and proxies** (IN-0065): the same owner model as custom profiles.
- **S3 one Jobs view**: `/plugins/{id}/jobs…` and `/system/meta/jobs…` in the server's own jobs shape, for plugins declaring the jobs capability (GOAL-0020) and for meta.
- **S4 package origins and details**: stores' status and refresh, package details and reload (GOAL-0020).

## Definition of Done

- [ ] Meta admin proxied, admin only, tests
- [ ] Custom solvers and proxies per plugin
- [ ] Jobs view for plugins and meta
- [ ] Package origins, details and reload
- [ ] Docs; checks green; leak-check clean
- [ ] `DONE:` with evidence per box

## History

- 2026-10-12: brief written from the accepted server design.
- 2026-10-12: design PROPOSEd by `panelarr-server` and accepted: mihon-source reached generically through source-mihon (jobs capability, package origins and details), no mihon-source admin key in Panelarr (no hard-coded mihon API, no second URL and key, one writer for stores); meta proxied with its admin key; one Jobs view in the server's jobs shape for server, plugins and meta (polled); custom solvers and proxies in Panelarr's store with the profile owner model (one source of truth, one push path, works for every plugin, secrets stay sealed). Slices S1 meta, S2 custom solvers and proxies (start now), S3 jobs view, S4 origins and details (after GOAL-0020).
- 2026-10-12: REPORT: **S2 done** (`23b9ac1`, merge `1b86a26`): custom solvers and proxies per plugin, extension, source or provider (owner model as profiles; usable only by profiles in the same scope; deleted with the plugin). A flaky image-budget test fixed (`1a05f2f`). Meta's answers: admin scope covers everything; provider schedules and settings are config-only (shown read-only); search rebuild is a job; duplicates page by status, min score and judged-only; confirming a duplicate is final. Next: S1 meta admin.
