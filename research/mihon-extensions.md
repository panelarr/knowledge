---
title: Community Mihon extensions (EXTREPO)
status: draft
tags: [research, mihon, extensions]
related: [research/mihon-extension-store.md, research/suwayomi-server.md, modules/mihon-source/overview.md]
inputs: [IN-0002]
updated: 2026-10-11
---

# Community Mihon extensions (EXTREPO)

> Checked on 2026-10-11. **[unverified]** marks items from memory or secondary sources. `EXTREPO` is an alias ([glossary](../meta/glossary.md)). This KB is public, so it never says where extensions can be obtained.

## Summary

EXTREPO is a large community collection of Mihon extensions (Apache-2.0). Extensions are Kotlin, built against the compile-only **extensions-lib** ("TachiyomiX") stubs, and published as APKs plus (EXTREPO-specific) jars through a Mihon **Extension Store** index ([format](mihon-extension-store.md)). Panelarr never bundles or points to any extension collection. Hosters add store URLs themselves ([Q-0016](../questions/README.md)).

## Repo layout
- Root folders: `src/`, `lib/`, `lib-multisrc/`, `core/`, `common/`, `compiler/`, `gradle/`.
- Extensions live in `src/<lang>/<name>`. `lib-multisrc/` holds ~64 shared "themes" (one theme serves many sites built on the same CMS).
- **Gradle DSL:** a project block `{ name, versionCode, contentWarning, libVersion, theme, pkgName, source { baseUrl, lang, id? } }`. Version name = `libVersion.versionCode` (e.g. `1.6.1`).

## extensions-lib versions
- Pinned at `tachiyomi-lib-v14` and `tachiyomi-lib-v16`. New code uses **lib 1.6** (main class extends an EXTREPO base source class). Lib 1.4 `HttpSource` is legacy.
- **Host runtime expected by 1.6:** Kotlin 2.4, coroutines 1.10, kotlinx.serialization 1.7+, **OkHttp 5.4**, jsoup 1.22, Injekt 1.0.
- **The collection builds with:** kotlinx.serialization (JSON, protobuf, json-okio), OkHttp 5.4 with brotli and zstd, jsoup, **QuickJS** (`zhanghai/quickjs-android`). There's no Rhino in the version catalog.

## Source IDs
- MD5 of `"${name.lowercase()}/$lang/$versionId"`, first 8 bytes, sign bit masked. Confirmed in Suwayomi's copy.
- `versionId` is bumped only when a site's URL scheme changes fundamentally. Renames pin `id` in Gradle.
- **Panelarr:** IDs are stable, so they work as `sourceId` inside a `mihon:<id>` namespaced source ID.

## Android APIs extensions use
- `ConfigurableSource` with SharedPreferences (`getPreferences()`/`getPreferencesLazy()`); mirror/custom-URL prefs are generated.
- **WebView:** helper utilities (`runWebView`, `getLocalStorage`, `runWebViewBlocking`) in the collection's utils package. These sources need a real browser engine.
- kotlinx.serialization `parseAs<T>()`, QuickJS, Injekt (`network.client`), and `android.util.Base64` **[unverified, common in practice]**.

## Sources
- The collection's CONTRIBUTING.md and `gradle/libs.versions.toml`, and its extensions-lib repo (links intentionally omitted).
