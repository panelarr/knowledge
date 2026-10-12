---
title: "GOAL-0016: meta: network profiles from Panelarr for meta plugins"
status: accepted
tags: [goal, agents, meta]
related: [planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md, architecture/networking.md, decisions/ADR-0016-per-source-network-profiles.md]
inputs: [IN-0058, IN-0059]
repos: [meta, meta-mangabaka]
session: "panelarr-meta"
features: [FEAT-0010]
updated: 2026-10-12
---

# GOAL-0016: meta: network profiles from Panelarr for meta plugins

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0016-meta-network-profiles-from-panelarr-for-meta-plugins.md"* is not needed; read this file and follow it.

## Status

`accepted` (2026-10-12): the owner accepted [FEAT-0010](../../planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md) with its assignment model (IN-0059). **PROPOSE your plan first**; the keeper reviews it and coordinates the three goals (GOAL-0015 server, GOAL-0016 meta, GOAL-0017 web). Plugin-side gaps (source-api, source-mihon, mihon-source) go to `panelarr-mihon-source` through the keeper.

## Context

- **Read first:** [FEAT-0010](../../planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md) (the owner's words are quoted there), [architecture/networking.md](../../architecture/networking.md), [ADR-0016](../../decisions/ADR-0016-per-source-network-profiles.md) (proposed), [contracts/source-plugin.md](../../contracts/source-plugin.md), [contracts/metadata-plugin.md](../../contracts/metadata-plugin.md).
- **Accepted decisions are law** (IN-0059):
  - solvers, proxies and network profiles live in Panelarr as **options**; nothing uses one until an admin assigns it;
  - assignment to a **whole plugin** (source plugin or meta plugin), an **extension**, or a **source**, the most specific wins; a **custom** profile per extension or source when needed; "choose or create new" from the plugin;
  - **all plugin admin settings in Panelarr**, apart from creating new integrations inside a plugin (integrations are Panelarr's).
- Same working rules as your earlier goals: slices, gated checks, merge to local main, never push, `REPORT:` per slice, `PROGRESS.md`; after each merge the keeper has the compose stack redeployed (IN-0056).

## Objective

1. Accept a network profile per provider pushed by a host (Panelarr), building on meta's existing pushed-profile support (GOAL-0003): pushed wins while connected, meta's own settings stay for standalone use.
2. Pass the effective profile to providers that declare the service: `SetNetworkProfile` for metadata plugins (additive, planned in contracts/metadata-plugin.md), with SDK support (`httpx`-style client from the profile).
3. Expose to the host what each provider declares (common services) so Panelarr only offers profiles where they apply.
4. Keep doing redeploys of the compose stack when the keeper asks (IN-0056).

## Definition of Done

- [ ] Per-provider pushed profiles, host wins while connected
- [ ] SetNetworkProfile for metadata plugins with SDK support
- [ ] Common services visible to the host
- [ ] Docs updated; checks green; leak-check clean
- [ ] `DONE:` with evidence per box

## History

- 2026-10-12: brief written and dispatched on the owner's acceptance (IN-0059); plan to be PROPOSEd first.
