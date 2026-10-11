---
title: meta overview
status: proposed
tags: [module, meta, metadata, go]
related: [contracts/metadata-plugin.md, research/mangabaka.md, research/metadata-providers.md, architecture/search.md]
inputs: [IN-0002, IN-0003]
updated: 2026-10-11
---

# meta

## Summary

An optional Go **metadata service**. It hosts **metadata plugins**, aggregates their records into a local DB, cross-references external IDs, **matches** source series to metadata, and provides metadata search. It runs standalone (`panelarr/meta`, usable by other projects) or embedded in server (default still open, [Q-0006](../../questions/README.md)). With meta absent, server falls back to source-provided metadata.

## Metadata plugins (none bundled, [ADR-0009](../../decisions/ADR-0009-plugins-not-bundled.md))
| Plugin | Mode | Notes |
|---|---|---|
| `meta-mangabaka` | `BulkSync` from the nightly dump (SQLite/JSONL, zstd) + API for freshness | Backbone and ID cross-reference. CC BY-NC-SA: hoster-downloaded, attributed ([research](../../research/mangabaka.md)) |
| `meta-anilist` | GraphQL search/get | Characters, staff, relations |
| `meta-mal`, `meta-mangaupdates`, `meta-kitsu` | API search/get | |
| `meta-mangadex` | API | Not in MangaBaka's ID map |
| `meta-comicvine` | API key | Western comics |

## Internals
- **Store:** its own DB (SQLite/Postgres/MySQL, as [ADR-0004](../../decisions/ADR-0004-database-portability.md)). Tables: works, titles, people, tags, characters, external_ids, provider_records (raw JSON), merges.
- **Sync scheduler:** dump imports on the hoster's schedule; incremental diff by provider ID; merge redirects.
- **Matcher:**
  - normalize titles (case, punctuation, width, romanization variants), compare against every title and language;
  - add an author overlap score, year proximity and type;
  - external IDs from sources (where given) short-circuit matching;
  - output candidates with a confidence score. server auto-links above a threshold, otherwise asks a curator.
- **Search:** the same `SearchIndex` abstraction as server ([search](../../architecture/search.md)).
- **Rate limits:** each plugin declares its limits and meta enforces them.

## Implementation status
Not started (M3).
