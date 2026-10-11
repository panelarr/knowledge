---
title: Suwayomi-Server internals
status: draft
tags: [research, suwayomi, mihon, jvm]
related: [modules/mihon-source/overview.md, research/mihon-extensions.md, research/mihon-extension-store.md]
inputs: [IN-0002]
updated: 2026-10-11
---

# Suwayomi-Server internals

> Checked on 2026-10-11 against `master`. Items marked **[unverified]** were not confirmed in source.

## Summary

Suwayomi-Server is the reference for running Mihon/Tachiyomi extensions on a plain JVM. Its extension loading and Android shims are the most useful parts for Panelarr. Its networking is global-only, and its downloader and multi-user model are what Panelarr wants to improve on. Kotlin 2.4, JVM 21, Javalin 7, Exposed with H2 or Postgres, GraphQL plus legacy REST.

## Extension loading
- **Install** (`server/.../manga/impl/extension/Extension.kt`): downloads `jarUrl` if the store provides one, otherwise `apkUrl`.
  - APK → jar with **dex2jar** (`de.femtopedia.dex2jar:dex-translator:2.4.38`, `PackageTools.kt`). APK `assets/` are copied into the jar.
  - Checks the `tachiyomi.extension` feature and a lib version in range `LIB_VERSION_MIN 1.3 … LIB_VERSION_MAX 1.6`.
  - Loads the class from the `tachiyomi.extension.class` metadata. `Source` gives one source; `SourceFactory.createSources()` gives several.
- **Bytecode patching** (`BytecodeEditor.kt`): ASM rewrites `java/text/SimpleDateFormat` to an icu4j-backed Android-style replacement.
- **APK metadata:** `net.dongliu:apk-parser:2.6.10`. It computes the SHA-256 of the first signing cert, but **no trust verification** is done. V2 signatures have an upstream issue.
- **Classloading:** one `ChildFirstURLClassLoader` per jar, cached, with a per-jar mutex. Uninstall closes the loader.

## AndroidCompat (Android API shims)
- Built on `com.github.Suwayomi:android-jar:1.0.0` stubs plus hand-written replacements in `AndroidCompat/src/main/java/`.
- **Shimmed packages:**
  - `android.content` (Context, SharedPreferences, Intent, PackageManager);
  - `android.os` (Build, Bundle, Handler, Looper, SystemClock);
  - `android.util` (Base64, Log, LruCache);
  - `android.graphics` (Bitmap, BitmapFactory, Canvas);
  - `android.text.Html`, `android.net.Uri`, `android.database.sqlite.*`;
  - `android.webkit` (WebView via **KCEF/JCEF**, CookieManager);
  - `androidx.preference.*`, `dalvik.system.PathClassLoader`.
- **JS:** `app.cash.quickjs.QuickJs` and `com.squareup.duktape.Duktape` are shims backed by **GraalJS**.
- **SharedPreferences:** stored as XML Properties files per key under `<root>/settings/`.
- **Images:** TwelveMonkeys plus imageio-webp.
- **Licence:** the Suwayomi-Server licence is **[unverified]** (believed MPL-2.0). It must be checked before any code reuse ([Q-0003](../questions/README.md)).

## Source API
- A copy of the Mihon source API lives *inside* the repo (`eu.kanade.tachiyomi.source.*`): `CatalogueSource` (suspend `getPopularManga`, `getSearchManga`, `getLatestUpdates`, `getMangaUpdate`, `getPageList`), `HttpSource`, `ConfigurableSource`, `ResolvableSource`.
- **Host classpath must match extensions:** OkHttp **5.x** ("major version locked by extensions"), RxJava 1.3.8, jsoup, kotlinx.serialization, Injekt (bridged to Koin).
- **Source ID:** first 8 bytes of MD5(`"${name.lowercase()}/$lang/$versionId"`), sign bit cleared.
- Mid-2026 (v2.3.2223+) added lib 1.6 support and Mihon's **Extension Store** system.

## Networking (what Panelarr must do better)
- **One shared OkHttp client** for all sources (`NetworkHelper.kt`), with a fixed Android Chrome UA.
- **Cookies:** a `PersistentCookieStore` set as the JVM default.
- **Cloudflare:** handled only through **FlareSolverr** (`CloudflareInterceptor.kt`). On 403/503 from `Server: cloudflare` it asks FlareSolverr for `cf_clearance` and the UA. Solves are serialized per host.
- **Proxy:** SOCKS only, set **globally** through JVM system properties. **No per-source proxy.** Changing the UA re-registers every source.

## API, database, downloader, users
- **APIs:** GraphQL (graphql-kotlin), legacy REST + WebSockets, OPDS v1.2.
- **Database:** Exposed with H2 (default) or PostgreSQL.
- **Downloader:**
  - one Downloader per source, at most 6 sources in parallel;
  - the queue is kept in SharedPreferences, not the database;
  - failed items are not retried automatically.
- **Users:** multi-user now exists (`authMode=ui_login`: JWT, bcrypt, roles and permissions). Library, chapters, categories and settings are per user. Downloads, the queue, source prefs and extensions are shared.
  - **Documented gaps:** page/CBZ endpoints don't check ownership, and queue control isn't per user.
- **Docker:** `eclipse-temurin` JRE plus Xvfb and Chromium libraries for KCEF. Image size **[unverified]** (likely several hundred MB).

## What it means for Panelarr
- **Reuse the approach** (dex2jar, child-first classloaders, the AndroidCompat-style shims, GraalJS behind the QuickJS API), subject to the licence check.
- **Do better on:**
  - per-source OkHttp clients with **network profiles** ([networking](../architecture/networking.md));
  - verifying extension signing keys;
  - a DB-backed retrying job queue;
  - real ownership checks;
  - keeping mihon-source **small**: no library, no DB ([mihon-source](../modules/mihon-source/overview.md)).
- **Pain points to plan for:**
  - WebView-only sources need headless Chromium ([Q-0002](../questions/README.md));
  - every extension runs in one process ([Q-0007](../questions/README.md));
  - classpath version pinning against extensions-lib.

## Sources
- https://github.com/Suwayomi/Suwayomi-Server
- https://github.com/Suwayomi/docker-tachidesk
