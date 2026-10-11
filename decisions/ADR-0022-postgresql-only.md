---
title: "ADR-0022: PostgreSQL is the only database"
status: accepted
tags: [database, deployment]
related: [decisions/ADR-0004-database-portability.md, decisions/ADR-0011-composable-opt-in-deployment.md, decisions/ADR-0023-sqlc-pgx-goose-data-layer.md, architecture/deployment.md, architecture/search.md]
inputs: [IN-0003, IN-0009]
updated: 2026-10-11
---

# ADR-0022: PostgreSQL only

- **Date:** 2026-10-11
- **Deciders:** @aurimasniekis
- **Supersedes:** [ADR-0004](ADR-0004-database-portability.md). Replaces the database points of [ADR-0011](ADR-0011-composable-opt-in-deployment.md).

## Context

ADR-0004 supported SQLite (default), PostgreSQL and MySQL/MariaDB, following "sqlite/postgres/mysql (optional but if possible and not too difficult)" (IN-0003 §1). While planning meta, the owner said "or maybe lets just do postgres solo and thats all" (IN-0009 §4). Asked whether that meant building Postgres first, meta only, or the whole app, the owner chose **the whole app: Postgres-only** (IN-0009 §5).

## Decision

- **PostgreSQL is the only database** for every Panelarr service with a database: server and meta.
- SQLite and MySQL/MariaDB are **dropped**.
- Postgres-specific features are fair game: full-text search (`tsvector`), `pg_trgm`, JSONB, `SKIP LOCKED` job queues, and Postgres-only libraries.
- Reading provider files that happen to be SQLite (e.g. the MangaBaka dump) is not a database choice. Plugins may still read them.

## Consequences

- **A Postgres instance is required.** "`server` alone is a working install" now means server + Postgres. Everything else stays opt-in ([ADR-0011](ADR-0011-composable-opt-in-deployment.md), annotated).
- **Deploy:** compose runs `postgres` by default (not behind a profile), and Unraid templates point at a Postgres container. Whether the AIO image bundles Postgres is part of M5 packaging.
- **One dialect** means one set of migrations, one CI target and no portability layer. The data layer changes with it ([ADR-0023](ADR-0023-sqlc-pgx-goose-data-layer.md)).
- **Search:** the built-in backend is Postgres FTS + `pg_trgm` only ([ADR-0017](ADR-0017-search-interface-builtin-default.md), proposed).
- **Jobs:** Postgres-only queue libraries (e.g. river) become an option for server.
- Q-0011 (is MySQL worth it?) is answered: no.

## Alternatives considered

| Option | Why not |
|---|---|
| Keep ADR-0004 and build Postgres first | Offered; the owner chose Postgres-only |
| Postgres-only for meta, multi-DB for server | Offered; the owner chose the whole app |
| Postgres + SQLite, drop MySQL | Offered; keeps a zero-setup default but doubles the dialect work |
