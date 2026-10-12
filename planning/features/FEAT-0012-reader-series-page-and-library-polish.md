---
title: "FEAT-0012: Reader, series page and library polish"
status: accepted
tags: [feature, web, reader, library, ux]
related: [planning/features/FEAT-0006-mobile-first-reader.md, planning/features/FEAT-0005-unified-chapters-and-update-checks.md, modules/web/overview.md]
inputs: [IN-0060]
milestone: ""
priority: P1
updated: 2026-10-12
---

# FEAT-0012: Reader, series page and library polish

## Problem

"now regarding reader it feels way to crowded doesnt go to next page on scroll … The item page by default latest on the top so DESC sort. … ours look more like app instead of actual reader. … for custom filters this can be future goal, the bookmarks is real idea. U can see how our reader on mobile is way to crowded, the new chapters have badge while suwayomi just mark it whiter color and dakrer (like disabled) when read, too many boxes we should make it pretty similar, some things can be just icon buttons with menu. see referneces for ideas" (IN-0060, with screenshots of ours and of the reference app described there).

## Outcome

Reading feels like a reader, not an app: the page fills the screen, the chrome is a thin top and bottom bar that hides, and settings live in one sheet. The series page and library are calm lists and grids with icon buttons and menus instead of boxes, close to the reference app.

## Scope

- **Bug now:** in long-strip reading, scrolling doesn't move on to the next page (the first page sits under a full-screen chapter-start panel with a spinner).
- **Series page:** chapters newest first by default (DESC); plain chapter rows (title, source, date, downloaded) with **unread bright and read dimmed** instead of "New" badges; the header's actions as **icon buttons with menus**: mark read, a download menu (next chapter, next 5, 10, 25, unread, all), one filter / sort / display sheet, and select mode with batch actions (download, delete, bookmark, mark read or unread); secondary actions in a ⋯ menu; a collapsible description and genre chips.
- **Reader:** a thin top bar (series, chapter, **bookmark**, ⋯) and a bottom bar of icons (chapters, layout, settings) that hide while reading; the chapter-start and chapter-end transitions small, not full screen; all reader settings in one sheet with tabs (Layout: mode, direction, tap zones, scale; General: background, progress bar, page number, safe area), with a mark on settings changed for this series.
- **Bookmarks** (a real feature): bookmark chapters (per user), filter by bookmarked, bookmark in batch; needs a server API.
- **Library:** ideas from the reference: unread count badges and a continue-reading button on covers; one filter / sort / display sheet (unread, started, downloaded, bookmarked; sorts; compact, comfortable grid or list).
- **Later (a future goal):** custom image filters in the reader (brightness, contrast, saturation, hue, sepia, grayscale, invert).

## Acceptance criteria

- [ ] AC1: In long-strip mode, scrolling moves through every page of a chapter and on into the next; the chapter-start notice takes no more than a small strip.
- [ ] AC2: A series page lists chapters newest first by default; the choice is remembered.
- [ ] AC3: Unread chapters show bright and read ones dimmed; no "New" badges in the list.
- [ ] AC4: The series page header has no boxed button rows: icon buttons with menus and one filter / sort / display sheet.
- [ ] AC5: The reader shows only thin top and bottom bars that hide on tap or scroll; all settings are in one tabbed sheet.
- [ ] AC6: A user can bookmark a chapter from the reader and the list, filter by bookmarked, and bookmark in batch.
- [ ] AC7: On a phone, the reader's page fills the screen with the bars hidden.

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| web | — | — | dispatched to `panelarr-web` (plan first; bug and DESC default straight away) |
| server | — | — | bookmarks API, dispatched to `panelarr-server` |

## Open questions

- Library changes: how far to follow the reference now (badges, play button, sheet) vs later.
