---
title: Server API and events (browser-facing)
status: draft
tags: [contract, api, openapi, sse]
related: [architecture/contracts-and-transport.md, modules/server/overview.md, modules/web/overview.md]
inputs: [IN-0002]
updated: 2026-10-11
---

# Server API and events

## Summary

The browser and 3rd-party API is **REST + OpenAPI 3.1** under `/api/v1`, with an **SSE** event stream. It is designed for TanStack Query: resource-oriented, cursor pagination, ETags. **Public home:** `server/api/openapi.yaml`.

## Resource groups (sketch)
| Group | Examples |
|---|---|
| auth | `POST /auth/login`, `/auth/logout`, `/auth/oidc/*`, `GET /me`, API keys |
| users (admin) | CRUD, grants, quotas |
| plugins (admin) | indexes, available, installed, install/update/remove, settings, health |
| sources | list (visible to the user), filters, `popular`/`latest`/`search`, series preview, network-profile assignment (admin) |
| network-profiles (admin) | CRUD, test connectivity |
| works | get, search, merge/split, source mapping and priority, metadata match/fix, cover |
| chapters | list per Work (variants), mark read/unread, download, delete file (admin) |
| library | per user: entries, categories, filters, sort |
| reader | `GET /chapters/{id}/pages`, `GET /pages/{id}` (streams from CBZ or proxies live) |
| progress / history | per user |
| trackers | accounts, auth flows, bindings, sync now |
| jobs | queue view, pause/resume, retry, priorities |
| search (admin) | backend config, rebuild, stats |
| system | health, version, logs, backup/restore, Mihon backup import |
| opds | `/opds/v1.2/*` (separate auth) |

## Events (SSE `GET /api/v1/events`)
`job.progress`, `job.done`, `job.failed`, `chapter.downloaded`, `work.updated`, `library.changed`, `plugin.health`, `progress.synced`. Filtered per user. web turns these into TanStack Query invalidations.
