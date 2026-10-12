---
title: "FEAT-0013: Connected services' admin inside Panelarr"
status: accepted
tags: [feature, admin, server, web, meta, mihon-source, source-mihon]
related: [modules/web/overview.md, planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md, planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md, decisions/ADR-0021-mihon-source-standalone-admin.md]
inputs: [IN-0065, IN-0039, IN-0063, IN-0064]
milestone: ""
priority: P1
updated: 2026-10-12
---

# FEAT-0013: Connected services' admin inside Panelarr

## Problem

"i meant also plugin settings, like mihon-source network stuff, resolvers, profiles, too not only extensions settings. like imagine meta/source admin page settings inside the admin here" (IN-0063). Asked whether the rest of mihon-source's and meta's admin pages should live inside Panelarr's admin: "Yes, all of it" (IN-0064). On network: "like Panelarr's Network page it defines profiles/proxies/resolvers and in plugin it becomes available for its settings so like on mihon-source setting i can choose resolver from Panelarr itself" (IN-0064).

This is the connected-services idea from IN-0039, left out of v0.

Custom network resources (IN-0065): on each plugin's page the admin can also create custom resolvers, proxies and profiles for that plugin, as in its own admin; Panelarr's shared ones are offered as options.

## Outcome

Everything an admin does in mihon-source's or meta's own admin can be done from Panelarr's admin, on that plugin's page. Network resources (solvers/resolvers, proxies, profiles) are defined once on Panelarr's Network page and picked from inside each plugin's settings (FEAT-0010). The standalone admins stay for people running those services alone.

## Scope

- **Network in plugin settings** (FEAT-0010, GOAL-0017): on a plugin's page (source-mihon, meta and its providers), the network part of its settings lets the admin choose a profile, proxy or resolver defined on Panelarr's Network page, or create one there.
- **mihon-source sections** on the source-mihon plugin page: stores (already), extensions (FEAT-0009), sources and their health checks (results, run now, the check settings), jobs (list, history, run now, cancel), anything else its admin offers apart from API clients and keys.
- **meta sections** on the meta page (Admin → System → Metadata, or a meta plugin page): providers and their syncs (history, start, settings), jobs, duplicates review, search engine settings and rebuild, integrations shown from Panelarr's Network page.
- **Out:** the services' own API clients and keys (Panelarr holds the key it uses); creating network integrations inside a plugin (they're Panelarr's, Q-0046).

## Acceptance criteria (draft)

- [ ] AC1: On the source-mihon plugin page, an admin picks a resolver, proxy or profile from Panelarr's Network page for the plugin, an extension or a source, without opening mihon-source's admin.
- [ ] AC2: mihon-source's stores, extensions, sources with health checks, and jobs are all reachable and usable from Panelarr's admin.
- [ ] AC3: meta's providers and syncs, jobs, duplicates review and search engine are reachable and usable from Panelarr's admin.
- [ ] AC4: Everything goes through each service's own admin API with the key Panelarr holds; the browser never talks to mihon-source or meta directly.
- [ ] AC5: The standalone admins keep working when the services run alone.

## Design notes

- How Panelarr reaches mihon-source's admin (through source-mihon, a generic plugin-admin capability in source.v1, or a connected-service link with mihon-source's admin key) is the server's first design question; FEAT-0009's packages capability is a precedent for "generic, only where supported".
- meta is already connected with an admin key; its admin APIs (jobs, duplicates, search, integrations) exist.
- The Jobs contract (contracts/jobs.md) is shared by both services, so one Jobs view can serve both.

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| | | | |
