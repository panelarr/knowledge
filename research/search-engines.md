---
title: Lightweight search engines
status: draft
tags: [research, search]
related: [architecture/search.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# Lightweight search engines

> Compiled 2026-10-11 from general knowledge; **[unverified]**. Benchmark before choosing ([Q-0022](../questions/README.md)).

## Summary

The author wants something lighter than OpenSearch, optional and chosen by the hoster ([ADR-0010](../decisions/ADR-0010-optional-search-engine.md)). The candidates fall into two groups: built-in database full-text (zero extra containers) and small dedicated engines.

| Option | Runs as | Strengths | Weaknesses |
|---|---|---|---|
| SQLite FTS5 | Inside SQLite | Zero ops; prefix queries; good enough for many libraries | No typo tolerance; CJK needs a trigram tokenizer |
| Postgres `tsvector` + `pg_trgm` | Inside Postgres | Trigram similarity gives fuzzy matches | Weak multilingual stemming for CJK |
| MySQL FULLTEXT (ngram parser) | Inside MySQL | Has an ngram parser for CJK | Least flexible |
| **Typesense** | Single C++ binary/container, in-RAM index | Typo tolerance, facets, synonyms, fast, simple API | Index must fit in RAM; separate service |
| **Meilisearch** | Single Rust binary/container | Typo tolerance, facets, **strong CJK tokenization (charabia)** | Separate service; on-disk index |
| Bleve (Go library) | Embedded in the Go process | No extra container; fuzzy queries | Slower; more code on our side; CJK analyzers limited |
| Manticore / ZincSearch | Container | Mature or light | Less fit / less momentum **[unverified]** |

## Notes for Panelarr
- Titles are very multilingual: Japanese, Korean and Chinese native titles plus romanizations. **CJK handling matters** when choosing an engine.
- Search should go through an interface. The DB stays the source of truth, and switching backend means a full re-index ([search architecture](../architecture/search.md)).
