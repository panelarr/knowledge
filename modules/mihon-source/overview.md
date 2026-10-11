---
title: mihon-source overview
status: proposed
tags: [module, mihon-source, mihon, kotlin, jvm]
related: [decisions/ADR-0021-mihon-source-standalone-admin.md, contracts/mihon-source-api.md, contracts/source-plugin.md, research/suwayomi-server.md, research/mihon-extensions.md, architecture/networking.md]
inputs: [IN-0002, IN-0003, IN-0005, IN-0006]
updated: 2026-10-11
---

# mihon-source

## Summary

A **standalone Kotlin/JVM service** that runs Mihon extensions and exposes them **directly over an API** (IN-0003 §3.4). It speaks Panelarr's **source-api protos** over gRPC and HTTP/JSON with OpenAPI, so it works **standalone** and as a **remote source plugin** (IN-0003 §6, [ADR-0012](../../decisions/ADR-0012-protobuf-grpc-contracts.md)). It has a **minimal admin** (React SPA) for sources, extension stores, clients and API keys, and integrations ([ADR-0021](../../decisions/ADR-0021-mihon-source-standalone-admin.md), IN-0006). It has no library, no users and no database; those belong to server.

## Owns / does not own
- **Owns:**
  - loading extension jars (APK → jar via dex2jar when there is no jar);
  - the Android shim layer;
  - per-source OkHttp clients built from network profiles;
  - extension prefs and cookies (files);
  - mapping Mihon `SManga`/`SChapter`/`Page`/`FilterList`/prefs onto the protos;
  - **extension stores:** store URLs, index parsing, signing-key pinning and verification, install and update from stores;
  - **clients and auth:** the admin token and scoped client API keys;
  - **integrations:** solvers and network profiles, assigned per source;
  - the **admin SPA** (browse and test sources, settings, extensions, stores, clients, integrations).
- **Doesn't own:** users, libraries, downloads. In the Panelarr stack its config comes from the main app through source-mihon; **the admin is for standalone users** (Q-0030, IN-0007 §1).

## Internals (planned)
| Part | Approach (from [Suwayomi research](../../research/suwayomi-server.md)) |
|---|---|
| Runtime | Kotlin, JVM 21. **Host classpath matches extensions-lib 1.4–1.6:** OkHttp 5.x, jsoup, kotlinx.serialization, coroutines, Injekt, RxJava 1 |
| Source API | Vendored `eu.kanade.tachiyomi.source.*` (Mihon API surface). EXTREPO base source class (lib 1.6) supported |
| Loading | dex2jar (`de.femtopedia.dex2jar`); ASM fix-ups (e.g. SimpleDateFormat); `ChildFirstURLClassLoader` per extension; `Source`/`SourceFactory` instantiation |
| Android shims | Context, SharedPreferences (file-backed), Base64, Log, Uri, Html, Bitmap/BitmapFactory, androidx.preference → JSON Schema, QuickJS/Duktape API backed by GraalJS. **Our own shims**, Suwayomi studied as a reference, no code copied (Q-0003 answered, IN-0005 §2) |
| Networking | One `OkHttpClient` per source from its profile: proxy, solver interceptor (FlareSolverr/Byparr, coalesced per host), rate limit, UA, cookie jar per source. **No JVM-global proxy properties** ([networking](../../architecture/networking.md)) |
| WebView | Optional ([Q-0002](../../questions/README.md)). Sources that need it report `needs_webview` |
| Server | gRPC + gRPC-Web + HTTP/JSON transcoding on one port, OpenAPI generated from the protos. **Armeria** ([ADR-0024](../../decisions/ADR-0024-armeria-for-the-jvm-rpc-server.md)); Armeria-specific code kept in one file, services are plain grpc-kotlin |
| Storage | `/data/extensions/*.jar`, `/data/prefs/<sourceId>.json`, `/data/cookies/<sourceId>.json`, plus files for stores, clients (hashed keys) and integrations |
| Admin UI | Small React SPA ([ADR-0006](../../decisions/ADR-0006-technology-stack.md) stack) built in a multi-stage image and served by the service. Logs in with the admin token |
| Auth | One admin token (env or generated on first start, shown once); scoped client API keys, hashed at rest |
| Isolation | One JVM, a classloader per extension ([Q-0007](../../questions/README.md)) |

## Standalone usage (target)
```
docker run -p 8080:8080 -v ./data:/data panelarr/mihon-source
# install an extension jar by URL, list sources, browse:
# open http://localhost:8080/ and log in with the admin token from the logs,
# or use the API with it:
curl -H "Authorization: Bearer $ADMIN" -X POST localhost:8080/v1/admin/extensions -d '{"url":"https://…/xyz.jar"}'
curl -H "Authorization: Bearer $CLIENT_KEY" localhost:8080/v1/sources
curl -H "Authorization: Bearer $CLIENT_KEY" localhost:8080/v1/sources/123456789/popular?page=1
```

## Implementation status
Not started (M1). [GOAL-0001](../../agents/goals/GOAL-0001-mihon-source-v0-run-mihon-extensions-over-the-source-api.md) is dispatched to `panelarr-mihon-source` (2026-10-11). **Slices 1–2 done:** scaffold (`chore/repo-scaffold`), then protos, API server and token auth (`feat/api-protos-auth` @ `2124d96`): GetInfo, Health and ListSources answer; other RPCs are UNIMPLEMENTED until their slice. Admin SPA started in parallel (`feat/admin-spa`). `main` has no commits until the owner merges. Until `source-api` exists, the `panelarr.source.v1` protos live in this repo's `proto/` and move later (IN-0005 §2).
