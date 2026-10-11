---
title: Metadata providers landscape
status: draft
tags: [research, metadata]
related: [research/mangabaka.md, research/trackers.md, modules/meta/overview.md]
inputs: [IN-0002]
updated: 2026-10-11
---

# Metadata providers landscape

> Checked on 2026-10-11. Rows marked **[unverified]** are from memory and need confirming before a plugin is built.

## Summary

These are candidate **metadata plugins** ([ADR-0009](../decisions/ADR-0009-plugins-not-bundled.md)). None ship by default. MangaBaka is the cross-reference backbone. The others add depth: characters, staff, western comics, fresher data.

| Provider | API | Auth / limits | Useful for |
|---|---|---|---|
| MangaBaka | REST + nightly dumps | Per IP: 30/min search, 180/min others | Backbone, external-ID map ([details](mangabaka.md)) |
| AniList | GraphQL `graphql.anilist.co` | ~90 req/min **[unverified]** | Rich data, **characters**, staff, relations |
| MyAnimeList | REST v2 | `X-MAL-CLIENT-ID` header **[unverified]** | Scores, popularity |
| MangaUpdates | REST `api.mangaupdates.com/v1` **[unverified]** | — | Scanlation groups, release feed, publishers |
| Kitsu | JSON:API `kitsu.app/api/edge` **[unverified]** | — | Alt titles |
| MangaDex | REST | ~5 req/s per IP (docs) | Not mapped by MangaBaka; also a common source |
| ComicVine | REST + API key | ~200 req/resource/hour **[unverified]** | **Western comics** (issues, volumes, characters) |

## Conventions worth adopting
- **ComicInfo.xml** (Anansi schema v2.0/2.1) inside CBZ is what Komga, Kavita and others read. Panelarr writes it on download and reads it in [source-local](../modules/source-local/overview.md).
- **komf** (a Komga/Kavita metadata fetcher) is prior art for matching-confidence UX **[unverified]**.

## What it means for Panelarr
- The meta matching engine must handle many-to-one external IDs and merged records.
- Every plugin declares its rate limits; the plugin host enforces them centrally.
- Characters come from AniList and ComicVine, not MangaBaka ([Q-0023](../questions/README.md)).
