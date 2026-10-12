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

## As built (home: source-api since GOAL-0009; mihon-source vendors a pinned copy)
- `SourcePluginService` (buf STANDARD naming, Request/Response per RPC) with every RPC above plus `GetSource`.
- `PluginInfo` carries `config_schema` (JSON Schema as a Struct) and `common_services` (`NETWORK_PROFILE`, `SOLVER`) per Q-0026/Q-0030, plus contracts, capabilities and limits.
- **Plugin-level config** (GOAL-0009 PROPOSE, accepted as a working assumption): `GetConfig` (`GET /v1/config`, values with `writeOnly` schema fields returned empty) and `SetConfig` (`PUT /v1/config`, validated against `PluginInfo.config_schema`, applied at runtime). The host calls SetConfig after start and on every admin save; the server re-sends the stored config when it starts and whenever a plugin comes back from down (server slice 3, working assumption). Plugins without a config schema answer UNIMPLEMENTED. Standalone plugins may also read the same config from `--config`/`PLUGIN_CONFIG` at start. Per-source `GetSettings`/`SetSettings` are unchanged. Additive.
- *Idea (later, additive):* optional `width`/`height` on `Page`, so readers can lay out double pages and long strips before images load (asked by web; the server would also read sizes from CBZs).
- `GetSeriesRequest.refresh` / `ListChaptersRequest.refresh` (HTTP `?refresh=true`): bypass a plugin's result cache and replace the cached result, e.g. to check for new chapters now (mihon-source `db067fc`). Not part of the cache key.
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

**Config schema property order (2026-10-12):** the schema travels as a protobuf `Struct` and the server's JSON sorts keys, so the declared order is lost. Web (`65fbfe2`) orders fields by `x-order` / `propertyOrder` when present, otherwise required fields first. The convention is a **per-property number** `x-order` (1, 2, …) at every depth. The source-api SDK stamps it from the declared order (`a3e91cd`; source-mihon `aa80905` pins its order); meta's plugin SDK does the same (`805d263`); mihon-source's per-source settings schemas add the per-property numbers next to their older object-level `x-order` array.

**Packages capability (GOAL-0012; in source.v1 since source-api `2ac5461`, 2026-10-12):** optional `PLUGIN_CAPABILITY_PACKAGES`; `ListPackages`, `GetPackage`, `InstallPackage`, `UpdatePackage`, `UninstallPackage`, `SetPackageSettings`; a `Package` lists its languages, versions, offers (per store) and sources (with lang and `available`); `PackageSettings.enabled_langs`; `Source.package_id`; install/update idempotent. Languages at plugin level (config) and package level both gate which sources `ListSources` returns. Package IDs never contain `:`. See [GOAL-0012](../agents/goals/GOAL-0012-source-plugins-extension-packages-and-languages.md).

**Icons (2026-10-12, server `470bf23`):** `Source.icon_url` and `Package.icon_url` are either a path relative to the plugin's own address (served over HTTP with the API's credentials) or an absolute http(s) URL. Hosts fetch them server-side, outside `FetchImage` (which is for covers and pages), and send credentials only to the plugin's own address.

**Restart detection and applied profile (2026-10-12, source-api `348bc2d`):** `HealthResponse.instance_id` changes on every plugin start (the SDK fills it); hosts re-push config and profiles when it changes. Optional `GetNetworkProfile(source_id)` returns the profile a plugin applies and its origin (PUSHED, PLUGIN, NONE), never a password. Per-source settings mark secrets `writeOnly`; they read back empty and an empty write keeps them.

**Image limits (2026-10-12, source-api `c9dbc17`, source-mihon `f709407`):** `Limits` gains `image_rate_limit` (pace for FetchImage only; unset = the plugin paces images itself and hosts add none) and `max_image_concurrency_per_source` (0 = none declared). The existing limits cover API calls only. source-mihon declares no image rate (extensions and the pushed profile pace images inside mihon-source) and an image concurrency of 4. From the reader fix (web `647cb99`): the host limit of 30 requests a minute made long chapters wait about 2 s per page. A pushed network profile's rate limit applies to all of a source's requests, images included.
