---
title: "FEAT-0017: Import reading history from other apps"
status: proposed
tags: [feature, server, web, history, import]
related: [planning/features/FEAT-0014-reading-history.md, planning/features/FEAT-0004-add-a-work-from-meta-and-match-sources.md, research/suwayomi-server.md]
inputs: [IN-0082]
milestone: ""
priority: P2
updated: 2026-10-18
---

# FEAT-0017: Import reading history from other apps

## Problem

The owner (IN-0082): "also one feature we should add is import of history, like from suwayomi/aidoku and etc (suwayomi is first one done, aidoku can be done later on)"

People coming to Panelarr already have years of reading in another app. Without an import, their History is empty and every chapter shows as unread.

## Outcome

A user imports their reading from another app, and Panelarr's History, read marks and "continue" pick up where they left off. **Suwayomi comes first**; Aidoku comes later (IN-0082), and more apps can follow.

## Scope (suggested)

- **In:**
  - one importer per app behind a common shape (read the export → match series → apply), Suwayomi first;
  - per user: each user imports into their own history and read marks; adding missing works to the library follows the user's add permission;
  - matching each imported series to a Panelarr work: by its source and URL when the source exists in Panelarr (Suwayomi uses Mihon extensions, so the same source IDs may apply **[unverified]**), else by title through meta, like adding from a source (FEAT-0004);
  - a preview before applying (matched, needs a choice, not found), and a summary afterwards; series that weren't matched can be matched by hand later;
  - safe to repeat: importing twice doesn't duplicate anything, and newer progress in Panelarr isn't overwritten by older imported progress.
- **Out (for now):** Aidoku (later, IN-0082); writing back to the other app; tracker syncing (later, IN-0074).

## Acceptance criteria (draft)

- [ ] AC1: Importing a Suwayomi export marks the same chapters read and fills History with the last-read times.
- [ ] AC2: Series whose source is in Panelarr match without asking; others go through meta, and the rest are listed for the user.
- [ ] AC3: Importing the same export again changes nothing.
- [ ] AC4: Progress newer in Panelarr than in the export is kept.
- [ ] AC5: One user's import doesn't touch another user's history.

## Design notes

To research before building: Suwayomi's backup format and its GraphQL API (what holds history, read marks and last-read times) **[unverified]**; Aidoku's backup format later.

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| | | | |

## Open questions

- How does the data come in: upload Suwayomi's **backup file**, or connect to a running **Suwayomi server** by URL? Suggestion: the backup file first (works offline and the same way for Aidoku later); a live connection could come after.
- What to import besides history and read marks: library entries, bookmarks, categories? Suggestion: history, read marks and bookmarks, and add the series to the library; categories later.
- Who may import: every user for themselves, or admins only? Suggestion: every user for themselves.
