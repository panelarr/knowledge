---
title: server overview
status: proposed
tags: [module, server, go]
related: [architecture/overview.md, architecture/domain-model.md, architecture/multi-user.md, contracts/server-api.md]
inputs: [IN-0002, IN-0003]
updated: 2026-10-11
---

# server

## Summary

The Go core. Together with PostgreSQL and **meta** it forms the minimal install ([ADR-0022](../../decisions/ADR-0022-postgresql-only.md), [ADR-0029](../../decisions/ADR-0029-meta-required.md)). It owns users, Works, per-user libraries, the job queue, files, the plugin host, network profiles, search and trackers. It serves the REST API and embeds the web build.

## Owns / does not own
- **Owns:** everything in the [domain model](../../architecture/domain-model.md); [multi-user](../../architecture/multi-user.md) enforcement; [plugin host](../../architecture/plugins.md); [network profiles](../../architecture/networking.md); [search](../../architecture/search.md) (library scope); [trackers](../../architecture/trackers.md); [storage](../../architecture/storage-layout.md).
- **Does not own:** scraping or extension runtime (plugins); metadata aggregation (meta); UI (web).
- **Connected-service admin (IN-0039):** the server keeps an admin-scope key per connected service (meta, mihon-source via source-mihon) as an encrypted secret and exposes their admin APIs to Panelarr admins through its own authorization (a thin, allow-listed proxy or typed clients, suggestion), so the web app can show those pages built in.

## Internal packages (suggested layout)
```
cmd/panelarr/            main; flags/env; migrations on start
internal/api/            REST handlers (OpenAPI-first, generated server interfaces), SSE hub, OPDS
internal/auth/           sessions, API keys, OIDC, grants
internal/library/        Works, SourceSeries, chapters, variants, merge/split
internal/jobs/           DB-backed queue: lease, retry/backoff, per-key limits (plugin, source, host)
internal/download/       page fetch → CBZ + ComicInfo writer, atomic moves
internal/plugins/        index client, verifier, go-plugin manager, remote clients, health
internal/network/        profiles, assignment, push to plugins
internal/search/         SearchIndex + backends (dbfts, typesense, meilisearch)
internal/meta/           meta client (meta is a required separate service, ADR-0029)
internal/trackers/       Tracker interface + implementations
internal/store/          goose SQL migrations, sqlc queries, pgx pool
web/                     go:embed of the web dist (pulled from web releases)
```

## Key technical choices (proposed)
- **DB:** PostgreSQL only ([ADR-0022](../../decisions/ADR-0022-postgresql-only.md)) with sqlc + pgx + goose ([ADR-0023](../../decisions/ADR-0023-sqlc-pgx-goose-data-layer.md)). CI runs against a real Postgres.
- **HTTP:** chi or stdlib `net/http` routing. Server stubs come from OpenAPI via `oapi-codegen` (suggestion).
- **Plugins:** `hashicorp/go-plugin`. ConnectRPC clients for remote endpoints ([Q-0020](../../questions/README.md)).
- **Jobs:** a queue on Postgres: in-house (`SELECT … FOR UPDATE SKIP LOCKED`) or a library such as river, now that Postgres is the only database (open, suggestion: try river first).
- **Images:** an image proxy for un-downloaded pages; cover thumbnails cached in `/config/cache`.

## Configuration
Env and flags, *arr*-style: `PANELARR_DB` (DSN), `PANELARR_DATA`, `PANELARR_CONFIG`, `PANELARR_BASE_URL`, `PANELARR_SEARCH_BACKEND`, `PANELARR_META_URL` and `PANELARR_META_KEY` (pre-fill the setup wizard; when set they win and show read-only; meta is required, ADR-0029). Everything else lives in the UI and the DB.

## Implementation status
In progress (GOAL-0010, `panelarr-server`). Slice 0 (scaffold) merged at `f14d9a4`: `panelarr serve|migrate|healthcheck|version`, config from env and flags, slog JSON, metrics off by default on a private listener, `/healthz` and `/readyz` (required vs optional checks, for "degraded" when meta is down), pgx/goose/sqlc with a `settings` table, spec-first OpenAPI 3.1 with a generated chi server, problem+json errors, CI with an API breaking-change check. Slice 1 (accounts and setup, FEAT-0003 AC1 and AC3–AC5) merged at `4aadeec`: users, roles and grants, the first-run gate, sessions, scoped API keys, invites, a users admin, and an authorization test across every API operation. Slice 2 (meta connection and catalogue, FEAT-0003 AC2, FEAT-0004 AC1) merged at `7643a8a`: a gRPC meta client, the wizard check (reachable, admin key, provider with records) with a "run first sync" action, meta as an optional readiness check (degraded, not down), catalogue search/browse/details filtered by the user's rating ceiling, and a cover cache. Slice 3 (source plugins, remote; FEAT-0003 AC4 for sources) merged at `b57831a`: register plugin instances by URL and key, sync their sources and health, plugin config via SetConfig (re-sent on server start and when a plugin comes back), per-user source visibility, browse/search/series/chapters/images through the server with signed image links. Slice 4 (jobs and events) merged at `1f47386`: an in-house task queue (SKIP LOCKED, leases, retries with back-off and retry-after, dedupe, per-kind and per-source concurrency, pause/resume), per-source limits from `PluginInfo.limits` (default 2 at once, 2 req/s), named jobs in the shared contract shape, and an SSE event stream. Slice 5 (works, library and matching; FEAT-0004 AC2–AC6, ADR-0028) merged at `a4b98e9`: one shared Work per meta entry with per-user library entries; matching as queued per-source tasks searching meta's titles (main, source language, romanized, English, others; up to 5 queries), scoring each result against all of meta's titles, auto-attaching only on one exact title plus a shared author; fix match (attach, detach remembered, priority, attach by URL, re-run); add from a source; per-user visibility. Rules explained publicly in the repo's `docs/matching.md`. Next: unified chapters and update checks.

## Open questions
[Q-0004](../../questions/README.md), [Q-0021](../../questions/README.md), [Q-0025](../../questions/README.md).
