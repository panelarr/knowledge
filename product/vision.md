---
title: Vision
status: proposed
tags: [product, vision]
related: [product/principles.md, product/scope.md, architecture/overview.md]
inputs: [IN-0002, IN-0003]
updated: 2026-10-11
---

# Vision

## Summary

**Panelarr** is a self-hosted, *arr*-style app for **panel media**: manga, manhwa, manhua and comics. It finds, acquires, curates, stores and reads them for a **whole household or group from one install**, with a reader that works as a PWA on desktop and mobile. It is *inspired* by Sonarr/Radarr's idea of media management, not their design (IN-0002).

## The problem
- **Suwayomi** proved that Mihon extensions can run as a server, but:
  - in practice it is one person per instance ("imagine you have to run 3 instances for 3 different people", IN-0002);
  - networking is global;
  - the downloader is fragile.
- Mihon/Tachiyomi are single-device apps. Komga and Kavita read files well but don't acquire them.
- Metadata is scattered across MangaBaka, AniList, MAL, MangaUpdates and others. So is tracking.

## What Panelarr is
1. **One store, many readers.** Content is downloaded once and shared, while each user keeps their own library, progress and trackers ([ADR-0003](../decisions/ADR-0003-shared-store-per-user-libraries.md)).
2. **Sources as plugins.** These include Mihon extensions (via the small **mihon-source** tool), the user's own CBZ/CBR files, and more later. Nothing ships by default ([ADR-0009](../decisions/ADR-0009-plugins-not-bundled.md)).
3. **Per-source networking.** Each source can have its own proxy, VPN exit, FlareSolverr/Byparr solver and rate limit ([ADR-0016](../decisions/ADR-0016-per-source-network-profiles.md)).
4. **Metadata and search.** Aggregated metadata (MangaBaka dumps and APIs as plugins). Search covers every title and language, with an optional Typesense-class engine ([ADR-0010](../decisions/ADR-0010-optional-search-engine.md)).
5. **Trackers.** Any tracker, bound per user.
6. **A great reader.** A fast PWA reader with paged, long-strip (webtoon) and double-page modes, RTL/LTR, and offline chapters.
7. **Standalone pieces.** mihon-source, meta and the source plugins are useful on their own, for other projects too.
8. **Self-host friendly.** Docker, Unraid templates, and a minimal install that is only one container ([ADR-0011](../decisions/ADR-0011-composable-opt-in-deployment.md)).
