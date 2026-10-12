---
title: "GOAL-0018: source plugins: network profiles and per-source settings"
status: accepted
tags: [goal, agents, source-api, source-mihon, mihon-source]
related: [planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md, agents/goals/GOAL-0015-server-shared-network-services-and-plugin-admin-settings.md, architecture/networking.md]
inputs: [IN-0058, IN-0059]
repos: [source-api, source-mihon, mihon-source]
session: "panelarr-mihon-source"
features: [FEAT-0010]
updated: 2026-10-12
---

# GOAL-0018: source plugins: network profiles and per-source settings

The brief a coding session works from. Read this file and follow it.

## Status

`accepted` (2026-10-12): the plugin side of [FEAT-0010](../../planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md), from `panelarr-server`'s GOAL-0015 plan. PROPOSE briefly, then build.

## Context

- Read [FEAT-0010](../../planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md), GOAL-0015 (its history has the server plan), [architecture/networking.md](../../architecture/networking.md).
- Decided (IN-0059): Panelarr's profiles are options assigned per plugin, extension or source; the host pushes the effective profile per source with `SetNetworkProfile`; an unset profile means the plugin's own default; all plugin admin settings show in Panelarr.

## Objective

1. **source-mihon** declares `COMMON_SERVICE_NETWORK_PROFILE` and `SOLVER` and implements `SetNetworkProfile` per source by forwarding to mihon-source; a pushed profile wins over mihon-source's own assignment, an unset one falls back to it. Persist pushed profiles (or document reliance on the host's re-push).
2. **Restart detection:** an additive per-start `instance_id` in `HealthResponse` (or `PluginInfo`) in source.v1, so hosts notice a fast restart and re-push config and profiles.
3. **Per-source settings:** `GetSettingsSchema` / `GetSettings` / `SetSettings` mapped to Mihon preferences, with `SOURCE_CAPABILITY_SETTINGS` on those sources and writeOnly on secrets; x-order kept.
4. Optional: `GetNetworkProfile(source_id)` so a host can show what a plugin actually applies.

## Constraints

Same as GOAL-0012: worktrees, gated checks, merge to local main, never push, no real store or site names, additive proto changes.

## Definition of Done

- [ ] source-mihon applies pushed profiles per source end to end against the real mihon-source (proxy and solver honoured; unset falls back)
- [ ] `instance_id` in source.v1, SDK and conformance
- [ ] Per-source settings through source.v1 end to end
- [ ] Checks green; docs; leak-check clean
- [ ] `DONE:` with evidence per box

## History

- 2026-10-12: brief written from the server's GOAL-0015 plan.
- 2026-10-12: plan PROPOSEd and accepted. Already there: source-mihon declares NETWORK_PROFILE and SOLVER and forwards SetNetworkProfile; mihon-source persists pushed profiles (passwords encrypted; pushed beats its own assignment; unset falls back); settings pass through with x-order. New (additive): `HealthResponse.instance_id` (per start; SDK fills it; source-mihon combines its own and mihon-source's), `GetNetworkProfile` with origin PUSHED / PLUGIN / NONE (secrets empty), writeOnly for password preferences. Slices: source-api, mihon-source, source-mihon with an e2e (proxy and solver honoured, fallback, restart, settings round trip, instance_id change), docs.
- 2026-10-12: REPORT: **slices 1–2 done**: source-api `348bc2d` (`HealthResponse.instance_id`, SDK-filled; optional `GetNetworkProfile` with origin PUSHED / PLUGIN / NONE, no password; conformance); source-mihon `eb60687` (pass-through, combined instance ID); mihon-source `c5ea860` (instance ID per start, GetNetworkProfile from its resolver, password preferences marked writeOnly, read back empty, kept on an empty write). Next: slice 3 e2e.
