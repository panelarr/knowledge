---
title: Mihon Extension Store index format
status: draft
tags: [research, mihon, extensions, index]
related: [research/mihon-extensions.md, modules/source-mihon/overview.md, contracts/plugin-index.md]
inputs: [IN-0002]
updated: 2026-10-11
---

# Mihon Extension Store index format

> Checked on 2026-10-11 against a public Extension Store (EXTREPO's) and Suwayomi's `NetworkExtensionStore.kt`. Store URLs are intentionally not listed.

## Summary

Mihon moved from a flat `index.min.json` to an **Extension Store** described by `repo.json`, which points to a protobuf (`index.pb`) or JSON index. **source-mihon** parses both formats ([module](../modules/source-mihon/overview.md)). It is also the model for Panelarr's own [plugin index](../contracts/plugin-index.md).

## Files a store publishes (example: EXTREPO)
- `repo.json`: store info, `index_v2` → `index.pb`, and a **signing-key SHA-256 fingerprint**.
- `index.pb` (protobuf), `index.json` (~1.5 MB, the same data as JSON), `index.min.json` (legacy).
- Also `release-assets.json`, `icon/` and `index.html`.
- APKs appear to be GitHub release assets **[unverified]**.

## Store / extension / source fields
- **Store:** `name`, `badgeLabel`, `signingKey`, `contact`, `extensionList` | `extensionListUrl`.
- **Extension:** `name`, `packageName`, `resources{apkUrl, iconUrl, jarUrl}`, `extensionLib` (e.g. "1.6"), `versionCode`, `versionName`, `contentWarning` (`SAFE`/`MIXED`/`NSFW`).
  - `jarUrl` is EXTREPO-specific (proto field 501). It skips dex2jar.
- **Source:** `id`, `name`, `language`, `homeUrl`, `mirrorUrls`, `message`.
- **Format detection:** Suwayomi tells protobuf from JSON by the first byte.

## Legacy `index.min.json`
- `[{name, pkg, apk, lang, code, version, nsfw:0|1, sources:[{id, lang, name, baseUrl}]}]`.
- EXTREPO now publishes only placeholder entries there ("Outdated App"), so **legacy-only clients get nothing useful**.

## What it means for Panelarr
- mihon-source ([ADR-0021](../decisions/ADR-0021-mihon-source-standalone-admin.md)), and source-mihon if it keeps store logic ([Q-0026](../questions/README.md)), must support `repo.json` → `index.pb`/JSON first, and legacy as a fallback for other stores.
- **Verify the signing key** of downloaded APKs/jars against the store's `signingKey`. Suwayomi stores it but doesn't verify.
- Map `contentWarning` to Panelarr content ratings, for per-user limits.

## Sources
- Suwayomi `NetworkExtensionStore.kt`, `NetworkLegacyExtension.kt`
