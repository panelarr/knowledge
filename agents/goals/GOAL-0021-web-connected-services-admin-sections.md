---
title: "GOAL-0021: web: connected services' admin sections"
status: accepted
tags: [goal, agents, web]
related: [planning/features/FEAT-0013-connected-services-admin-inside-panelarr.md, contracts/jobs.md, contracts/source-plugin.md]
inputs: [IN-0039, IN-0063, IN-0064, IN-0065]
repos: [web]
session: "panelarr-web"
features: [FEAT-0013]
updated: 2026-10-12
---

# GOAL-0021: web: connected services' admin sections

The brief a coding session works from. Read this file and follow it.

## Status

`accepted`, **Done 2026-10-12** (verified, pass; [test report](../../qa/reports/goal-0021-web-connected-services-done-verification.md)). The owner accepted [FEAT-0013](../../planning/features/FEAT-0013-connected-services-admin-inside-panelarr.md) (IN-0064). Design by `panelarr-server`, accepted by the keeper (see GOAL-0019's history).

## Context

- Read [FEAT-0013](../../planning/features/FEAT-0013-connected-services-admin-inside-panelarr.md), [contracts/jobs.md](../../contracts/jobs.md), [contracts/source-plugin.md](../../contracts/source-plugin.md).
- **Decided:** everything in mihon-source's and meta's admin (apart from their API clients and keys) is usable from Panelarr's admin; mihon-source is reached **generically through source-mihon and source.v1** (capabilities, like packages), not with a mihon-source admin key; meta is proxied by the server with its admin key; one Jobs view for the server, plugins and meta; network resources stay Panelarr's, with custom solvers, proxies and profiles per plugin kept in Panelarr's store (IN-0065).
- Same working rules as before: slices, gated checks, merge to local main, never push, `REPORT:` per slice; every merge is redeployed for the owner (IN-0056).

## Objective

After GOAL-0017 and FEAT-0012 R4. On the plugin page (tabs built to grow) and on the metadata service's page: stores' status and refresh, package details and reload, sources' health checks (results, check now), one Jobs component for the server, plugins and meta (list, history, run with params, cancel, polling while running), meta's providers and sync runs, duplicates review with the judge, search engine settings. PROPOSE when you get there.

## Definition of Done

- [x] mihon-source sections on the plugin page
- [x] meta sections on the metadata service page
- [x] One Jobs component for every service
- [x] Tests incl. phone, layout and axe
- [x] Docs; checks green; leak-check clean
- [x] `DONE:` with evidence per box

## History

- 2026-10-12: brief written from the accepted server design.
- 2026-10-12: plan PROPOSEd and accepted. S1 one Jobs component for the server, meta and plugins (events for server jobs, polling for the others); S2 plugin admin (stores with refresh on the Extensions tab, package reload and details, a Sources tab with health, scheduled-check switch and "Check now"); S3 a metadata service page at /admin/metadata (overview, providers and sync runs, jobs, network) plus "Refresh from providers" on a work; S4 duplicates review with the judge; S5 search engine, docs, DONE. Keeper answers: "Check now" uses a plugin job that declares a `source_ids` string_list param (convention recorded in contracts/jobs.md); meta gets its own /admin/metadata page with tabs, linked from System.
- 2026-10-12: REPORT: **S1 done** (`9f66ccc`): one set of Jobs screens for the server, meta and plugins (events for the server, polling for meta and plugins); a Jobs tab on plugins with the capability; a new Admin → Metadata page (Overview, Jobs, Network) with the connection and meta network moved there from System.
- 2026-10-12: REPORT: **S2 done** (`2dbd31a`): stores with Refresh now on the Extensions tab, an installed extension's details and Reload, a Sources tab (health, search and filters, scheduled-check switch, "Check now" through the per-source job convention), cron schedules in words (UTC assumed; time zone asked of the server). A rare reader-stability e2e flake under full parallel load is being watched.
- 2026-10-12: REPORT: **S3 done** (`86ff8a9`): Metadata Overview with per-component health; a Providers tab (schedules in words, last runs, start a full sync or changes, runs and run details with polling); "Refresh from providers" on a catalogue entry; the plugin Sources tab hides not-present sources by default; cron labels use `time_zone`; the light theme's warning colour darkened to pass contrast.
- 2026-10-12: REPORT: **S4 done** (`12dc5e6`): Metadata → Duplicates (pairs with filters in the URL; a pair side by side with why they look alike and the model's verdict; merge with a can't-undo confirmation, different works, take back), the decision model card and settings (key write-only, test without saving, reset to configuration); @every and @daily-style schedules read in words.
- 2026-10-12: REPORT: **S5 done** (`c40ed4a`): Metadata → Search (engine state and capabilities, index status, rebuild through meta's job, settings with test and reset). DONE received and verified on a clean clone (`make check` 355, `make e2e` 61). Goal closed; FEAT-0013 delivered.
