---
title: "FEAT-0014: Reading history"
status: accepted
tags: [feature, web, server, reader]
related: [planning/features/FEAT-0012-reader-series-page-and-library-polish.md, contracts/server-api.md]
inputs: [IN-0072]
milestone: ""
priority: P1
updated: 2026-10-18
---

# FEAT-0014: Reading history

## Problem

"also we need history tab/tracking so u could see what u read before" (IN-0072). The server already records reading progress and answers `GET /me/history` ("Chapters you read, newest first"), but the web app has no page for it.

## Outcome

Each user has a **History** tab: what they read, newest first, grouped by day, one line per series with the last chapter read and when, a cover, and a tap to resume. They can remove an entry or clear their history.

## Scope

- **In:**
  - a History tab in the main navigation (phone bottom nav and desktop sidebar);
  - entries grouped by day (Today, Yesterday, dates), each with the cover, series title, the last chapter read ("Chapter 200 · page 13 of 117"), the time, and Resume;
  - one entry per series by default (the latest chapter read), with a way to see every chapter read (per series or as a toggle);
  - search within history;
  - remove one entry (that series from history, keeping read marks), and clear all, both with a confirmation;
  - per user; never shown to other users.
- **Out (for now):** external trackers such as AniList or MyAnimeList (Q-0021 is still open; "tracking" here means the reading history).

## Acceptance criteria

- [ ] AC1: After reading, the series appears at the top of History with the chapter and page and the time; tapping it resumes there.
- [ ] AC2: History is grouped by day and paged; it works on a phone with the compact layout.
- [ ] AC3: Removing an entry hides that series from history without changing its read marks; clearing removes all, after confirmation.
- [ ] AC4: One user's history is never visible to another.

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| server | — | — | check `/me/history` covers grouping per series, removal and clearing |
| web | — | — | History tab, after the mobile fixes (IN-0068..IN-0071) |

## Open questions

- Should "tracking" also mean syncing with external trackers (AniList, MyAnimeList)? Kept out until the owner says (Q-0021).
