---
title: Metadata plugin contract and meta API
status: draft
tags: [contract, metadata]
related: [modules/meta/overview.md, architecture/plugins.md, research/mangabaka.md]
inputs: [IN-0002, IN-0003]
updated: 2026-10-11
---

# Metadata plugin contract (`panelarr.metadata.v1`) and meta API (`panelarr.meta.v1`)

## Summary

- **Metadata plugins** (MangaBaka, AniList, …) feed **meta**.
- **meta** aggregates them, cross-references external IDs, matches series, and serves server.
- **Public home:** the `meta` repo.

## Metadata plugin sketch
```proto
service MetadataPlugin {
  rpc GetInfo(Empty) returns (PluginInfo);            // capabilities: search, get, bulk_sync (dump), characters, people
  rpc Search(MetaSearchRequest) returns (MetaSeriesList);
  rpc Get(ExternalRef) returns (MetaSeries);           // normalized record + raw extras
  rpc BulkSync(BulkSyncRequest) returns (stream MetaSeries); // dump-style providers (MangaBaka) stream everything / changes since
  rpc GetSettingsSchema(Empty) returns (SettingsSchema);
  rpc Health(Empty) returns (HealthStatus);
}
```

## meta service sketch (consumed by server)
```proto
service Meta {
  rpc Search(SearchRequest) returns (SearchResponse);          // across aggregated metadata
  rpc Get(MetaId) returns (Work);
  rpc LookupExternal(ExternalRef) returns (Work);              // e.g. anilist:30013 → meta work
  rpc Match(MatchRequest) returns (MatchResponse);             // titles, authors, year, lang, source hints → candidates + confidence
}
```

## Design notes
- **Normalized record:** titles[] (lang, kind, primary), people[] (role), description(s), genres/tags (with spoiler/explicit flags), status, year, type, content rating, covers (+ blurhash), external IDs map, characters[] (optional), relations.
- **Merges:** honour MangaBaka `merged_with`. meta keeps redirects so old IDs still resolve.
- **Attribution:** every record carries provider attribution, and web shows it.
