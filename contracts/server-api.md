---
title: Server API and events (browser-facing)
status: draft
tags: [contract, api, openapi, sse]
related: [architecture/contracts-and-transport.md, modules/server/overview.md, modules/web/overview.md]
inputs: [IN-0002, IN-0041]
updated: 2026-10-11
---

# Server API and events

## Summary

The browser and 3rd-party API is **REST + OpenAPI 3.1** under `/api/v1`, with an **SSE** event stream. **It is a public client API** (IN-0041): our `web` app is just one client in its own repo, and anyone can build another. Every web feature uses only this documented API, it is versioned (breaking changes need `/api/v2`, checked in CI against the published spec), and clients authenticate with personal API keys or a session. It is designed for TanStack Query: resource-oriented, cursor pagination, ETags. **Public home:** `server/api/openapi.yaml`.

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

**Sources are admin-only (2026-10-12, server `4a51c86`, IN-0054):** listing sources and browsing, searching or reading a source directly need an admin with the admin scope. Users see sources only on works (each with `lang`), plus signed source images. The one deliberate non-additive change within v1, recorded in the server's docs/api.md.

**Packages (2026-10-12, server `1d732f6`):** for plugins whose `capabilities` include `packages`, admin endpoints `GET /plugins/{id}/packages[/{pkg}]`, `POST …/install|update` and `DELETE …/{pkg}` (202 tasks of kind `plugin.package`), `PUT …/languages`. Sources carry `package_id`, `package_name` and `unavailable_reason` (`language`). Single-site plugins answer 422 `no_packages`.
