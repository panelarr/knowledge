---
title: Source plugin contract (panelarr.source.v1)
status: draft
tags: [contract, sources, grpc]
related: [architecture/contracts-and-transport.md, architecture/plugins.md, modules/source-api/overview.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# Source plugin contract (`panelarr.source.v1`)

## Summary

Every source plugin implements this: Mihon (via mihon-source and/or source-mihon), local files and future kinds. Its shape follows the Mihon source API (popular, latest, search with filters, details, chapters, pages) because that model has proven itself across thousands of sources, generalised so non-Mihon sources fit. **Public home:** `source-api/proto/panelarr/source/v1/` ([ADR-0012](../decisions/ADR-0012-protobuf-grpc-contracts.md)).

## Service sketch
```proto
service SourcePlugin {
  rpc GetInfo(GetInfoRequest) returns (PluginInfo);             // id, version, contract versions, capabilities, limits, common services it can use (IN-0007)
  rpc ListSources(ListSourcesRequest) returns (ListSourcesResponse); // id, name, lang, content_rating, icon, capabilities
  rpc GetFilters(SourceRef) returns (FilterList);                // typed filters (text, select, tri-state, sort, group)
  rpc Popular(PageRequest) returns (SeriesPage);
  rpc Latest(PageRequest) returns (SeriesPage);
  rpc Search(SearchRequest) returns (SeriesPage);                // query + filter values + page
  rpc ResolveUrl(ResolveUrlRequest) returns (SeriesRef);         // optional: paste a URL → series
  rpc GetSeries(SeriesRef) returns (Series);                     // title, alt titles, authors, artists, description, genres, status, cover, url
  rpc ListChapters(SeriesRef) returns (ChapterList);             // key, name, number, volume, scanlator, uploaded_at, lang
  rpc ListPages(ChapterRef) returns (PageList);                  // ordered page refs (opaque) + optional direct urls
  rpc FetchImage(ImageRef) returns (stream Chunk);               // bytes via the source's network profile
  rpc GetSettingsSchema(SourceRef) returns (SettingsSchema);     // JSON Schema (Mihon prefs map here)
  rpc GetSettings(SourceRef) returns (Settings);
  rpc SetSettings(SetSettingsRequest) returns (Settings);
  rpc SetNetworkProfile(SetNetworkProfileRequest) returns (Empty); // pushed by host, see networking
  rpc Health(Empty) returns (HealthStatus);
}
```

## As built (in mihon-source, until source-api exists)
- `SourcePluginService` (buf STANDARD naming, Request/Response per RPC) with every RPC above plus `GetSource`.
- `PluginInfo` carries `config_schema` (JSON Schema as a Struct) and `common_services` (`NETWORK_PROFILE`, `SOLVER`) per Q-0026/Q-0030, plus contracts, capabilities and limits.
- `ResolveUrlResponse.best_effort`: plugins may resolve pasted URLs by searching sources without a native resolver and flag the answer as best effort (mihon-source, GOAL-0005).
- Search filter values are sparse `FilterValue{path, value}` keyed by **position**, because Mihon filters have no stable keys.
- `Source.health` (`SourceHealth`: OK / FAILING + reason, latency, checked_at, checks_disabled) from mihon-source's self-check (ADR-0027, GOAL-0005).
- `FetchImage` streams metadata first, then chunks. `ErrorReason` enum; `google.rpc.ErrorInfo.reason` carries the name without the prefix.

## Design notes
- **Keys are opaque strings** chosen by the plugin (for Mihon, the extension's relative URL). The host never parses them.
- **Source IDs** are namespaced by the host as `plugin:sourceId`. Mihon IDs are stable MD5-derived longs, carried as strings.
- **Filters** use a typed union that maps Mihon `FilterList` (Header, Separator, Text, CheckBox, TriState, Select, Sort, Group) 1:1. web renders it generically.
- **Capabilities** let sources skip features: `latest`, `search`, `filters`, `resolve_url`, `settings`, `needs_webview`, `nsfw`.
- **Errors:** gRPC status + `ErrorInfo.reason` ∈ {`CLOUDFLARE_CHALLENGE`, `RATE_LIMITED` (+ retry_after), `SOURCE_DOWN`, `NOT_FOUND`, `LOGIN_REQUIRED`, `UNSUPPORTED`}.
- **Network profile push:** the host owns profiles ([networking](../architecture/networking.md)), and plugins apply them per source.
- **Local sources** (source-local) implement the same contract. `FetchImage` reads from archives.
- **Conformance suite** (in source-api): runs any endpoint through list → popular → details → chapters → pages → image, checking schema and error mapping.
