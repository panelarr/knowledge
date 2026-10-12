---
title: "GOAL-0015: server: shared network services and plugin admin settings"
status: accepted
tags: [goal, agents, server]
related: [planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md, architecture/networking.md, decisions/ADR-0016-per-source-network-profiles.md]
inputs: [IN-0058, IN-0059]
repos: [server]
session: "panelarr-server"
features: [FEAT-0010]
updated: 2026-10-12
---

# GOAL-0015: server: shared network services and plugin admin settings

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0015-server-shared-network-services-and-plugin-admin-settings.md"* is not needed; read this file and follow it.

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

1. **Integrations** (admin): solvers (FlareSolverr/Byparr, with a test), proxies (HTTP/SOCKS5; credentials encrypted, never returned), stored once.
2. **Network profiles** built from them (proxy, solver, user agent, rate limits, DoH), plus custom profiles owned by one extension or source.
3. **Assignment**: per plugin, per extension (package), per source; most specific wins; none = the plugin's own defaults. Resolve the effective profile per source and push it with `SetNetworkProfile` to plugins that declare `NETWORK_PROFILE`/`SOLVER`, on change and after a plugin (re)starts.
4. **Meta**: profiles assignable to a meta plugin (provider); the server pushes the chosen one to meta (coordinate the API with GOAL-0016).
5. **Plugin admin settings**: per-source settings (`GetSettingsSchema`/`GetSettings`/`SetSettings`) through the API, admin only.
6. Tell `panelarr-web` the API as it settles.

## Definition of Done

- [ ] Integrations and profiles API with encrypted secrets and tests
- [ ] Assignment levels with effective-profile resolution and push, including after plugin restarts
- [ ] Meta plugin assignment through GOAL-0016's API
- [ ] Per-source settings API
- [ ] Docs updated; checks green; leak-check clean
- [ ] `DONE:` with evidence per box

## History

- 2026-10-12: brief written and dispatched on the owner's acceptance (IN-0059); plan to be PROPOSEd first.
- 2026-10-12: plan PROPOSEd and accepted by the keeper. Tables for solvers, proxies (secrets sealed), profiles (with optional owner for custom ones), assignments (global, plugin, package, source, meta, provider; a profile or an explicit `plugin_default`; no row = inherit) and push state. Effective profile: source → package → plugin → global → none; provider → meta → global → none. Pushes only to plugins and providers that declare the service (solver stripped without SOLVER), as deduplicated `network.push` tasks, on change, on sync for new sources and after a plugin restart; the server's own limiter follows the profile. Admin API under `/network/...`, `/plugins/{id}/network`, `/system/meta/network`, `/sources/{id}/settings`. Slices: S1 solvers and proxies, S2 profiles and assignments, S3 push, S4 per-source settings, S5 meta. Answers: global default optional and unset (IN-0059); `plugin_default` OK; a meta level above providers OK, plus a level per provider plugin if one plugin serves several providers; deleting a plugin deletes its custom profiles. Plugin-side needs became GOAL-0018.
- 2026-10-12: REPORT: **S1 done** (`d334cad`, merge `171a566`): `/network/solvers` and `/network/proxies` (admin; CRUD plus checks of saved and unsaved settings; proxy passwords sealed and never returned; credentials in proxy URLs refused; delete in use → 409). Notes: meta confirmed SetPushedProfile is persisted with admin scope and re-pushed on reconnect, no plugin level for meta; source-api `348bc2d` has `instance_id` and `GetNetworkProfile`. Next: bookmarks, then S2.
- 2026-10-12: REPORT: **S2 done** (`65e652f`, merge `d409c60`): network profiles (custom ones owned by a plugin and deleted with it; usable only at their owner), assignments (global, plugin, package, source, meta, provider; profile or plugin_default) and effective resolution; `/network/profiles`, `/network/assignments`, `/plugins/{id}/network` (each source's effective profile and level, and whether the plugin accepts profiles and solvers); delete in use → 409. Next: S3 push. Also delivered: chapter bookmarks API (`781ed85`, FEAT-0012).
