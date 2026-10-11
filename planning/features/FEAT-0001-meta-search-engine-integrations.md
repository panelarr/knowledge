---
title: "FEAT-0001: meta search engine integrations"
status: accepted
tags: [feature, meta, search]
related: [modules/meta/search-engines.md, research/search-engines.md, architecture/search.md, decisions/ADR-0010-optional-search-engine.md, decisions/ADR-0017-search-interface-builtin-default.md]
inputs: [IN-0003, IN-0017, IN-0018, IN-0021, IN-0025]
milestone: "M3"
priority: P2
updated: 2026-10-11
---

# FEAT-0001: meta search engine integrations

## Problem

The owner wants meta to have "optional configurable search engine integrations like typesense/meilisearch/(opensearch/algolia maybe)" (IN-0017). These are for meta, not the library (IN-0018). The owner asked to start scoping and designing them (IN-0021). Postgres search (trigram + full text) works, but it has no facet counts, weaker typo tolerance and ranking, and no per-language tokenization for Japanese, Chinese and Korean.

## Outcome

A hoster who wants better catalogue search adds a Typesense or Meilisearch container, points meta at it in config or the admin UI, and gets typo-tolerant, multilingual search with facet counts. meta keeps working unchanged without one, and falls back to Postgres if the engine is down.

## Scope

- **In:**
  - an engine adapter behind meta's existing `search.Index`;
  - a reliable change feed from Postgres to the engine;
  - full rebuild with an atomic swap;
  - **Typesense** first (the owner's pick, ADR-0017), then **Meilisearch**;
  - facet counts in Browse/Search;
  - fallback to Postgres;
  - config, health and an admin view (rides on GOAL-0003's integrations page);
  - compose profiles.
- **Out:**
  - the library's search (server stays on Postgres, IN-0018);
  - OpenSearch and Algolia until [Q-0033](../../questions/README.md) is settled (ADR-0010 says lightweight only; Algolia sends data off-instance);
  - Postgres-extension backends (PGroonga, ParadeDB), which need a superuser ([Q-0037](../../questions/README.md));
  - vector/hybrid search (a later idea, possibly shared with GOAL-0004's duplicate candidates);
  - characters (Q-0023).

## Acceptance criteria

- [ ] **AC1, opt-in:** With `search.backend: postgres` (the default) and no engine configured, meta behaves exactly as today. No engine container is required anywhere.
- [ ] **AC2, select:** With `search.backend: typesense` and a reachable Typesense, `Search` and `Browse` answers come from Typesense and return the same entry IDs and order rules (filters, sorts, paging) as Postgres for the shared conformance cases.
- [ ] **AC3, change feed:** Given an entry is created, changed, merged or removed by ingest, the engine reflects it within a configurable delay (default ≤ 30 s), without losing updates across a meta restart or an engine outage (at-least-once, idempotent).
- [ ] **AC4, rebuild:** A full rebuild builds a new index and swaps it in atomically; searches keep answering from the old index until the swap. A rebuild runs automatically on first use and when the document schema version changes.
- [ ] **AC5, fallback:** When the engine is unreachable or the index isn't ready, searches fall back to Postgres, health shows "degraded", and `/readyz` stays ready.
- [ ] **AC6, multilingual:** Japanese, Chinese and Korean titles are searchable by substring/prefix, romanized titles and typos ("naruro" finds "Naruto") are found, and people names match. The conformance cases from the Postgres search tests pass on each engine.
- [ ] **AC7, facets:** Browse and Search can return facet counts (genres, tags, type, status, content rating, original language) when the backend reports the `Facets` capability; Postgres reports none, and clients handle both.
- [ ] **AC8, Meilisearch:** the same as AC2–AC7 with `search.backend: meilisearch`; analytics off by default in the compose profile.
- [ ] **AC9, secrets and exposure:** The engine's API key is stored as a secret (never returned), meta uses its own key, and the engine is never exposed to browsers; all search goes through meta's API.
- [ ] **AC10, ops:** Compose profiles `search-typesense` and `search-meilisearch` in meta's example; the admin UI shows backend, document count, change-feed lag, last rebuild and a "Rebuild" button.

## Design notes

- Design: [modules/meta/search-engines.md](../../modules/meta/search-engines.md). Research: [search engines](../../research/search-engines.md).
- Decisions it rests on: [ADR-0010](../../decisions/ADR-0010-optional-search-engine.md) (optional, lightweight; accepted), [ADR-0017](../../decisions/ADR-0017-search-interface-builtin-default.md) (interface, Postgres default, Typesense first; proposed), [ADR-0022](../../decisions/ADR-0022-postgresql-only.md).

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| meta | [GOAL-0006](../../agents/goals/GOAL-0006-meta-search-engines-typesense-then-meilisearch.md) | — | queued after GOAL-0003, GOAL-0004 |

## Open questions

- [Q-0033](../../questions/README.md): OpenSearch/Algolia vs ADR-0010.
- [Q-0037](../../questions/README.md): Postgres-extension backends (PGroonga's romaji/kana prefix is attractive for Japanese).
- [Q-0022](../../questions/README.md): benchmark the engines on real data (CJK quality, RAM).
