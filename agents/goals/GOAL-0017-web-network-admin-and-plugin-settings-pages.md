---
title: "GOAL-0017: web: Network admin and plugin settings pages"
status: accepted
tags: [goal, agents, web]
related: [planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md, architecture/networking.md, decisions/ADR-0016-per-source-network-profiles.md]
inputs: [IN-0058, IN-0059]
repos: [web]
session: "panelarr-web"
features: [FEAT-0010]
updated: 2026-10-12
---

# GOAL-0017: web: Network admin and plugin settings pages

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0017-web-network-admin-and-plugin-settings-pages.md"* is not needed; read this file and follow it.

## Status

`accepted`, **Done 2026-10-12** (verified, pass with issues; [test report](../../qa/reports/goal-0017-web-network-admin-done-verification.md)). The owner accepted [FEAT-0010](../../planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md) with its assignment model (IN-0059). **PROPOSE your plan first**; the keeper reviews it and coordinates the three goals (GOAL-0015 server, GOAL-0016 meta, GOAL-0017 web). Plugin-side gaps (source-api, source-mihon, mihon-source) go to `panelarr-mihon-source` through the keeper.

## Context

- **Read first:** [FEAT-0010](../../planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md) (the owner's words are quoted there), [architecture/networking.md](../../architecture/networking.md), [ADR-0016](../../decisions/ADR-0016-per-source-network-profiles.md) (proposed), [contracts/source-plugin.md](../../contracts/source-plugin.md), [contracts/metadata-plugin.md](../../contracts/metadata-plugin.md).
- **Accepted decisions are law** (IN-0059):
  - solvers, proxies and network profiles live in Panelarr as **options**; nothing uses one until an admin assigns it;
  - assignment to a **whole plugin** (source plugin or meta plugin), an **extension**, or a **source**, the most specific wins; a **custom** profile per extension or source when needed; "choose or create new" from the plugin;
  - **all plugin admin settings in Panelarr**, apart from creating new integrations inside a plugin (integrations are Panelarr's).
- Same working rules as your earlier goals: slices, gated checks, merge to local main, never push, `REPORT:` per slice, `PROGRESS.md`; after each merge the keeper has the compose stack redeployed (IN-0056).

## Objective

1. **Admin → Network**: solvers and proxies (add, test, edit; secrets write-only), network profiles.
2. **Assignment pickers**: on a plugin's page (source or meta plugin), in an extension's sheet and on a source: choose an existing profile, create a new one in place, or a custom one; show the effective profile and where it comes from.
3. **Per-source settings** on the plugin page (schema form), with the source's profile.
4. Build against the server's draft spec and mocks; PROPOSE after the server's plan.

## Definition of Done

- [x] Admin → Network (integrations, profiles)
- [x] Assignment at plugin, extension and source level, with create-in-place and custom profiles
- [x] Per-source settings
- [x] Tests incl. phone and layout
- [x] Docs updated; checks green; leak-check clean
- [x] `DONE:` with evidence per box

## History

- 2026-10-12: brief written and dispatched on the owner's acceptance (IN-0059); plan to be PROPOSEd first.
- 2026-10-12: per-source settings pulled forward (IN-0062) and done (`f61ad6e`): a Settings button on sources with the capability (Admin → Sources row, the source's browse page, the Extensions sheet), a schema-form dialog with write-only secrets and x-order. The rest of this goal follows FEAT-0012.
- 2026-10-12: plan PROPOSEd and accepted (after the reader jump fix, IN-0066). N1 Admin → Network (solvers, proxies, profiles with tests; global and meta defaults); N2 one profile picker at every level showing what's in effect and push state (plugin page Network tab, extension sheet, a source's "Settings & network", the metadata service page); N3 custom solvers, proxies and profiles per plugin (IN-0065); N4 layout, axe, journey, docs. Answers: plugin page tabs built to grow (FEAT-0013); meta's pickers on the metadata service's page, not Admin → Network; creating in a picker makes a custom item, shared ones only on Admin → Network.
- 2026-10-12: REPORT: **N1 done** (`d107983`): Admin → Network with Profiles / Proxies / Solvers tabs, "Show custom ones too", a global "For everything" choice (None by default), tests before saving, write-only passwords, delete refused while in use with the reason. Next: N2 pickers.
- 2026-10-12: REPORT: **N2 done** (`df04df5`): one profile picker at every level, showing what's in effect, where from and whether it arrived; inherit, the plugin's own settings, shared, or a custom one made in place; placed on the plugin page's new Network tab (plugin, each extension, each source), the extension sheet, a source's "Settings and network" dialog and the metadata service card on Admin → System. Next: N3.
- 2026-10-12: REPORT: **N3** (`f65410d`, plugin-owned proxies, solvers and profiles on the Network tab) and **N4** (`dd2e2a5`, journey e2e, docs/network.md). DONE received. Keeper verification on a clean clone under very heavy machine load: unit tests passed on a re-run; e2e had 2 different timeout failures on each of two runs. Goal closed with the flakiness sent back for hardening.
