---
title: "FEAT-0010: Shared network services and plugin admin settings in Panelarr"
status: proposed
tags: [feature, admin, networking, plugins, server, web, meta, source-mihon, mihon-source]
related: [architecture/networking.md, decisions/ADR-0016-per-source-network-profiles.md, architecture/plugins.md, contracts/source-plugin.md, contracts/metadata-plugin.md, planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md]
inputs: [IN-0058, IN-0007, IN-0039]
milestone: ""
priority: P2
updated: 2026-10-12
---

# FEAT-0010: Shared network services and plugin admin settings in Panelarr

## Problem

"also extensions should expose all admin settings like network profiles and etc for admin too, now i would need to go to mihuo admin to do it. Also the admin should provide some of those services to all plugins from main app config like flaresolver, proxies and etc so u could access those inside source/meta plugins too and dont need to repeat same config multiple times" (IN-0058).

Today solvers (FlareSolverr and the like), proxies and network profiles are configured separately in mihon-source's admin and meta's admin, and Panelarr itself has none (left out of v0). The design already plans for the host to own them: per-source **network profiles** ([networking](../../architecture/networking.md), [ADR-0016](../../decisions/ADR-0016-per-source-network-profiles.md), proposed), plugins declaring the **common services** they can use (IN-0007), and `SetNetworkProfile` pushed by the host in `source.v1` (and planned in `metadata.v1`).

## Outcome

An admin configures solvers, proxies (including VPN-style proxy containers) and network profiles **once, in Panelarr**. Every plugin that declares it can use them gets them pushed: source plugins and meta's providers. Per-source settings a plugin offers (network profile assignment, the source's own preferences) are edited on the plugin's page in Panelarr, so the standalone admins are only needed when running those services alone.

## Scope (suggested)

- **In:**
  - Panelarr admin → **Network**: solvers (FlareSolverr / Byparr endpoints, tested on save), proxies (HTTP / SOCKS5, with credentials as secrets), and **network profiles** (proxy, solver, user agent, rate limits, DoH), with a global default profile;
  - **assignment**: a default profile per plugin and an override per source; profiles pushed to plugins that declare `NETWORK_PROFILE` / `SOLVER` through `SetNetworkProfile`, again when changed and after a plugin restarts;
  - **plugin page → per-source settings**: for each source, its network profile and its own settings (`GetSettingsSchema` / `SetSettings`, e.g. Mihon preferences), in the same schema form;
  - **meta**: the same shared services reach meta's providers (how: [Q-0045](../../questions/README.md));
  - which other plugin admin settings show in Panelarr: [Q-0046](../../questions/README.md).
- **Out:**
  - mihon-source's API clients and keys (they stay in its own admin; Panelarr holds the key it uses);
  - running VPN containers (Panelarr points at a proxy endpoint; the container is the admin's, e.g. the documented gluetun example).

## Acceptance criteria (draft)

- [ ] AC1: An admin adds a solver and a proxy in Panelarr once; a test button shows they work.
- [ ] AC2: An admin builds network profiles from them and sets a global default, a default per plugin and an override per source.
- [ ] AC3: source-mihon (and through it mihon-source) uses the assigned profile for each source without anything configured in mihon-source's own admin; changes apply within seconds and survive a plugin restart.
- [ ] AC4: meta's providers that declare the service use the shared solver/proxy (per Q-0045) without configuring meta's admin.
- [ ] AC5: The plugin page shows each source's settings and its profile; saving them reaches the plugin.
- [ ] AC6: Secrets (proxy passwords, solver keys) are stored encrypted, never shown again, and never sent to browsers.
- [ ] AC7: A plugin that doesn't declare a common service never receives it; a standalone mihon-source or meta keeps working with its own admin settings when not connected to Panelarr.

## Design notes

- Panelarr wins over a service's own admin when connected (as decided for mihon-source config, Q-0030); the standalone admins stay for standalone use.
- Already in the wire contracts: `PluginInfo.common_services` (`NETWORK_PROFILE`, `SOLVER`), `SetNetworkProfile`, `GetSettingsSchema` / `GetSettings` / `SetSettings` in `source.v1`; `SetNetworkProfile` for metadata plugins is planned ([contracts/metadata-plugin.md](../../contracts/metadata-plugin.md)).
- Go plugins already have `source-api/sdk/httpx.NewClient(profile)`; mihon-source builds one HTTP client per source from its profile.

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| | | | |

## Open questions

- [Q-0045](../../questions/README.md): meta and its plugins.
- [Q-0046](../../questions/README.md): which plugin admin settings Panelarr shows.
- ADR-0016 (per-source network profiles) is still `proposed`; this feature would rely on it.
