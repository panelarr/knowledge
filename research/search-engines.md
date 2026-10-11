---
title: Search engines for meta
status: draft
tags: [research, search, meta]
related: [architecture/search.md, modules/meta/search-engines.md, planning/features/FEAT-0001-meta-search-engine-integrations.md]
inputs: [IN-0003, IN-0017, IN-0021]
updated: 2026-10-11
---

# Search engines for meta

> Checked 2026-10-11. Versions and licences come from GitHub (repo metadata, releases, licence files); behaviour comes from official docs. **[unverified]** marks the rest. Benchmark before relying on numbers ([Q-0022](../questions/README.md)).

## Summary

meta searches about 300k active entries (MangaBaka scale, [research](mangabaka.md)), with very multilingual titles: Japanese, Chinese and Korean native titles, romanizations and English alternates. It searches people names and filters by tags, type, status, year and rating, sorted by popularity. The default stays **Postgres** (`pg_trgm` + `tsvector`, [ADR-0022](../decisions/ADR-0022-postgresql-only.md)). Engines are **optional add-ons for meta only**; the library uses Postgres (IN-0017, IN-0018).

**Best fits:**
- **Typesense:** owner's first pick, small RAM at this size, aliases for swaps.
- **Meilisearch:** best CJK out of the box, atomic index swap.
- **OpenSearch:** capable and fully open, but a heavy JVM service.
- **Algolia:** works only as a bring-your-own-account option.
- **Postgres extensions** (PGroonga, ParadeDB) keep everything in Postgres but need a superuser and a host-level install.

## Engines

### Typesense
- **v30.2** (2026-04), **GPL-3.0**. A separate process, so no licence impact on meta. [GitHub](https://github.com/typesense/typesense)
- Single binary or container. **Index in RAM** (docs: 2–3× the searchable fields; under ~1–2 GB for 500k small docs, **[unverified]** estimate). Raft clusters of 3 or 5 nodes for HA.
- **CJK:** per-field `locale` (ja/zh/ko). `infix: true` enables substring matching, at a significant memory cost. Japanese prefix behaviour without spaces is **[unverified]**.
- Typo tolerance (0–2), prefix on by default, per-field weights, `filter_by`, `facet_by` with counts, sort on up to 3 fields (`_text_match` + popularity). `string[]` fields, nested objects.
- Built-in auto-embedding (ONNX models or OpenAI-compatible) and hybrid search.
- JSONL bulk import with upsert. **Atomic reindex via collection aliases.**
- Go client `typesense-go` v3.2.0 (2025-03); the v4 module is alpha only, so the client lags the server. Calling the REST API directly is an option.

### Meilisearch
- **v1.54.3** (2026-10), **MIT AND BUSL-1.1**: Enterprise Edition files (sharding, replication since v1.37) need a commercial licence for production. Hosters stay on the MIT parts, which means no HA. [LICENSE](https://github.com/meilisearch/meilisearch/blob/main/LICENSE)
- Single binary or container, LMDB on disk. **Telemetry is collected unless disabled** (`--no-analytics` / `MEILI_NO_ANALYTICS`).
- **CJK:** Charabia tokenizer (jieba for Chinese, lindera with IPADIC for Japanese, lindera with ko-dic for Korean). `localizedAttributes` sets the locale per attribute pattern (e.g. `*_ja` → `jpn`).
- Typo tolerance, prefix, synonyms, ranking rules plus `popularity:desc`, facets (100 values per facet by default). **Limits:** only the first 10 query words are used; `maxTotalHits` defaults to 1000.
- Embedders (local, OpenAI, Ollama, REST) and hybrid search.
- **Atomic `swap-indexes`.** API keys scoped by action and index, plus tenant tokens.
- Go client `meilisearch-go` v0.36.3 (MIT), active, pre-1.0.

### OpenSearch
- **3.9.0** (2026-09), **Apache-2.0**, under the Linux Foundation since 2024-09.
- JVM service with an on-disk Lucene index. An initial admin password is required. **Japanese needs the kuromoji plugin**; ICU, nori and smartcn are also plugins **[unverified]**.
- Fuzzy queries, synonyms, `function_score`/`rank_feature` for popularity, aggregations for facets, k-NN/hybrid. **Aliases** for atomic swaps. Go client `opensearch-go/v5`.
- [ADR-0010](../decisions/ADR-0010-optional-search-engine.md) rules out OpenSearch-class engines, so it can only come in if the owner revises that ([Q-0033](../questions/README.md)).

### Algolia
- Proprietary hosted SaaS: the catalogue leaves the instance, with usage costs. Languages are set per index or query, not per field. Japanese needs `ja` in both `indexLanguages` and `queryLanguages`.
- Typo tolerance, custom ranking, facets, secured API keys. `ReplaceAllObjects` swaps via a temp index (record count doubles while it runs). Go client v4 (MIT).

### Postgres extensions (stay inside Postgres)
- **PGroonga 4.1.0** (2026-10, PostgreSQL licence):
  - strong all-language full-text search;
  - a **romaji/kana prefix operator** (`&^~`), notable for Japanese title search;
  - facets via SQL.
  - Needs a **superuser and the Groonga library** on the host. Some managed hosts (e.g. Supabase) offer it.
- **ParadeDB pg_search 0.26.1** (2026-10, **AGPL-3.0**):
  - Tantivy BM25 with lindera CJK tokenizers.
  - Needs `shared_preload_libraries`, a restart, effectively a **superuser**, and pgvector.
- **Both conflict with meta's "no superuser" design**, so they could only ever be explicit opt-in backends.

### Others
| Engine | Facts | Fit |
|---|---|---|
| Manticore 29.9 (GPL-3.0) | Japanese/Korean only as 1-gram n-grams; fuzzy needs a sidecar | Weak for this catalogue |
| Elasticsearch 9.5 (AGPL/SSPL/ELv2) | Like OpenSearch, with paid ML features **[unverified]** | OpenSearch is the cleaner pick |
| Bleve v2.6 (Apache-2.0, Go library) | Embedded; CJK bigram only; vectors need cgo; single process | Maybe a small-instance fallback |
| Quickwit / Tantivy | Built for append-only logs; no Go binding | Not suitable |

## Comparison

| Engine | Licence | Deploy | Memory | Japanese | Typo | Facets | Vectors | Go client | Atomic swap |
|---|---|---|---|---|---|---|---|---|---|
| Postgres (default) | PostgreSQL | built in | in DB | trigram substring | trigram | SQL | pgvector | pgx | in transaction |
| Typesense | GPL-3.0 | 1 binary | all in RAM | per-field locale | yes | yes | built-in | v3 stable / v4 alpha | aliases |
| Meilisearch | MIT + BUSL (EE) | 1 binary | disk | lindera, per attribute | yes | yes | built-in | v0.36 | swap-indexes |
| OpenSearch | Apache-2.0 | JVM | heap + disk | kuromoji plugin | fuzzy | aggregations | k-NN | v5 | aliases |
| Algolia | proprietary | SaaS | n/a | per index | yes | yes | paid **[unverified]** | v4 | temp index |
| PGroonga | PostgreSQL | PG extension, superuser | in DB | strong + romaji | similar | SQL | no | SQL | in transaction |

## Sources
- https://github.com/typesense/typesense · https://typesense.org/docs/guide/system-requirements.html · https://typesense.org/docs/30.1/api/collections.html · https://typesense.org/docs/30.1/api/search.html
- https://github.com/meilisearch/meilisearch/blob/main/LICENSE · https://www.meilisearch.com/docs/learn/resources/language · https://www.meilisearch.com/docs/learn/resources/known_limitations · https://www.meilisearch.com/docs/reference/api/indexes/swap-indexes · https://www.meilisearch.com/docs/learn/resources/telemetry
- https://github.com/opensearch-project/OpenSearch · https://docs.opensearch.org/latest/analyzers/tokenizers/kuromoji/
- https://www.algolia.com/doc/api-reference/api-methods/replace-all-objects
- https://pgroonga.github.io/reference/ · https://www.paradedb.com/docs/deploy/self-hosted/extension
- https://manual.manticoresearch.com/Creating_a_table/NLP_and_tokenization/Languages_with_continuous_scripts · https://github.com/blevesearch/bleve
