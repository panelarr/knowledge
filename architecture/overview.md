---
title: Architecture overview
status: proposed
tags: [architecture, overview]
related: [architecture/plugins.md, architecture/contracts-and-transport.md, architecture/domain-model.md, architecture/deployment.md, modules/README.md]
inputs: [IN-0002, IN-0003]
updated: 2026-10-11
---

# Architecture overview

## Summary

Panelarr is a **Go core (`server`)** that serves a **React/TanStack PWA (`web`)** and hosts **opt-in plugins**: source plugins (Mihon via `source-mihon` + `mihon-source`, local files via `source-local`, more later) and metadata plugins (behind the optional **`meta`** service). Services talk over **protobuf/gRPC**. The browser talks **REST + OpenAPI + SSE**. Everything except `server` is optional ([ADR-0011](../decisions/ADR-0011-composable-opt-in-deployment.md)).

## Containers

```mermaid
flowchart TB
    U((Users<br/>browser / PWA)) -- "REST + OpenAPI 3.1, SSE" --> S

    subgraph core [Required]
        S["server (Go)<br/>users · library · jobs · files · trackers<br/>plugin host · search · web (go:embed)"]
        DB[(PostgreSQL)]
        FS[("/data/library<br/>CBZ + ComicInfo.xml")]
        S --- DB
        S --- FS
    end

    subgraph optional [Optional, hoster-chosen]
        META["meta (Go)<br/>metadata service · matching"]
        SE[(Typesense / Meilisearch)]
        subgraph splug [Source plugins]
            SM["source-mihon (Go)<br/>stores · trust · orchestration"]
            SL["source-local (Go)<br/>CBZ/CBR/CB7/CBT/folders"]
            SX["… future: OPDS, native, other ecosystems"]
        end
        MS["mihon-source (Kotlin/JVM)<br/>Mihon extensions over source-api + minimal admin"]
        subgraph mplug [Metadata plugins]
            MB[meta-mangabaka] --- MA[meta-anilist] --- MO[… MAL, MU, Kitsu, MangaDex, ComicVine]
        end
        NET["FlareSolverr / Byparr · HTTP/SOCKS proxies · gluetun VPN"]
    end

    S -- "gRPC (source-api)" --> SM & SL & SX
    S -. "gRPC (source-api), direct remote plugin" .-> MS
    SM -- "gRPC (source-api + mihon admin)" --> MS
    S -- "gRPC (meta API) or embedded" --> META
    META -- "gRPC (metadata-plugin)" --> mplug
    S -- "SearchIndex" --> SE
    MS & SM & SL -. "per-source network profile" .-> NET
```

## Responsibilities

| Component | Owns | Doesn't own |
|---|---|---|
| [server](../modules/server/overview.md) | Users, auth, permissions; Works and the source mapping; per-user libraries and progress; job queue (downloads, updates, refresh, re-index, tracker sync); files; plugin host; network profiles; search; trackers; REST API; serving web | Scraping, extension runtime, metadata aggregation |
| [web](../modules/web/overview.md) | All UI: library, browse, reader, admin; PWA and offline | Business rules |
| [source-api](../modules/source-api/overview.md) | Source-plugin protos, Go SDK, HTTP client factory honouring network profiles, conformance tests | Any concrete source |
| [source-mihon](../modules/source-mihon/overview.md) | Mihon extension stores, signing trust, install/update orchestration, caching | Running extensions |
| [mihon-source](../modules/mihon-source/overview.md) | Loading and running Mihon extensions; per-source OkHttp; prefs; speaks source-api | Stores, library, database |
| [source-local](../modules/source-local/overview.md) | Reading the user's archive and image folders as a source | Moving or modifying user files |
| [meta](../modules/meta/overview.md) | Metadata plugin host, aggregation, matching, metadata search | User data |
| [deploy](../modules/deploy/overview.md) | Compose profiles, Unraid templates, AIO image | — |

## Key flows

**Add a series from a source and read it**

```mermaid
sequenceDiagram
    actor U as User
    participant W as web
    participant S as server
    participant P as source plugin
    participant M as meta (optional)
    U->>W: search "Solo Leveling" in Browse
    W->>S: GET /api/v1/browse/search
    S->>P: Search(sourceId, query, filters)
    P-->>S: series list
    U->>W: Add to library
    W->>S: POST /api/v1/library
    S->>S: find or create Work, link SourceSeries
    S-)M: Match(titles, authors, year)
    M-->>S: candidates + confidence (auto-link if high)
    S->>P: GetChapters(series)
    S->>S: enqueue downloads per rules (shared store)
    S->>P: GetPages → FetchImage (via network profile)
    S->>S: write CBZ + ComicInfo, index, SSE event
    U->>W: open reader → pages streamed from CBZ (or proxied live if not downloaded)
```

## Cross-cutting docs
- [Contracts and transport](contracts-and-transport.md) · [Plugins](plugins.md) · [Networking](networking.md) · [Search](search.md)
- [Domain model](domain-model.md) · [Multi-user](multi-user.md) · [Storage layout](storage-layout.md) · [Trackers](trackers.md)
- [Security](security.md) · [Deployment](deployment.md) · [Repo standard](repo-standard.md)
