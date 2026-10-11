---
title: "ADR-0010: Optional, lightweight search engine chosen by the hoster"
status: accepted
tags: [search]
related: [architecture/search.md, decisions/ADR-0017-search-interface-builtin-default.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# ADR-0010: Optional search engine

- **Date:** 2026-10-11 · **Deciders:** author

## Context
"Some kind of proper search engine not opensearch but something lighter to search by different titles, descriptions, character info if available … something like typesense. also this should be optional and possible to configure" (IN-0003 §4).

## Decision
- Panelarr supports a dedicated **lightweight** search engine (Typesense-class; never OpenSearch or Elasticsearch).
- It indexes all titles, descriptions, people, tags, and characters where available.
- It is **optional**. The hoster decides whether to run it and configures it.

## Consequences
Without an engine there must still be decent search. The proposed shape is in [ADR-0017](ADR-0017-search-interface-builtin-default.md).
