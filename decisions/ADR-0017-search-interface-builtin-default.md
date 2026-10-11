---
title: "ADR-0017: Search behind an interface; built-in DB full-text by default, Typesense adapter first"
status: proposed
tags: [search]
related: [architecture/search.md, research/search-engines.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# ADR-0017: Search interface and backends

- **Date:** 2026-10-11 · **Deciders:** author (proposed)

## Decision (proposed)
- server and meta use a `SearchIndex` interface. **The DB is the source of truth**; the index is rebuildable.
- **Default backend:** PostgreSQL's own full-text (`tsvector` + `pg_trgm`; Postgres is the only database since [ADR-0022](ADR-0022-postgresql-only.md)). No extra container.
- **First external adapter: Typesense** (the author's suggestion). **Meilisearch** is the candidate second adapter (strong CJK).
- *Update (IN-0017, IN-0018):* the optional engine integrations belong to **meta**; the library (server) uses the built-in Postgres search. OpenSearch/Algolia: [Q-0033](../questions/README.md).
- **Bleve** (embedded) is to be evaluated ([Q-0022](../questions/README.md)).
- Switching backend triggers a background full re-index job.
