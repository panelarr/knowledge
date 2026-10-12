---
title: "GOAL-0014: web: Extensions tab, admin Sources, no user source browsing"
status: accepted
tags: [goal, agents, web]
related: [planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md, agents/goals/GOAL-0013-server-extensions-source-languages-admin-only-sources.md]
inputs: [IN-0052, IN-0053, IN-0054, IN-0055]
repos: [web]
session: "panelarr-web"
features: [FEAT-0009]
updated: 2026-10-12
---

# GOAL-0014: web: Extensions tab, admin Sources, no user source browsing

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0014 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`accepted` (2026-10-12): the owner accepted [FEAT-0009](../../planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md) (IN-0055). Builds on GOAL-0013's API: work against the server's draft spec and mocks as before; PROPOSE your plan once the server's plan is in.

## Context

- Code: `~/Projects/Panelarr/web`.
- **Read first:** [FEAT-0009](../../planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md), GOAL-0012, GOAL-0013.
- **Accepted decisions are law** (IN-0053..IN-0055): the Extensions tab is on the **plugin's page** and only for plugins that declare the capability; languages on the plugin and per extension decide which sources exist; **sources are admin-only**, regular users see a work's sources only on the work; admins keep a "browse a source" view in Admin → Sources.

## Objective

1. **Plugin page → Extensions tab** (only when the plugin declares the capability): available extensions from all stores with name, language(s), version, installed version, update available, content warning and store; search and language filter; install, update, uninstall with progress; per-extension enabled languages.
2. **Admin → Sources:** language and providing extension per source, language filter, enable/disable, and the "browse a source" view for testing.
3. **Regular users:** no Sources page or direct source browsing (Browse → Sources goes away for them); a work's source tabs show each source's language.
4. Mobile-first and accessible like the rest; extend the layout spec to the new pages.

## How to work

As in GOAL-0011: slices, `make check` and `make e2e` green, `REPORT:` per slice, `PROGRESS.md`.

## Constraints

- Merge to local main yourself; never push; don't touch the running stack.

## Definition of Done

- [ ] Extensions tab for capable plugins (list, filter, install, update, uninstall, languages)
- [ ] Admin Sources with language, enable/disable and browse-for-testing
- [ ] No source browsing for regular users; languages on a work's sources
- [ ] Tests (unit, Playwright incl. phone and layout); docs; leak-check clean
- [ ] `DONE:` with evidence per box

## History

- 2026-10-12: brief written and dispatched on the owner's go (IN-0055).
- 2026-10-12: plan PROPOSEd and accepted by the keeper. S0 admin-only sources (Browse → Sources moves to Admin → Sources → a source as the test view; old links redirect; a work's sources show lang). S1 Admin → Sources (language, package, filters in the URL, on/off; "Off" vs "Not available" vs "Absent" kept apart). S2 Extensions tab (only with the packages capability; virtualised list, search and language filter, install/update/uninstall as tasks with live progress, a package sheet with its sources and enabled_langs). S3 layout, axe, journey test, docs. Work page "Search this source" for match fixers: admin-only until the server adds a work-scoped search (asked of panelarr-server).
- 2026-10-12: REPORT: **S0 done** (`556a01f`): source browsing moved to Admin → Sources → a source (the test view, with add to library); Browse is the catalogue only; old links redirect (admins to the admin page with the search kept, others to /browse); a work's source tabs show language; search-by-hand admin-only until the work-scoped search lands. Keeper decision on its assumption: admins may browse a source that's Off (for testing before turning it on); Not available and Absent sources can't be browsed (the plugin answers NOT_FOUND). Asked of panelarr-server for S2.
- 2026-10-12: REPORT: **S1 part one** (`d51440d`): fixers have search-by-hand back via the work-scoped search (results marked Attached / Candidate / Rejected); Admin → Sources shows Off and Absent apart, plugin names in the filter; admins browse Off sources; Absent ones show the reason. Deviation accepted: Admin → Sources filters one full list in the browser (instant filters, one request), server filters used where a slice is enough. Waiting on S3 for the providing package and "Not available".
