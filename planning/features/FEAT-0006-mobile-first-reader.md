---
title: "FEAT-0006: Mobile-first reader"
status: accepted
tags: [feature, server, web, m2]
related: [modules/web/overview.md]
inputs: [IN-0037, IN-0042, IN-0043]
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
  - **reading and sliding modes like Suwayomi's reader, polished** (IN-0043): single page, double page (spread detection, offset for covers), continuous vertical, webtoon (no gaps), continuous horizontal LTR/RTL; page transitions and swipe behaviour per mode;
  - fit width/height/original, zoom (pinch, double tap, wheel);
  - tap zones and swipe; keyboard shortcuts;
  - preloading; next-chapter handoff;
  - progress saved per user and synced across devices;
  - **settings per source** with a global default and per-series override;
  - pages from the downloaded CBZ or proxied live from the source;
  - installable PWA shell;
  - **themes:** several colour themes, custom colours and fonts for the app (IN-0043), and reader background colour.
- **Out:** offline chapters (M4), image filters (later).

## Acceptance criteria

- [ ] AC1: On a phone-sized screen the app uses mobile patterns (bottom navigation, full-screen reader, gestures, safe areas) and is installable as a PWA; on desktop it uses a sidebar layout. No horizontal scrolling at 360px.
- [ ] AC2: All reading modes work with touch, mouse and keyboard; RTL/LTR is respected in paged mode; long strip loads continuously.
- [ ] AC3: Zoom, fit, mode and direction are remembered **per source**, overridable per series, with global defaults; changing them in the reader updates the right level.
- [ ] AC4: Pages load from the CBZ when downloaded, otherwise proxied through the server from the source plugin (headers and network profile applied); the next pages are preloaded.
- [ ] AC5: Progress (chapter, page) saves as you read and appears on another device; finishing a chapter marks it read.
- [ ] AC6: Reaching the end offers the next chapter (unified list order) without leaving the reader.
- [ ] AC7: The reader offers single page, double page (with spread detection and a cover offset), continuous vertical, webtoon and continuous horizontal (LTR/RTL), with smooth, configurable page transitions; each mode works with touch, mouse and keyboard.
- [ ] AC8: Users pick from several colour themes (incl. dark and true-black), customise accent and key colours, and choose the UI font; choices are saved per user and apply across devices.

## Design notes

shadcn/ui + Tailwind ([Q-0008](../../questions/README.md)); [web](../../modules/web/overview.md).

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| server | [GOAL-0010](../../agents/goals/GOAL-0010-server-v0-accounts-add-and-match-chapters-reader-api-downloa.md) slice 7 | — | server side done (`e2726f1`; CBZ pages in slice 8) |
| web | [GOAL-0011](../../agents/goals/GOAL-0011-web-v0-panelarr-app-for-the-first-slice.md) | — | web side done (pending verification) |

## Open questions

- Per-series overrides: also per user? **Answered as built:** settings are per user (server `e2726f1`).
- Suwayomi's reader feature list is from the owner's experience; the web session should review it hands-on and list what to keep and what to polish.
