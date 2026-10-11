---
title: Metadata plugin contract and meta API
status: draft
tags: [contract, metadata]
related: [contracts/metadata-schema.md, modules/meta/overview.md, modules/meta-mangabaka/overview.md, architecture/plugins.md, research/mangabaka.md, research/metadata-providers.md]
inputs: [IN-0002, IN-0003, IN-0007, IN-0009, IN-0010]
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
- Provider specifics stay in the plugin: URLs, auth, checksums, decompression and file formats. meta only sees records in the [entry schema](metadata-schema.md).

## Metadata plugin sketch
```proto
service MetadataPlugin {
  rpc GetInfo(Empty) returns (PluginInfo);            // id, version, ingestion types + limits, capabilities (characters, people, …), common services it can use
  rpc Search(MetaSearchRequest) returns (ProviderEntryList); // lookup / scrape
  rpc Get(ExternalRef) returns (ProviderEntry);         // lookup / scrape: schema record + raw original
  rpc Sync(SyncRequest) returns (stream SyncEvent);    // dump / delta: mode, optional cursor
  rpc GetSettingsSchema(Empty) returns (SettingsSchema); // what config it expects (IN-0007)
  rpc GetSettings(Empty) returns (Settings);
  rpc SetSettings(Settings) returns (Settings);
  rpc Health(Empty) returns (HealthStatus);
}

message SyncEvent {
  oneof event {
    SyncStarted started = 1;   // snapshot id/date, expected record count if known
    ProviderEntry upsert = 2;  // one record in the entry schema
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
  rpc Browse(BrowseRequest) returns (EntryPage);                // Seerr-style discovery: filters (genre, tag, type, status, year, content rating, language) + sort (popularity, rating, updated, year)
  rpc Search(SearchRequest) returns (SearchResponse);          // titles in every language and alt title, people
  rpc Get(EntryId) returns (Entry);                            // details: titles, people, description, covers (+blurhash), tags, status, relations, links, attribution
  rpc LookupExternal(ExternalRef) returns (Entry);             // e.g. anilist:30013 → meta entry
  rpc Match(MatchRequest) returns (MatchResponse);             // later: titles, authors, year, lang, source hints → candidates + confidence
}

service MetaAdmin {
  rpc ListProviders(Empty) returns (ProviderList);             // plugins, ingestion types, health, last sync
  rpc RunSync(RunSyncRequest) returns (SyncRun);               // manual dump/delta run
  rpc ListSyncRuns(ListSyncRunsRequest) returns (SyncRunList); // status, counts, errors, cursor
}
```

## As built (meta slice 2, `d9e0aed`)
- **Names** follow buf STANDARD: `MetadataPluginService`, `MetaService`, `MetaAdminService`; `Sync` returns `stream SyncResponse` (a oneof of events); meta's `Get` is `GetEntry`. `Match` is left out until matching starts.
- **Ingestion kind is an open string**, not an enum, so new kinds never break hosts. `GetInfo` declares id, provider key, protocols, `ingestions[]` (kind, per-operation rate limits, max concurrency, schedule hint, full snapshot), open-string `capabilities[]` (e.g. `lookup_by_external_id`), `common_services[]` (name, required, purpose) and a default attribution.
- **Sync events:** started (snapshot id/time, expected count, full snapshot, `unchanged`), upsert, removed, merge, checkpoint (cursor, count), finished (totals, next cursor), plus **notice** (level, message, ref) and **progress** (phase, done/total, unit). `SyncRequest.force` re-sends an unchanged dump.
- **meta API:** `Browse`, `Search`, `GetEntry`, `LookupExternal`, `ListTags`; admin `ListProviders`, `RunSync`, `ListSyncRuns`, `GetSyncRun`, `RefreshEntry`. REST: `GET /v1/entries`, `/v1/search`, `/v1/entries/{id}`, `/v1/lookup/{provider}/{external_id}`, `/v1/tags`, `/v1/admin/…`.
- **Transport:** ConnectRPC (gRPC, gRPC-Web, Connect) for standalone plugins and meta's API; grpc-go for managed plugins (go-plugin needs it); REST via vanguard transcoding planned. Decided in [ADR-0026](../decisions/ADR-0026-connectrpc-on-go-grpc-as-the-plugin-wire.md): gRPC is the canonical wire.

## Design notes
- **Record shape:** the [entry schema](metadata-schema.md) (IN-0010). Plugins send `ProviderEntry`s; meta stores them as received and builds merged `Entry`s with per-field provider priority and manual locks.
- **Merges:** honour MangaBaka `merged_with`. meta keeps redirects so old IDs still resolve.
- **Snapshots:** after a full `dump` sync, records the provider no longer has are marked removed, not deleted, so links keep working.
- **Attribution:** every record carries provider attribution, and web shows it. Licences such as MangaBaka's CC BY-NC-SA mean the hoster downloads the data; Panelarr never ships it ([scope](../product/scope.md)).
- **Library flags** ("in my library") come from server, not meta. meta knows nothing about users.
