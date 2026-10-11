---
title: Trackers
status: draft
tags: [architecture, trackers]
related: [research/trackers.md, architecture/domain-model.md, modules/server/overview.md]
inputs: [IN-0002]
updated: 2026-10-11
---

# Trackers

## Summary

Users connect their own tracker accounts. Panelarr binds Works to remote entries, using meta's external IDs to **suggest** bindings, and syncs progress, status, score and dates. For now trackers are built into server behind a Go `Tracker` interface. Whether they become a plugin kind is open ([Q-0021](../questions/README.md)). IN-0002 asks for the ability to "integrate any kind of trackers".

## Interface (sketch)
```go
type Tracker interface {
    Info() TrackerInfo                    // id, name, auth kind, score scale, supports private/dates
    AuthStart(ctx, user) (AuthChallenge, error)  // OAuth URL / PIN / credentials form
    AuthFinish(ctx, user, input) (Account, error)
    Search(ctx, acct, query) ([]Remote, error)
    Get(ctx, acct, remoteID) (Remote, error)
    Push(ctx, acct, binding, state) error // progress, status, score, dates, private
    Pull(ctx, acct, binding) (State, error) // two-way where supported
}
```

## Built-in targets
| Tracker | Auth (Mihon prior art) | Notes |
|---|---|---|
| AniList | OAuth implicit / PIN | Rich; supports private entries |
| MyAnimeList | OAuth code + PKCE | |
| Kitsu | OAuth password grant | |
| MangaUpdates | Username/password session | |
| Shikimori, Bangumi, MangaBaka | OAuth code | |
| **Webhook** | — | Generic: POST progress events to any URL. Covers "any tracker" until a plugin kind exists |

## Behaviour
- **Auto-bind suggestion:** if a Work's MetaLink has the tracker's ID (MangaBaka cross-references AniList, MAL, Kitsu, MU and Shikimori), propose the binding.
- **Push** on chapter completion, on status change (start/finish), and when the user sets a score. Pushes are **queued jobs** with retries, so they survive offline periods and API outages.
- **Pull** (optional, per account) imports remote progress, e.g. from reading on another app. Conflict rule: take the higher progress unless the user overrides.
- **OAuth redirect on self-hosted instances** is the hard part ([Q-0004](../questions/README.md)).
