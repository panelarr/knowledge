---
title: "FEAT-0015: Updates feed"
status: accepted
tags: [feature, web, server, library]
related: [planning/features/FEAT-0014-reading-history.md, planning/features/FEAT-0005-unified-chapters-and-update-checks.md]
inputs: [IN-0073]
milestone: ""
priority: P1
updated: 2026-10-18
---

# FEAT-0015: Updates feed

## Problem

"and updates too" (IN-0073, with a screenshot of the reference app's Updates tab, described there). Panelarr checks for new chapters (FEAT-0005) but has no place listing what's new across the library.

## Outcome

An **Updates** tab lists new chapters in the user's library, newest first, grouped by day, one row per series (cover, title, the newest new chapter) with "Show N more chapters" to expand the rest, a download button, read ones dimmed; "Last update: <time>" with a refresh that runs the update check.

## Scope

- **In:**
  - Updates in the main navigation; the phone bottom nav becomes Library, Updates, History, Browse, More (as in the reference);
  - per user: chapters that appeared in works in that user's library, with when they appeared;
  - one row per series per day, expandable to its other new chapters; tap a chapter to read; download one or all of a row (admins and users allowed to download);
  - read chapters dimmed; marking read from the row;
  - "Last update" time and a refresh that starts the update check (FEAT-0005's job) and shows progress;
  - paging.
- **Out:** notifications (push, email).

## Acceptance criteria

- [ ] AC1: New chapters found by an update check appear in Updates for every user who has that work in their library, grouped by day and series.
- [ ] AC2: "Show N more chapters" expands a row; tapping a chapter opens the reader; read chapters are dimmed.
- [ ] AC3: Refresh runs the update check and the list updates when it finishes; "Last update" shows when it last ran.
- [ ] AC4: Works fine on a phone in the compact layout.

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| server | — | — | an updates feed API (new chapters per user, grouped data, last check time, refresh) |
| web | — | — | Updates tab, after the mobile fixes and History |
