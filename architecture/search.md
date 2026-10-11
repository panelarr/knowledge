---
title: Search
status: proposed
tags: [architecture, search]
related: [decisions/ADR-0010-optional-search-engine.md, decisions/ADR-0017-search-interface-builtin-default.md, research/search-engines.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# Search

## Summary

Search goes through a **`SearchIndex` interface**. The default backend is the **database's own full-text search**, with no extra container. Hosters may add **Typesense** (first adapter) or **Meilisearch** for typo tolerance, facets and better multilingual search. This applies to **both server and meta**, each configured on its own (IN-0017) ([ADR-0010](../decisions/ADR-0010-optional-search-engine.md) accepted; [ADR-0017](../decisions/ADR-0017-search-interface-builtin-default.md) proposed). The DB stays the source of truth.

## What is searched

| Field | Source | Weight (initial guess) |
|---|---|---|
| All titles: primary, native, romanized, alternates per language | Work, MetaLink (MangaBaka `titles[]`), SourceSeries titles | highest |
| Authors, artists, publishers | meta, sources, ComicInfo | high |
| Characters (where available) | metadata plugins (AniList, ComicVine) ([Q-0023](../questions/README.md)) | medium |
| Tags, genres, type, status, year, content rating, original language | meta, sources | facets/filters |
| Description | meta, sources | low |
| Per user: in-library, category, read state | server | filters (applied by server, never stored per user in the engine) |

## Where search happens
- **Library and Work search** (server): searches Works the instance knows, scoped by user visibility.
- **Metadata search** (meta): searches the MangaBaka dump and other metadata. Used by matching and "add by metadata".
- **Source search** stays live at the source plugin (`Search` RPC), since sources are remote catalogues. Results may be cached.

## Interface (sketch)
```go
type SearchIndex interface {
    Upsert(ctx context.Context, docs ...Doc) error
    Delete(ctx context.Context, ids ...string) error
    Query(ctx context.Context, q Query) (Result, error) // text, filters, facets, sort, page
    Rebuild(ctx context.Context, src DocSource) error   // full re-index job
    Capabilities() Caps                                // typo tolerance, facets, CJK...
}
```

## Backends
1. **Built-in:** Postgres `tsvector` + **`pg_trgm`** similarity (trigrams also cover CJK substrings). Postgres is the only database ([ADR-0022](../decisions/ADR-0022-postgresql-only.md)).
2. **Typesense:** a collection per doc type, typo tolerance, facets, synonyms (e.g. romanization variants).
3. **Meilisearch:** a candidate; strong CJK tokenization.
   - **OpenSearch / Algolia:** "maybe" for meta (IN-0017). Not planned: ADR-0010 rules out OpenSearch-class engines, and Algolia is hosted SaaS ([Q-0033](../questions/README.md)).
4. **Bleve** (embedded): evaluate ([Q-0022](../questions/README.md)).

## Operations
- Index updates ride the job queue (debounced). Switching backend or changing the schema starts a **full rebuild** job.
- *Admin → Search* shows the backend, document count, last rebuild and a "test query" box.
