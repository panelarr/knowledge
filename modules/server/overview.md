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
In progress (GOAL-0010, `panelarr-server`). Slice 0 (scaffold) merged at `f14d9a4`: `panelarr serve|migrate|healthcheck|version`, config from env and flags, slog JSON, metrics off by default on a private listener, `/healthz` and `/readyz` (required vs optional checks, for "degraded" when meta is down), pgx/goose/sqlc with a `settings` table, spec-first OpenAPI 3.1 with a generated chi server, problem+json errors, CI with an API breaking-change check. Slice 1 (accounts and setup, FEAT-0003 AC1 and AC3–AC5) merged at `4aadeec`: users, roles and grants, the first-run gate, sessions, scoped API keys, invites, a users admin, and an authorization test across every API operation. Slice 2 (meta connection and catalogue, FEAT-0003 AC2, FEAT-0004 AC1) merged at `7643a8a`: a gRPC meta client, the wizard check (reachable, admin key, provider with records) with a "run first sync" action, meta as an optional readiness check (degraded, not down), catalogue search/browse/details filtered by the user's rating ceiling, and a cover cache. Slice 3 (source plugins, remote; FEAT-0003 AC4 for sources) merged at `b57831a`: register plugin instances by URL and key, sync their sources and health, plugin config via SetConfig (re-sent on server start and when a plugin comes back), per-user source visibility, browse/search/series/chapters/images through the server with signed image links. Slice 4 (jobs and events) merged at `1f47386`: an in-house task queue (SKIP LOCKED, leases, retries with back-off and retry-after, dedupe, per-kind and per-source concurrency, pause/resume), per-source limits from `PluginInfo.limits` (default 2 at once, 2 req/s), named jobs in the shared contract shape, and an SSE event stream. Slice 5 (works, library and matching; FEAT-0004 AC2–AC6, ADR-0028) merged at `a4b98e9`: one shared Work per meta entry with per-user library entries; matching as queued per-source tasks searching meta's titles (main, source language, romanized, English, others; up to 5 queries), scoring each result against all of meta's titles, auto-attaching only on one exact title plus a shared author; fix match (attach, detach remembered, priority, attach by URL, re-run); add from a source; per-user visibility. Rules explained publicly in the repo's `docs/matching.md`. Slice 6 (unified chapters and update checks; FEAT-0005 AC1–AC6) merged at `a114382`: per-source chapter lists; canonical chapters grouped by normalized number (volume a majority attribute, unnumbered chapters kept as per-source extras, chapters that lose all copies stay as unavailable); a chosen copy with a reason (pinned → language → healthier source → priority → newest → first listed); pins; update checks every 6 h (jittered) and on demand; per-user "new" badges; a daily refresh of works' display fields from meta. Slice 7 (reader API; FEAT-0006 server side) merged at `e2726f1`: page lists (cached 15 min) and pages fetched through the source plugin, falling back to a copy the user may use; previous/next in unified order; progress per user with completion, bulk read/unread, "continue" and history; reader settings at global, source and work levels merged into `effective`, and per-user preferences (client-owned JSON). Slice 8 (storage and downloads; FEAT-0007) merged at `8179f54`: local and S3-compatible storage with admin test, default and move; CBZ with ComicInfo written atomically; a naming template; de-duplicated downloads under per-source limits; auto-download of new chapters; the reader serves downloaded chapters from the file. Slice 9 part 1 merged at `a64e0cf`: the web app embedded per its contract, and a security review. Slice 9 completed with the container image and release setup (`41418a9`). **v0 done** (GOAL-0010, verified 2026-10-12). Follow-up `2fd70b1`: `library_work_id` on catalogue entries, event schemas with an event table, `current_run_id` on already_running, string_list documented, `chapter_id` on downloads. Page sizes deferred: they would need optional width/height on source.v1 `Page` from plugins (additive) plus reading them from CBZs.

## Open questions
[Q-0004](../../questions/README.md), [Q-0021](../../questions/README.md), [Q-0025](../../questions/README.md).

Meta errors (IN-0049, `0fd607b`): `meta_unavailable` (503) only when meta didn't answer; `meta_provider_unavailable` (502) when meta answered that a provider's plugin is down (meta `5117089` adds `ErrorInfo` reason `PROVIDER_UNAVAILABLE` with the provider); `meta_key_rejected` and `meta_error` (502) for other answered errors.

Plugin health (IN-0050, `6fc6819`): a plugin found down is rechecked on its own after 10s, 30s and 1m (single-plugin syncs, debug logs, no job runs), then by the 5-minute `plugins.sync`; at startup a plugin that doesn't answer gets 1s and 2s waits before it's marked down.

Meta check (`97055ae`): runs detached from the request (own 10s timeout, shared by concurrent callers); a caller that gives up early gets an uncached "didn't finish in time", so one cancelled request can't make the status "degraded" for everyone.

Config follow-up (IN-0051, `844b43f`): after a plugin's config is saved, the server syncs that plugin after 5s and 30s on the same per-plugin chain as the rechecks; every plugin sync publishes a `plugin.health` event to admins (sent after each sync, not only on change).
