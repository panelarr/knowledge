---
title: Scope
status: draft
tags: [product, scope]
related: [planning/roadmap.md, architecture/overview.md]
inputs: [IN-0002, IN-0003]
updated: 2026-10-11
---

# Scope

## Summary

What Panelarr does, roughly grouped by milestone ([roadmap](../planning/roadmap.md)). Anything not listed is out of scope until it's added here.

## In scope (v1 direction)
| Area | Features |
|---|---|
| Users | Local accounts, admin/user roles, permissions (allowed plugins/sources, content-rating ceiling, may-add, may-download, quotas), API keys, optional OIDC |
| Plugins | Add plugin indexes, install/update/remove, settings forms, health. Kinds: source, metadata |
| Sources | Browse popular/latest, search with filters, series details, chapters, pages. Network profiles per source |
| Library | Per-user library and categories. A Work maps to several source series. Chapter de-duplication and preferred scanlator/source |
| Acquisition | Update checks, auto-download rules, shared download queue with retries and per-source limits, CBZ + ComicInfo |
| Local files | source-local for the user's CBZ/CBR/CB7/CBT/folders; optional "adopt into library" |
| Metadata | meta service with plugins (MangaBaka, AniList, …); matching with confidence; manual fix |
| Search | Built-in DB search; optional Typesense/Meilisearch |
| Reader | PWA: paged / long strip / double page, RTL/LTR, zoom, preloading, progress sync, offline chapters |
| Trackers | AniList, MAL, Kitsu, MangaUpdates, Shikimori, Bangumi, MangaBaka, webhook. Per user |
| Interop | OPDS feed; Mihon backup import |
| Ops | Notifications (webhook/Discord/Apprise), backups, logs, health, Docker/Unraid |

## Explicitly out of scope (for now)
- Hosting or redistributing content publicly. Panelarr is a private, self-hosted library.
- Bundling any extension, extension store, or metadata dump.
- Native mobile apps (the PWA covers mobile).
- Social features beyond one instance.

## Maybe later
- Request/approve flow (Overseerr-style), Panelarr as a Mihon tracker/source target ([Q-0025](../questions/README.md)), novels, a Kotatsu/Paperback ecosystem ([Q-0009](../questions/README.md)), an AIO image.
