---
title: "FEAT-0012: Reader, series page and library polish"
status: accepted
tags: [feature, web, reader, library, ux]
related: [planning/features/FEAT-0006-mobile-first-reader.md, planning/features/FEAT-0005-unified-chapters-and-update-checks.md, modules/web/overview.md]
inputs: [IN-0060, IN-0061]
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

- [x] AC1: In long-strip mode, scrolling moves through every page of a chapter and **straight on into the next chapter, loaded automatically as you near the end** (no button press; IN-0061); between chapters only a small strip shows which chapter starts.
- [x] AC2: A series page lists chapters newest first by default; the choice is remembered.
- [x] AC3: Unread chapters show bright and read ones dimmed; no "New" badges in the list.
- [x] AC4: The series page header has no boxed button rows: icon buttons with menus and one filter / sort / display sheet.
- [x] AC5: The reader shows only thin top and bottom bars that hide on tap or scroll; all settings are in one tabbed sheet.
- [x] AC6: A user can bookmark a chapter from the reader and the list, filter by bookmarked, and bookmark in batch.
- [x] AC7: On a phone, the reader's page fills the screen with the bars hidden.

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| web | — | — | quick fix done (`647cb99`): long strip loads pages in reading order, chapters load on scroll in both directions, small bands between chapters, newest first by default; rest planned next |
| server | — | — | bookmarks API done (`781ed85`): per user, batch, `bookmarked` on chapters and a filter, counts in the library, `bookmarks.changed` events |

## Open questions

- Library changes: how far to follow the reference now (badges, play button, sheet) vs later.

## Plan (accepted by the keeper, 2026-10-12)

`panelarr-web`, after the quick fix (`647cb99`, AC1–AC2):
- **R1 series page:** one row of icon buttons (in library, a download menu, a mark-read menu, one filter / sort / display sheet, select mode, ⋯); plain rows with unread bright and read dimmed, no "New" badges; the summary says "N chapters · M unread"; select mode with a floating batch bar.
- **R2 bookmarks** on server `781ed85`: in the reader, the row menu, batch actions, a filter, a mark on the row.
- **R3 reader chrome:** a thin top bar (back, series and chapter, bookmark, ⋯) and a bottom icon bar (chapters, quick layout, settings) that hide while reading; one settings sheet (Layout, General) with a This series / This source / Everywhere switch and a mark on settings set for the current scope.
- **R4 library:** unread badges and a continue button on covers; one filter / sort / display sheet (needs server fields: unread count, continue chapter, last read, latest chapter).
- 2026-10-12: **R1 done** (web `2db8c9d`): one summary line with icon buttons (mark read, download menu, filter/sort/display sheet, select, ⋯), plain rows with unread bright and read dimmed, select mode with a floating action pill; view in the URL and remembered per user.
- 2026-10-12: **R2 done** (web `d37c44d`): bookmarks in the row menu, batch, a Bookmarked filter, a mark on rows, a toggle in the reader; synced across devices.
- 2026-10-12: **R3 done** (web `d132205`): a 48 px top bar (back, series and chapter, bookmark, ⋯) and a bottom bar (slider with previous/next, chapters sheet, one-tap layout switch saved for the series, settings) that hide while reading; one settings sheet (Layout, General) with the This series / source / Everywhere switch, markers and per-setting reset. Also fixed: the page list was refetched on every progress save.
- 2026-10-12: **Reader jumps fixed** (IN-0066, web `daa764c`): the strip anchors the page in the middle of the screen and compensates every size change before paint (works on iOS Safari too); placeholders take the shape of the chapter's loaded pages; the previous chapter loads only when you scroll up into the start. Measured: the page being read moves at most 3 px while pages and chapters load (desktop, phone, WebKit).

