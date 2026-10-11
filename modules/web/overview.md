---
title: web overview
status: proposed
tags: [module, web, react, tanstack, pwa]
related: [contracts/server-api.md, modules/server/overview.md]
inputs: [IN-0002]
updated: 2026-10-11
---

# web

## Summary

A SPA built with **Vite + React + TanStack Router, Query, Virtual, Pacer and Store** (IN-0002). It is installable as a **PWA** on desktop and mobile ("added as pwa or icon where app would be browser"). It holds no business rules and talks only to server's REST API and SSE.

## Stack
| Concern | Choice |
|---|---|
| Routing | TanStack Router (file-based, typed search params, loaders that prefetch Query) |
| Server state | TanStack Query. Client generated from OpenAPI (proposed: `openapi-typescript` + `openapi-fetch` + `openapi-react-query`). SSE → invalidations |
| Lists and reader | **TanStack Virtual**: library grids, chapter lists, long-strip reader (variable page heights) |
| Rate control | **TanStack Pacer**: debounced search-as-you-type, throttled progress sync while scrolling, page preload queues |
| Client state | **TanStack Store**: reader state (mode, page, zoom, direction), UI prefs |
| PWA | `vite-plugin-pwa` (Workbox). Offline chapters in OPFS / Cache Storage |
| UI kit | Open ([Q-0008](../../questions/README.md)) |
| Tests | Vitest + Testing Library; Playwright smoke |

## Screens
- **Library:** per-user grid or list, categories, filters, sort, unread badges.
- **Browse:**
  - pick a source (only allowed ones), then popular / latest / search with dynamic filters;
  - preview, then add to library.
- **Work page:** metadata, sources and variants, chapters, trackers, "fix match".
- **Reader:**
  - modes: paged (LTR/RTL), long strip (webtoon), double page with spread detection;
  - tap zones, zoom, keyboard shortcuts, preloading, progress sync, next-chapter handoff.
- **Downloads and jobs:** queue, progress over SSE, retry.
- **Search:** global search across the library (+ metadata).
- **Admin:** users and grants, plugins and indexes, network profiles, search backend, system.

## Implementation status
Not started (M2).
