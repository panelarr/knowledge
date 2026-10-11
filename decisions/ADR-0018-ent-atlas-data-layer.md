---
title: "ADR-0018: ent + Atlas versioned migrations as the Go data layer"
status: proposed
tags: [database, go]
related: [decisions/ADR-0004-database-portability.md, modules/server/overview.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# ADR-0018: ent + Atlas

- **Date:** 2026-10-11 · **Deciders:** author (proposed; [Q-0001](../questions/README.md))

## Decision (proposed)
- **ent** (schema-as-Go-code, typed client, supports SQLite/Postgres/MySQL), with **Atlas versioned migrations** generated per dialect.
- SQLite via pure-Go `modernc.org/sqlite`, so there is no cgo and cross-compiling is easy.

## Alternatives considered
| Option | Why not (yet) |
|---|---|
| sqlc + goose | Best raw SQL ergonomics, but needs separate query files per dialect, which is about 3× upkeep |
| bun | Good multi-dialect query builder; less schema/migration tooling than ent+Atlas |
| GORM | Runtime reflection, weaker typing, migration drift |
