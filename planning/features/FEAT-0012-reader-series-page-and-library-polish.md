---
title: "FEAT-0012: Reader, series page and library polish"
status: accepted
tags: [feature, web, reader, library, ux]
related: [planning/features/FEAT-0006-mobile-first-reader.md, planning/features/FEAT-0005-unified-chapters-and-update-checks.md, modules/web/overview.md]
inputs: [IN-0083, IN-0081, IN-0060, IN-0061]
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
| web | — | — | done (`647cb99` … `645caa3`; [test report](../../qa/reports/feat-0012-reader-series-library-verification.md)) |
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
- 2026-10-12: server fields for R4 done (`ac8875e`): LibraryEntry chapters, unread, downloaded, started, continue_chapter_id, last_read_at, latest_chapter_at.
- 2026-10-12: chapter labels use the server's `display_title` (web `06c718a`): "Vol. 1 · Chapter 1: Double Dungeon", or "Chapter 192" when there's no name; in rows, the reader bar, the chapter sheet and the bands.
- 2026-10-12: **R4 done** (web `645caa3`): unread badges and continue buttons on covers, one filter / sort / display sheet, sort and layout saved per user. Verified on a clean clone; feature delivered.
- 2026-10-18: **Flicker on a real iPhone fixed** (IN-0068, IN-0070; web `c052bd1`): a loaded page that left the loading window lost its image and collapsed (577 → 96 px), which moved everything below and could flip the current page back and forth. Loaded pages now keep their image, and known pages show at once when scrolled back. Measured in the iOS Simulator (Mobile Safari, real touches): no one-frame jumps, no image taken away.
- 2026-10-18: **Reader errors** (IN-0068, web `4ce796b`): a source failure shows the server's reason at once (no automatic retries for it), with Retry, Back to the series (when known), Back and Library; a note after 8 s if a chapter is slow to open.
- 2026-10-18: server `8a13bb6`: a failed chapter-pages request names the series and chapter (work_id, work_title, chapter_label) when the caller may see it, so the reader can always offer Back to the series.
- 2026-10-18: **Home Screen app** (IN-0068 item 1, IN-0069, IN-0076; web `4654cc3`): iOS starts an installed web app with a layout viewport short by the status bar's height (812 of 874 pt), leaving an unpainted band under the bottom nav; the body is now at least the full screen tall in the installed app (checked on iPhone 16 Pro and 16e). No "Panelarr" header on phones; a thin blurred strip under the status bar; the top inset capped so a wrong value can't open a band. The owner's top band couldn't be reproduced; it came from the old header's top padding, which is gone.
- 2026-10-18: **Compact series page on phones** (IN-0071, web `b753025`): a top bar with back, title (once scrolled) and ⋯; a smaller cover; chapter rows edge to edge with one name line and one meta line; copy reasons only in the copies list; a floating Continue / Start button. About 10 chapters fit on an iPhone 16 Pro (before about 6).
- 2026-10-18: library search behind an icon on phones (IN-0075, web `2565c48`); "Back to the series" from the pages problem's work_id (`ff7d11f`).
- 2026-10-18: **Seams and sticky scrolling up fixed** (IN-0077, IN-0078; web `3f7b93f`): strip pages get exact whole-pixel heights (the virtualizer rounded, leaving hairline gaps: 32 before, 0 after); while the user scrolls, the anchor corrects with a transform and folds it into scrollTop once scrolling settles, so iOS momentum isn't killed (flings up went from about 500 px to 6,300 px over 10 s, like down). Measured in the iOS Simulator with real flings.
- 2026-10-18: regression from `3f7b93f` fixed (`6bedb02`): near the ends of the loaded strip the browser clamps scrollTop itself, so the deferred correction doubled it (a jump of about a page); there the strip corrects directly again, and the reader's position counts any pending correction. Proven with repeated runs (18/18 phone, 20/20 desktop).
- 2026-10-18: **R5 asked** (IN-0081): (a) a Browse item already in the library opens its library page, and **Add to library** moves to the new library page; (b) in the long strip, opening a chapter in the middle (e.g. 45) and scrolling up should bring in the previous chapter more smoothly. Handed to `panelarr-web`.
- 2026-10-18: **R5 (a) done** (web `621c97a`): a Browse card for a work in the library opens its series page; Add to library moves to the new series page (replacing the catalogue page, so Back returns to Browse). The catalogue page itself doesn't redirect, because it is the series' Details view (Details on desktop, ⋯ on phones); it keeps its "In your library" link.
- 2026-10-18: **R5 (b) done** (web `6a8b95f`): the previous chapter is fetched as soon as the reader is within the first 5 pages of the first loaded chapter, and added above only while the strip is still (adding it mid-fling would stop the fling on iOS); scrolling to the very top still asks for it. iOS Simulator, Chapter 12 opened at its start: before, the first fling up stopped dead after 108 px and Chapter 11 came 1.7 s later; after, Chapter 11 was already above and the fling ran through the band in one motion, no jumps or blank frames over about 600 frames. Strip specs 30/30 on phone and desktop. Known limit: with page heights far from the guesses, a long fling may still stop briefly at the top.
- 2026-10-22: **Bug** (IN-0083): in a long strip, "Pages to load ahead" has no effect: the strip loads a fixed 2 pages past the first one still loading (`AHEAD = 2`, `strip-viewer.tsx`); only the paged reader honours the setting. Handed to `panelarr-web`.
