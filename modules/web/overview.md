---
title: web overview
status: proposed
tags: [module, web, react, tanstack, pwa]
related: [contracts/server-api.md, modules/server/overview.md]
inputs: [IN-0002, IN-0037]
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
| UI kit | **shadcn/ui + Tailwind** (Q-0008, IN-0037) |
| Tests | Vitest + Testing Library; Playwright smoke |

## Separate client (IN-0041)
- `web` is its own repo (ADR-0002) and only uses the public [server API](../../contracts/server-api.md); the server image embeds a pinned web release, and users may build or run their own client against the same API.

## Working assumptions from the v0 plan (2026-10-11)
- **Stack:** Vite, React 19, TypeScript, TanStack (Router, Query, Virtual, Pacer, Store), shadcn/ui on Tailwind v4, pnpm, a PWA (app shell only in v0), fonts self-hosted.
- **API:** client generated from the server's spec (copied from server `main`); parts the server hasn't specced are drafted by web and sent through the keeper; the server owns the final shape.
- **Defaults:** brand pink accent; font list in config.
- **Embedding contract** (web `docs/embedding.md`, `331ae2e`): the server embeds the release tarball of `dist/`; SPA fallback for everything except `/api/`, `/opds/`, `/assets/`, `/healthz`, `/readyz`, `/metrics`; `assets/*` cached immutable, everything else no-cache; `sw.js` served from the root; headers CSP + nosniff + `Referrer-Policy: no-referrer` + `X-Frame-Options: DENY` (exact strings in web `csp.config.mjs`); paths relative to `<base href="/">`. **CSP:** `script-src 'self'` (strict), `img-src 'self' data: blob:`, and `style-src 'self' 'unsafe-inline'`, because Radix's scroll lock and the toast library insert style elements at runtime.
- **Not in v0:** library categories, offline chapters, connected-service admin pages (IN-0039).

## Look and feel (IN-0037 §3)
- **Fully responsive.** On phones it should look and feel like a **native mobile app**: bottom navigation, full-screen views, touch gestures, safe-area insets, installable PWA. On desktop it should look good too: sidebar navigation, wider grids, keyboard shortcuts.
- **Theming (IN-0043):** several colour themes (light, dark, true-black/AMOLED and preset palettes), **custom colours** (accent and key surfaces, saved per user), and **font choice** for the UI. Built on CSS variables, which shadcn/ui's theming uses.
- **Reader settings per source:** zoom level, fit, reading mode and direction, remembered **per source** (with a global default and a per-series override, suggestion), since sources differ in page sizes and formats.

## Screens
- **Library:** per-user grid or list, categories, filters, sort, unread badges.
- **Browse:**
  - pick a source (only allowed ones), then popular / latest / search with dynamic filters;
  - preview, then add to library.
- **Work page** (ADR-0028): metadata from meta, **a tab per source** with its own chapters, and a **unified chapter list** that fills gaps from other sources; trackers; "fix match" (attach, detach, confirm sources).
- **Reader:**
  - modes: paged (LTR/RTL), long strip (webtoon), double page with spread detection;
  - tap zones, zoom, keyboard shortcuts, preloading, progress sync, next-chapter handoff;
  - **settings remembered per source** (zoom, fit, mode, direction), with global defaults and per-series overrides (IN-0037 §3).
- **Downloads and jobs:** queue, progress over SSE, retry.
- **Search:** global search across the library (+ metadata).
- **Admin:** users and grants, plugins and indexes, network profiles, search backend, system.
- **Connected services, built into Panelarr's admin** (IN-0039): when meta and mihon-source are connected, most of their admin is available inside Panelarr itself: meta's providers, sync runs and jobs, health, duplicates review, integrations; mihon-source's extensions, stores, sources and health checks, jobs, integrations. It's the same API their own admins use (every admin action is a plain API call), called by the server with each service's admin-scope key. Standalone admins stay for people not running Panelarr.

## Implementation status
v0 done (GOAL-0011, `panelarr-web`; verified at `8154eb1`, [test report](../../qa/reports/goal-0011-web-v0-done-verification.md)). Slice 0 (scaffold) merged at `331ae2e`: the stack, a spec copy from server main with a drafts overlay, generated client, one error type, the SSE client, MSW mocks validated against the spec, the responsive shell (sidebar / bottom nav), themes before first paint, PWA app shell; 37 unit and 8 Playwright tests (desktop, 360 px, CSP). Slice 1 (setup and login; FEAT-0003 web side) merged at `150a90f`: the first-run wizard (admin, metadata service with a checklist, "start sync" and polling, optional source plugin), sign-in with clear errors and safe redirects, invites, settings (profile, password and sessions, API keys, appearance), the admin health banner; stateful mock scenarios; mocks validated against the spec; 79 unit and 14 Playwright tests. Slices 2–10 merged (up to `dd4ed74`): users, plugins and sources admin (schema-driven plugin settings); catalogue (search, browse, entry, add); jobs, queue and live events; library, add and fix match, source browsing; work page with unified chapters and source tabs; the reader (single and double page, long strip and webtoon, horizontal, gestures and zoom, tap zones, progress and resume, chapter transitions, settings per series / source / everywhere, defaults by work type, auto webtoon, wake lock, fullscreen); downloads and storage; themes, accent and key colours, fonts per user; PWA install, accessibility checks, a journey test and size budgets. 259 unit and 29 Playwright tests. Uses the server's API follow-ups (`6829bad`). Smoke-tested against the real server in the compose stack (setup wizard, sign-in, admin pages; embedded in the server image); a deeper real-server check by `panelarr-web` passed (every page, 0 console errors or failed requests, CSP clean); its fixes (no `/me` probe before sign-in, plain versions, an empty-catalogue message) are at `8154eb1`. The wizard lets the admin continue before meta has data, with a warning (IN-0045). Owner-reported layout fixes (IN-0047, IN-0048): form fields in a row line up (`Field` packs to the top), dialogs fit the screen with a pinned footer, tab strips scroll only sideways (a shared `ScrollStrip`), job parameter names shown as words; a layout regression test (`e2e/layout.spec.ts`) at `6163280`, `e56a72b`.
