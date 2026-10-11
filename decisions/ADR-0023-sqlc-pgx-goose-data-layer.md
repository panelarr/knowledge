---
title: "ADR-0023: sqlc + pgx + goose as the Go data layer"
status: accepted
tags: [database, go]
related: [decisions/ADR-0022-postgresql-only.md, decisions/ADR-0018-ent-atlas-data-layer.md, modules/server/overview.md, modules/meta/overview.md]
inputs: [IN-0009]
updated: 2026-10-11
---

# ADR-0023: sqlc + pgx + goose

- **Date:** 2026-10-11
- **Deciders:** @aurimasniekis
- **Supersedes:** [ADR-0018](ADR-0018-ent-atlas-data-layer.md)

## Context

ent + Atlas (ADR-0018) won because one Go schema served three SQL dialects, while sqlc meant about 3× upkeep with separate queries per dialect. The owner accepted ent + Atlas (IN-0009 §2), then asked about goose for migrations (IN-0009 §3), then made Postgres the only database ([ADR-0022](ADR-0022-postgresql-only.md)). With one dialect, that reason is gone. Asked again, the owner picked **sqlc + pgx + goose** (IN-0009 §5).

## Decision

- **sqlc:** queries are written as plain SQL and compiled into typed Go.
- **pgx** (v5) is the driver and connection pool.
- **goose:** migrations are plain SQL files, embedded in the binary and applied at startup (and through a CLI subcommand). This answers [Q-0032](../questions/README.md).
- Applies to every Go service with a database: server and meta.

## Consequences

- Full Postgres power without an ORM in the way: FTS, `pg_trgm`, JSONB, CTEs, `COPY` for bulk loads (useful for metadata dumps).
- The schema lives in the migrations. Every change needs a new goose migration, and sqlc reads the migrations to type-check queries.
- No generated query builder: dynamic filters (e.g. meta's Browse) are composed in SQL with optional parameters, or with a small builder where that gets unreadable (session's call).
- Tests run against a real Postgres (testcontainers or a CI service), never a substitute.

## Alternatives considered

| Option | Why not |
|---|---|
| ent + Atlas (ADR-0018) | Its multi-dialect advantage no longer applies; Postgres features go through escape hatches |
| ent + goose | Two tools for one schema; still ORM-shaped |
| bun / GORM | Query builders or reflection without sqlc's compile-time checks |
