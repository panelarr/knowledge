---
title: "GOAL-0006: meta search engines: Typesense then Meilisearch"
status: accepted
tags: [goal, agents, meta, search]
related: [planning/features/FEAT-0001-meta-search-engine-integrations.md, modules/meta/search-engines.md, research/search-engines.md, architecture/search.md]
inputs: [IN-0017, IN-0018, IN-0021, IN-0025]
repos: [meta]
session: "panelarr-meta"
features: [FEAT-0001]
updated: 2026-10-11
---

# GOAL-0006: meta search engines: Typesense then Meilisearch

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0006 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`accepted` (FEAT-0001 accepted by the owner, IN-0025). **Queued for `panelarr-meta` after GOAL-0003 and GOAL-0004**, unless the owner reorders.

## Context

- Code: `~/Projects/Panelarr/meta` · branches `<type>/<scope>-<slug>`
- **Read first:**
  1. **[FEAT-0001](../../planning/features/FEAT-0001-meta-search-engine-integrations.md): the acceptance criteria are the DoD.**
  2. [modules/meta/search-engines.md](../../modules/meta/search-engines.md): the design (outbox, rebuild swap, document shape, query mapping, fallback, config).
  3. [research/search-engines.md](../../research/search-engines.md): engine facts and limits.
  4. Your own `internal/search` and `internal/catalog`.
- ADRs: [ADR-0010](../../decisions/ADR-0010-optional-search-engine.md) (optional, lightweight; accepted), [ADR-0017](../../decisions/ADR-0017-search-interface-builtin-default.md) (proposed), [ADR-0022](../../decisions/ADR-0022-postgresql-only.md), [ADR-0027](../../decisions/ADR-0027-observability-baseline-for-every-service.md) (metrics for lag and backend). **meta only:** the library stays on Postgres (IN-0018).

## Objective

Implement FEAT-0001: optional Typesense, then Meilisearch, behind `search.Index`, with a reliable change feed, atomic rebuilds, facet counts, fallback to Postgres, config, an admin view (as an integration in the GOAL-0003 admin) and compose profiles. Postgres stays the default and the source of truth.

## Slices (suggested order)

1. **Change feed:** the `search_outbox` table written in the same transaction as every catalog write (rebuild, merge, retire, remove), only when a non-Postgres backend is configured. An indexer worker (claim with SKIP LOCKED, coalesce, bulk apply, back off, at-least-once). Lag metric. Tests: restart, outage, flood → rebuild.
2. **Adapter conformance suite:** extract today's Postgres search tests into a suite every backend must pass (romanized, Japanese substring, typo, person, filters, sorts, paging, merged excluded).
3. **Typesense:** document schema per the design (per-language title fields with locales, `infix` only on the CJK fields), bulk import, alias swap rebuild with a schema version, query mapping, facets, fallback. Thin REST client or `typesense-go` (say which). Compose profile `search-typesense`.
4. **Facets in the API:** an additive `facets` field in Browse/Search responses, filled when `Capabilities.Facets`; Browse stays on Postgres unless facets are requested (setting).
5. **Meilisearch:** the same via `localizedAttributes`, `swap-indexes`, `maxTotalHits` tuning, `MEILI_NO_ANALYTICS=true` in compose; MIT edition only.
6. **Admin and ops:** a search-engine section in the integrations UI (connection, test, document count, lag, last rebuild, Rebuild button; key stored as a secret). Metrics. Docs. Benchmarks on synthetic data at about 300k entries (RAM, index size, p50/p95, rebuild time) in the REPORT.

## When something isn't decided

- `ASK:` the keeper, then `PROPOSE:`. Open: [Q-0022](../../questions/README.md) (benchmarks), [Q-0033](../../questions/README.md) (OpenSearch/Algolia: out of scope), [Q-0037](../../questions/README.md) (Postgres extensions: out of scope).

## Constraints

- Same as GOAL-0003 (merge your own branches before the first release, never push; public repo; aliases; leak-check; ask before touching shared Docker state).
- Engines are always optional; nothing breaks or changes without one.

## Definition of Done

- [ ] FEAT-0001 AC1–AC10 met, each with test or doc evidence
- [ ] Conformance suite passes on Postgres, Typesense and Meilisearch
- [ ] Benchmarks reported; docs and compose profiles done; `make check` green; leak-check clean
- [ ] `DONE:` with evidence per AC

## History

- 2026-10-11: written from FEAT-0001 after the owner accepted it (IN-0025); queued after GOAL-0003 and GOAL-0004.
- 2026-10-11: owner approved GOAL-0004 and GOAL-0006 and kept the order: GOAL-0003 → GOAL-0004 → GOAL-0006 (IN-0026).
