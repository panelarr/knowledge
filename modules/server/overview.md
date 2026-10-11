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

The Go core and the only **required** component ([ADR-0011](../../decisions/ADR-0011-composable-opt-in-deployment.md)). It owns users, Works, per-user libraries, the job queue, files, the plugin host, network profiles, search and trackers. It serves the REST API and embeds the web build. On its own, with SQLite, built-in search and no plugins, it is a working, if empty, install.

## Owns / does not own
- **Owns:** everything in the [domain model](../../architecture/domain-model.md); [multi-user](../../architecture/multi-user.md) enforcement; [plugin host](../../architecture/plugins.md); [network profiles](../../architecture/networking.md); [search](../../architecture/search.md) (library scope); [trackers](../../architecture/trackers.md); [storage](../../architecture/storage-layout.md).
- **Does not own:** scraping or extension runtime (plugins); metadata aggregation (meta); UI (web).

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
internal/meta/           meta client (remote) or embedded meta
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
Env and flags, *arr*-style: `PANELARR_DB` (DSN), `PANELARR_DATA`, `PANELARR_CONFIG`, `PANELARR_BASE_URL`, `PANELARR_SEARCH_BACKEND`, `PANELARR_META_URL` (empty = embedded/off). Everything else lives in the UI and the DB.

## Implementation status
Not started (M2). Repo not created yet.

## Open questions
[Q-0004](../../questions/README.md), [Q-0021](../../questions/README.md), [Q-0025](../../questions/README.md).
