---
title: "GOAL-0023: web: image retry settings in the extension admin"
status: accepted
tags: [goal, agents, web]
related: [planning/features/FEAT-0016-automatic-retries-for-failed-page-images.md, agents/goals/GOAL-0022-server-automatic-retries-for-failed-page-images.md]
inputs: [IN-0079, IN-0080]
repos: [web]
session: "panelarr-web"
features: [FEAT-0016]
updated: 2026-10-18
---

# GOAL-0023: web: image retry settings in the extension admin

The brief a coding session works from. Read this file and follow it.

## Status

`accepted`, **Done 2026-10-18** (verified, pass; [test report](../../qa/reports/feat-0016-image-retries-verification.md)). The owner accepted [FEAT-0016](../../planning/features/FEAT-0016-automatic-retries-for-failed-page-images.md) (IN-0080). GOAL-0022's API is merged (server `6ff0878`).

## Context

- Read [FEAT-0016](../../planning/features/FEAT-0016-automatic-retries-for-failed-page-images.md) and [GOAL-0022](GOAL-0022-server-automatic-retries-for-failed-page-images.md).
- **Decided (IN-0080):** the setting is on an extension (all its sources), with an optional override on one of its sources; default 2 more attempts, 1 s then 3 s.
- Same working rules as before: slices, gated checks, merge to local main, never push, `REPORT:` per slice; every merge is redeployed for the owner (IN-0056). Live checks on the owner's stack never change the owner's settings or progress: use a throwaway user and put back anything you change.

## Objective

In the plugin page's extension details: an "Image retries" setting (attempts and delays) for the extension, showing the default when unset. On a source of that extension: an override, showing the inherited value and where it comes from, with reset to inherit. The reader keeps its manual "Try again" for when the attempts run out.

## Definition of Done

- [x] Extension setting and per-source override, with inherited values shown and reset
- [x] Tests incl. phone, layout and axe
- [x] Checks green; leak-check clean
- [x] `DONE:` with evidence per box

## History

- 2026-10-18: brief written from the accepted FEAT-0016.
- 2026-10-18: plan PROPOSEd and accepted by the keeper. One shared control (like the network profile picker): Inherit (says what it inherits; choosing it DELETEs), Off ([]), Custom (up to 5 rows "Attempt N after [x] s", 0–30 s, prefilled from what is in effect), with a line "In effect: … (set here / from its extension / the default)". On the extension details sheet after Network (also when not installed) and in the source settings dialog after Network; admin only. Saving an extension refreshes its sources' inherited text. Tests: unit for the states, e2e on desktop and phone, layout and axe; docs/admin.md.
- 2026-10-18: DONE (`3f73d90`): the shared control (src/features/extensions/image-retries.tsx) on the extension sheet and the source settings dialog; saves refresh every cached image-retries query; inline bounds and the server's refusal; docs/admin.md. Verified on a clean clone (`make check` 392, `make e2e` 65). Goal closed; FEAT-0016 delivered.
