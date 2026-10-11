---
title: "FEAT-0006: Mobile-first reader"
status: accepted
tags: [feature, server, web, m2]
related: [modules/web/overview.md]
inputs: [IN-0037, IN-0042]
milestone: "M2"
priority: P1
updated: 2026-10-11
---

# FEAT-0006: Mobile-first reader

## Problem

"the ui should be fully responsive, like full mobile native app look on mobiles and good look on desktop, per source zoom levels and etc (in reader)" (IN-0037 §3).

## Outcome

Reading in Panelarr on a phone feels like a native manga app; on desktop it is comfortable with keyboard and mouse. Reader settings are remembered per source.

## Scope

- **In:**
  - modes: paged LTR/RTL, vertical, long strip (webtoon), double page with spread detection;
  - fit width/height/original, zoom (pinch, double tap, wheel);
  - tap zones and swipe; keyboard shortcuts;
  - preloading; next-chapter handoff;
  - progress saved per user and synced across devices;
  - **settings per source** with a global default and per-series override;
  - pages from the downloaded CBZ or proxied live from the source;
  - installable PWA shell.
- **Out:** offline chapters (M4), image filters (later).

## Acceptance criteria

- [ ] AC1: On a phone-sized screen the app uses mobile patterns (bottom navigation, full-screen reader, gestures, safe areas) and is installable as a PWA; on desktop it uses a sidebar layout. No horizontal scrolling at 360px.
- [ ] AC2: All reading modes work with touch, mouse and keyboard; RTL/LTR is respected in paged mode; long strip loads continuously.
- [ ] AC3: Zoom, fit, mode and direction are remembered **per source**, overridable per series, with global defaults; changing them in the reader updates the right level.
- [ ] AC4: Pages load from the CBZ when downloaded, otherwise proxied through the server from the source plugin (headers and network profile applied); the next pages are preloaded.
- [ ] AC5: Progress (chapter, page) saves as you read and appears on another device; finishing a chapter marks it read.
- [ ] AC6: Reaching the end offers the next chapter (unified list order) without leaving the reader.

## Design notes

shadcn/ui + Tailwind ([Q-0008](../../questions/README.md)); [web](../../modules/web/overview.md).

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| web, server | — | — | — |

## Open questions

- Per-series overrides: also per user? (suggestion: settings are per user).
