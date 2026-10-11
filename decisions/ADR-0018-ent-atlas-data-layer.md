---
title: "ADR-0018: ent + Atlas versioned migrations as the Go data layer"
status: superseded
tags: [database, go]
related: [decisions/ADR-0004-database-portability.md, modules/server/overview.md, modules/meta/overview.md]
inputs: [IN-0003, IN-0009]
updated: 2026-10-11
---

# ADR-0018: ent + Atlas

- **Date:** 2026-10-11 · **Deciders:** @aurimasniekis (proposed by the keeper; accepted in IN-0009 §2, answering [Q-0001](../questions/README.md))
- **Superseded by:** [ADR-0023](ADR-0023-sqlc-pgx-goose-data-layer.md) on 2026-10-11, the same day: Postgres became the only database (ADR-0022), which removed ent's multi-dialect advantage (IN-0009 §5).

## Decision
- **ent** (schema-as-Go-code, typed client, supports SQLite/Postgres/MySQL), with **Atlas versioned migrations** generated per dialect.
- SQLite via pure-Go `modernc.org/sqlite`, so there is no cgo and cross-compiling is easy.
- Applies to every Go service with a database: server and meta.
- **Applying migrations at runtime** is open ([Q-0032](../questions/README.md)). The owner floated goose ("maybe migrations too like goose or etc?", IN-0009 §3). *Suggestion:* Atlas generates the versioned files in goose format at dev time, and the service applies them with goose, embedded at startup. Then no Atlas binary ships in the image. Atlas's goose output format is **[unverified]**.

## Alternatives considered
| Option | Why not (yet) |
|---|---|
| sqlc + goose | Best raw SQL ergonomics, but needs separate query files per dialect, which is about 3× upkeep |
| bun | Good multi-dialect query builder; less schema/migration tooling than ent+Atlas |
| GORM | Runtime reflection, weaker typing, migration drift |
