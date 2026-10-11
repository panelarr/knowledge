---
title: Metadata plugin contract and meta API
status: draft
tags: [contract, metadata]
related: [modules/meta/overview.md, modules/meta-mangabaka/overview.md, architecture/plugins.md, research/mangabaka.md, research/metadata-providers.md]
inputs: [IN-0002, IN-0003, IN-0007, IN-0009]
updated: 2026-10-11
---

# Metadata plugin contract (`panelarr.metadata.v1`) and meta API (`panelarr.meta.v1`)

## Summary

- **Metadata plugins** (MangaBaka, AniList, …) feed **meta**. Each one says which **ingestion types** it supports: API lookups, scraping, dump downloads and more (IN-0009 §1).
- **meta** stores their records in its own DB, cross-references external IDs and serves them. It is the **Seerr-style** part of Panelarr: browsing, search and details over the whole metadata catalogue, not only the library (IN-0009 §2). Matching source series to metadata and external search engines come later.
- **Public home:** the protos and the Go SDK live in the `meta` repo; each plugin has its own repo, e.g. `meta-mangabaka` (Q-0017, IN-0009 §2).

## Ingestion types (draft)

The owner listed "API/Scrape/Dump downloads and etc" (IN-0009 §1). The keeper's first cut, for the meta session to refine:

| Type | What the plugin does | Who triggers it | Example |
|---|---|---|---|
| `lookup` | On-demand `Search` / `Get` through a provider API | meta, on a user action or a stale record; rate-limited | MangaBaka API, AniList GraphQL |
| `scrape` | On-demand `Search` / `Get` by fetching and parsing pages | same as `lookup`; uses the main app's common services (network profiles, solvers, IN-0007) | providers without an API |
| `dump` | Download a full snapshot file, verify it, read it and stream every record | meta, on the hoster's schedule or a manual run | MangaBaka SQLite dump |
| `delta` | Stream only the changes since a cursor | meta, more often than dumps | "updated since" API endpoints |

- A plugin declares in `GetInfo` the types it supports, its limits per type, and the common services it can use. The list is open, so new types can be added without breaking v1.
- Provider specifics stay in the plugin: URLs, auth, checksums, decompression and file formats. meta only sees normalized records.

## Metadata plugin sketch
```proto
service MetadataPlugin {
  rpc GetInfo(Empty) returns (PluginInfo);            // id, version, ingestion types + limits, capabilities (characters, people, …), common services it can use
  rpc Search(MetaSearchRequest) returns (MetaSeriesList); // lookup / scrape
  rpc Get(ExternalRef) returns (MetaSeries);           // lookup / scrape: normalized record + raw extras
  rpc Sync(SyncRequest) returns (stream SyncEvent);    // dump / delta: mode, optional cursor
  rpc GetSettingsSchema(Empty) returns (SettingsSchema); // what config it expects (IN-0007)
  rpc GetSettings(Empty) returns (Settings);
  rpc SetSettings(Settings) returns (Settings);
  rpc Health(Empty) returns (HealthStatus);
}

message SyncEvent {
  oneof event {
    SyncStarted started = 1;   // snapshot id/date, expected record count if known
    MetaSeries upsert = 2;     // a normalized record
    ExternalRef removed = 3;   // gone from the provider
    Merge merge = 4;           // provider merged id A into id B (MangaBaka merged_with)
    Checkpoint checkpoint = 5; // cursor; meta commits everything before it
    SyncFinished finished = 6; // totals; the cursor to use for the next delta
  }
}
```

## meta service sketch (consumed by server and web)
```proto
service Meta {
  rpc Browse(BrowseRequest) returns (WorkPage);                // Seerr-style discovery: filters (genre, tag, type, status, year, content rating, language) + sort (popularity, rating, updated, year)
  rpc Search(SearchRequest) returns (SearchResponse);          // titles in every language and alt title, people
  rpc Get(MetaId) returns (Work);                              // details: titles, people, description, covers (+blurhash), tags, status, relations, links, attribution
  rpc LookupExternal(ExternalRef) returns (Work);              // e.g. anilist:30013 → meta work
  rpc Match(MatchRequest) returns (MatchResponse);             // later: titles, authors, year, lang, source hints → candidates + confidence
}

service MetaAdmin {
  rpc ListProviders(Empty) returns (ProviderList);             // plugins, ingestion types, health, last sync
  rpc RunSync(RunSyncRequest) returns (SyncRun);               // manual dump/delta run
  rpc ListSyncRuns(ListSyncRunsRequest) returns (SyncRunList); // status, counts, errors, cursor
}
```

## Design notes
- **Normalized record:** titles[] (lang, kind, primary), people[] (role), description(s), genres/tags (with spoiler/explicit flags), status, year, type, content rating, covers (+ blurhash), external IDs map, characters[] (optional), relations, links.
- **Merges:** honour MangaBaka `merged_with`. meta keeps redirects so old IDs still resolve.
- **Snapshots:** after a full `dump` sync, records the provider no longer has are marked removed, not deleted, so links keep working.
- **Attribution:** every record carries provider attribution, and web shows it. Licences such as MangaBaka's CC BY-NC-SA mean the hoster downloads the data; Panelarr never ships it ([scope](../product/scope.md)).
- **Library flags** ("in my library") come from server, not meta. meta knows nothing about users.
