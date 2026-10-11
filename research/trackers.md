---
title: Trackers as implemented in Mihon
status: draft
tags: [research, trackers]
related: [architecture/trackers.md, research/metadata-providers.md]
inputs: [IN-0002]
updated: 2026-10-11
---

# Trackers as implemented in Mihon

> Checked on 2026-10-11 against Mihon's `data/track` source and docs.

## Summary

Mihon ships these trackers: AniList, Bangumi, Hikka, Kavita, Kitsu, Komga, MangaBaka, MangaUpdates, MyAnimeList, Shikimori and Suwayomi. Sync is mostly **one-way** (app → tracker). Komga, Kavita and Suwayomi are **"enhanced" trackers**: no login, they auto-bind to the matching source, and progress syncs both ways.

## Auth flows
| Tracker | Flow |
|---|---|
| AniList | OAuth2 **implicit** (`response_type=token`) (verified) |
| MyAnimeList | OAuth2 auth code + **PKCE "plain"** (verified) |
| Kitsu | OAuth2 **password grant**, hardcoded client secret, refresh tokens (verified) |
| MangaUpdates | Username/password → session token, `PUT /v1/account/login` (verified) |
| Shikimori, Bangumi, MangaBaka, Hikka | OAuth2 auth code with browser redirect **[unverified]** |

## What syncs
- **Progress:** chapter progress updates on the last page or on mark-read.
- **Status and dates:** start/finish status and dates update automatically.
- **Score:** user-set, in the tracker's own scale. Private entries exist on AniList, Bangumi, Kitsu and MangaBaka.
- **Offline:** changes are queued and sent on reconnect.

## What it means for Panelarr
- A **self-hosted** app has a different redirect URI on every instance. OAuth apps that need registered redirect URIs need per-instance client registration, a PIN/copy-token flow, or a shared relay ([Q-0004](../questions/README.md)).
- Panelarr can itself be an **"enhanced tracker"** target later, so the Mihon app could sync with it the way it syncs with Komga ([Q-0025](../questions/README.md)).
