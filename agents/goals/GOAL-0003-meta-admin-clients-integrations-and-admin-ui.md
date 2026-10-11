---
title: "GOAL-0003: meta admin: clients, integrations and admin UI"
status: accepted
tags: [goal, agents, meta, admin, networking]
related: [agents/goals/GOAL-0002-meta-v0-metadata-protocol-meta-service-and-mangabaka-dump-in.md, modules/meta/overview.md, contracts/metadata-plugin.md, contracts/mihon-source-api.md, architecture/networking.md, architecture/security.md]
inputs: [IN-0007, IN-0020, IN-0021]
repos: [meta, meta-mangabaka]
session: "panelarr-meta"
features: []
updated: 2026-10-11
---

# GOAL-0003: meta admin: clients, integrations and admin UI

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0003 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`accepted`: dispatched to `panelarr-meta` on 2026-10-11 (owner's go, IN-0021). Written from IN-0020.

## Context

- Code: `~/Projects/Panelarr/meta` (most of the work), `~/Projects/Panelarr/meta-mangabaka` (applying a network profile) · branches `<type>/<scope>-<slug>`
- **Read first:**
  1. [modules/meta/overview.md](../../modules/meta/overview.md) (the "Admin" bullet) and [contracts/metadata-plugin.md](../../contracts/metadata-plugin.md) ("Proposed" section).
  2. **The model to copy:** mihon-source already has all of this. Read [contracts/mihon-source-api.md](../../contracts/mihon-source-api.md) and the mihon-source repo (`MihonClientsService`, `MihonIntegrationsService`, its `admin/` SPA, `network/`). Match its concepts, names and UX unless there's a reason not to, so the two admins feel like one product.
  3. [architecture/networking.md](../../architecture/networking.md) (profiles, solvers, VPN as a proxy container) and [architecture/security.md](../../architecture/security.md) (secrets at rest).
  4. Accepted ADRs as in GOAL-0002, plus [ADR-0026](../../decisions/ADR-0026-connectrpc-on-go-grpc-as-the-plugin-wire.md) (gRPC wire) and [ADR-0025](../../decisions/ADR-0025-licences-gpl-3-0-apps-apache-2-0-sdks-and-protos.md) (licences).
- **Accepted decisions are law.** If code and KB disagree, the KB wins, or send `CONFLICT:`.

## Objective

Give meta a minimal admin like mihon-source's (IN-0020). It covers **API key clients**, **integrations** (FlareSolverr/Byparr solvers, network profiles for proxies and VPN containers) and an **admin web UI**. Plugins that use the network actually go through the profile they're given.

## Slices (suggested order)

1. **Clients and auth:** `MetaClientsService` in `meta.v1`. Admin token (env, or generated on first start and printed once), client API keys with scopes (suggested: `catalog:read`, `admin`), hashed at rest, shown once, rotatable, last use recorded. The fixed `api_keys` config keeps working as a fallback, or is migrated; say which in a REPORT.
2. **Integrations:** `MetaIntegrationsService`: solvers, profiles (proxy with auth, solver, UA, rate limit, timeouts), a default profile, assignments per provider. Secrets encrypted at rest, never returned. **Avoid mihon-source's trap:** a solver alone must not silently do nothing (offer a default profile, or warn).
3. **Plugin side:** `SetNetworkProfile` added to `MetadataPluginService` (additive). meta pushes the assigned profile to plugins declaring the `network_profile` common service. The SDK gives plugins a ready HTTP client from a profile (proxy, solver round-tripper with broad challenge detection, rate limit, UA). meta-mangabaka uses it for dump downloads and API calls.
4. **Admin UI:** a React SPA on mihon-source's stack (React + Vite + TanStack), served by meta at `/`. Pages: clients, integrations, providers (health, schedules, sync runs, run now), and browse/search with entry details (suggestion). Token login without cookies, strict CSP, typed client from the OpenAPI.
5. **Image and docs:** the UI built into the meta image; docs for clients, integrations and the admin.

## When something isn't decided

- `ASK:` the keeper first; then `PROPOSE:` a working assumption, built cheap to change.
- Known open point: [Q-0034](../../questions/README.md) (whether server pushes profiles in the full stack). Build it the way mihon-source does: local config, and a pushed profile overrides it.

## Constraints

- Same as GOAL-0002: merge your own branches into `main` before the first release, never push; public repos (KB IDs and links allowed, aliases only); leak-check before each REPORT.
- Everything stays optional: meta runs with no solver, no profile and no admin UI use.

## Definition of Done

- [ ] Clients: admin token plus scoped, hashed, rotatable client keys; a test proves a read key can't call admin APIs
- [ ] Integrations: solvers, profiles, default, per-provider assignment; secrets encrypted and never returned; an unused solver is flagged or auto-wired
- [ ] `SetNetworkProfile` in the plugin protocol; SDK HTTP client from a profile; meta-mangabaka downloads through a proxy in a test
- [ ] Admin UI: clients, integrations, providers and sync runs, browse/search; tests; served at `/` with a strict CSP
- [ ] Docs and image updated; `make check` green; leak-check clean
- [ ] `DONE:` with evidence per box

## History

- 2026-10-11: brief written from IN-0020 (`proposed`); starts after GOAL-0002.
- 2026-10-11: `panelarr-meta` reports that the owner said "go" directly in that session and has started slice 1. **Not confirmed by the owner to the keeper yet**, so the status stays `proposed` until the owner confirms.
- 2026-10-11: the owner confirmed the go to the keeper (IN-0021): `accepted`, dispatched to `panelarr-meta`.
