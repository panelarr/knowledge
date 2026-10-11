---
title: meta overview
status: proposed
tags: [module, meta, metadata, go]
related: [contracts/metadata-plugin.md, contracts/metadata-schema.md, modules/meta-mangabaka/overview.md, research/mangabaka.md, research/metadata-providers.md, architecture/search.md, decisions/ADR-0022-postgresql-only.md, decisions/ADR-0023-sqlc-pgx-goose-data-layer.md]
inputs: [IN-0002, IN-0003, IN-0009, IN-0010, IN-0015, IN-0017]
updated: 2026-10-11
---

# meta

## Summary

An optional Go **metadata service**, the **Seerr-style** part of Panelarr: it provides metadata information, browsing and search to the library and the rest of the app (IN-0009 §2). It hosts **metadata plugins**, ingests their records into its own Postgres DB, cross-references external IDs, merges providers into one **Entry** per item ([schema](../../contracts/metadata-schema.md)), and serves **Browse / Search / Get** over the whole catalogue, not only what is in a library. Later: matching source series to metadata, and external search engines. It is a **standalone service** (`panelarr/meta`, its own container, port 8901, usable by other projects) that **integrates with the library** through its API (Q-0006, IN-0015). With meta absent, server falls back to source-provided metadata.

## Repos
- **`meta`**: the `panelarr.metadata.v1` and `panelarr.meta.v1` protos, the Go plugin SDK (`plugin.Serve`, managed via go-plugin or standalone `--listen`), the meta service.
- **One repo per plugin** (Q-0017, IN-0009 §2): [`meta-mangabaka`](../meta-mangabaka/overview.md) first, later `meta-anilist`, …

## Ingestion types
Plugins declare which they support: `lookup` (API), `scrape`, `dump` (snapshot download), `delta` (changes since a cursor). The list stays open ([contract](../../contracts/metadata-plugin.md), IN-0009 §1).

## Metadata plugins (none bundled, [ADR-0009](../../decisions/ADR-0009-plugins-not-bundled.md))
| Plugin | Ingestion | Notes |
|---|---|---|
| `meta-mangabaka` | `dump` from the nightly SQLite dump (zstd) + `lookup` via the API for freshness | Backbone and ID cross-reference. CC BY-NC-SA: hoster-downloaded, attributed ([research](../../research/mangabaka.md)) |
| `meta-anilist` | `lookup` (GraphQL) | Characters, staff, relations |
| `meta-mal`, `meta-mangaupdates`, `meta-kitsu` | `lookup` | |
| `meta-mangadex` | `lookup` | Not in MangaBaka's ID map |
| `meta-comicvine` | `lookup` (API key) | Western comics |

## Internals
- **Store:** PostgreSQL ([ADR-0022](../../decisions/ADR-0022-postgresql-only.md)), its **own database**, configured by its own DSN. In the production setup it shares one Postgres server with server's library database (IN-0012); dev doesn't matter (IN-0013) with sqlc + pgx + goose ([ADR-0023](../../decisions/ADR-0023-sqlc-pgx-goose-data-layer.md)). Shaped by the [entry schema](../../contracts/metadata-schema.md): provider_entries (as received, raw JSONB), entries (merged view) with titles, descriptions, credits, company credits, tag assignments, relations, adaptations, items, images, links, external IDs; shared persons, companies and tags; field locks; merges/redirects; sync_runs.
- **Ingest:** consumes a plugin's `Sync` stream; upserts in batches, committing at each checkpoint; applies merges as redirects; after a full dump, marks unseen records removed; records each sync run (counts, errors, cursor). Bulk loads may use `COPY` into staging tables.
- **Sync scheduler:** dump and delta runs on the hoster's schedule, plus manual runs from `MetaAdmin`.
- **API:** `Browse` (filters + sort, Seerr-style discovery), `Search`, `Get`, `LookupExternal`; gRPC + HTTP/JSON + OpenAPI. Every record carries attribution.
- **Search:** Postgres FTS + `pg_trgm` by default, behind the `SearchIndex` interface. **Optional, configurable search engine integrations**, a meta feature, not the library's (IN-0017, IN-0018): **Typesense** and **Meilisearch** planned; **OpenSearch** and **Algolia** maybe ([Q-0033](../../questions/README.md): they conflict with ADR-0010 or send data off-instance). The hoster picks one in config; the DB stays the source of truth and the index can be rebuilt ([search](../../architecture/search.md)).
- **Matcher (later):**
  - normalize titles (case, punctuation, width, romanization variants), compare against every title and language;
  - add an author overlap score, year proximity and type;
  - external IDs from sources (where given) short-circuit matching;
  - output candidates with a confidence score. server auto-links above a threshold, otherwise asks a curator.
- **Rate limits:** each plugin declares its limits per ingestion type and meta enforces them.

## Implementation status
Not started. [GOAL-0002](../../agents/goals/GOAL-0002-meta-v0-metadata-protocol-meta-service-and-mangabaka-dump-in.md) is dispatched to `panelarr-meta` (2026-10-11). **Slice 1 (scaffold) merged** into `main` (`e7763e4`, not pushed). It was pulled forward from M3 to run alongside M1 (IN-0009).
