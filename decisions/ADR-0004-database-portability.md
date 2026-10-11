---
title: "ADR-0004: Support SQLite, PostgreSQL and MySQL/MariaDB"
status: accepted
tags: [database, server]
related: [modules/server/overview.md, decisions/ADR-0018-ent-atlas-data-layer.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# ADR-0004: SQLite, PostgreSQL and MySQL/MariaDB

- **Date:** 2026-10-11 · **Deciders:** author

## Context
The author wants a choice of databases: "sqlite/postgres/mysql (optional but if possible and not too difficult)" (IN-0003 §1).

## Decision
- **SQLite** is the zero-config default.
- **PostgreSQL** is supported.
- **MySQL/MariaDB** is supported if the cost stays reasonable. It can be dropped after a cost review ([Q-0011](../questions/README.md)).
- Applies to every Go service with persistent state (server, meta).

## Consequences
- SQL has to stay portable, with migrations per dialect. The proposed data layer is [ADR-0018](ADR-0018-ent-atlas-data-layer.md).
- Full-text search differs per DB and is hidden behind the search interface ([ADR-0017](ADR-0017-search-interface-builtin-default.md)).
- CI runs the test suite against all supported dialects.
