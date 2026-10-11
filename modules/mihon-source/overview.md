---
title: mihon-source overview
status: proposed
tags: [module, mihon-source, mihon, kotlin, jvm]
related: [contracts/mihon-source-api.md, contracts/source-plugin.md, research/suwayomi-server.md, research/mihon-extensions.md, architecture/networking.md]
inputs: [IN-0002, IN-0003]
updated: 2026-10-11
---

# mihon-source

## Summary

A **small Kotlin/JVM tool** that runs Mihon extensions and exposes them **directly over an API** (IN-0003 §3.4). It speaks Panelarr's **source-api protos** over gRPC and HTTP/JSON with OpenAPI, so it works **standalone** and as a **remote source plugin** (IN-0003 §6, [ADR-0012](../../decisions/ADR-0012-protobuf-grpc-contracts.md)). It has no store logic, no library and no database; those belong to source-mihon and server.

## Owns / does not own
- **Owns:**
  - loading extension jars (APK → jar via dex2jar when there is no jar);
  - the Android shim layer;
  - per-source OkHttp clients built from network profiles;
  - extension prefs and cookies (files);
  - mapping Mihon `SManga`/`SChapter`/`Page`/`FilterList`/prefs onto the protos.
- **Doesn't own:** store indexes, update policy, trust decisions (it enforces a fingerprint it is given), users, downloads.

## Internals (planned)
| Part | Approach (from [Suwayomi research](../../research/suwayomi-server.md)) |
|---|---|
| Runtime | Kotlin, JVM 21. **Host classpath matches extensions-lib 1.4–1.6:** OkHttp 5.x, jsoup, kotlinx.serialization, coroutines, Injekt, RxJava 1 |
| Source API | Vendored `eu.kanade.tachiyomi.source.*` (Mihon API surface). EXTREPO base source class (lib 1.6) supported |
| Loading | dex2jar (`de.femtopedia.dex2jar`); ASM fix-ups (e.g. SimpleDateFormat); `ChildFirstURLClassLoader` per extension; `Source`/`SourceFactory` instantiation |
| Android shims | Context, SharedPreferences (file-backed), Base64, Log, Uri, Html, Bitmap/BitmapFactory, androidx.preference → JSON Schema, QuickJS/Duktape API backed by GraalJS. **Reuse Suwayomi's AndroidCompat vs write our own:** [Q-0003](../../questions/README.md) |
| Networking | One `OkHttpClient` per source from its profile: proxy, solver interceptor (FlareSolverr/Byparr, coalesced per host), rate limit, UA, cookie jar per source. **No JVM-global proxy properties** ([networking](../../architecture/networking.md)) |
| WebView | Optional ([Q-0002](../../questions/README.md)). Sources that need it report `needs_webview` |
| Server | gRPC + HTTP/JSON transcoding + OpenAPI docs (Armeria vs grpc-kotlin + Ktor, [Q-0020](../../questions/README.md)) |
| Storage | `/data/extensions/*.jar`, `/data/prefs/<sourceId>.json`, `/data/cookies/<sourceId>.json` |
| Isolation | One JVM, a classloader per extension ([Q-0007](../../questions/README.md)) |

## Standalone usage (target)
```
docker run -p 8080:8080 -v ./data:/data panelarr/mihon-source
# install an extension jar by URL, list sources, browse:
curl -X POST localhost:8080/v1/admin/extensions -d '{"url":"https://…/xyz.jar"}'
curl localhost:8080/v1/sources
curl localhost:8080/v1/sources/123456789/popular?page=1
```

## Implementation status
Not started (M1).
