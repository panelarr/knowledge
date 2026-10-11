---
title: "FEAT-0007: Downloads to the shared library"
status: proposed
tags: [feature, server, web, m2]
related: [decisions/ADR-0003-shared-store-per-user-libraries.md, decisions/ADR-0015-cbz-comicinfo-storage.md, architecture/storage-layout.md]
inputs: [IN-0003, IN-0037]
milestone: "M2"
priority: P1
updated: 2026-10-11
---

# FEAT-0007: Downloads to the shared library

## Problem

The first slice is add → read → **download** (IN-0037 §2). Downloads are stored once and shared ([ADR-0003](../../decisions/ADR-0003-shared-store-per-user-libraries.md)) as CBZ + ComicInfo ([ADR-0015](../../decisions/ADR-0015-cbz-comicinfo-storage.md), proposed).

## Outcome

A user with permission downloads chapters (one, a range, all unread, or automatically for new chapters). The server fetches them through the source plugin using the chosen variant, writes CBZ files to the library, and serves them to the reader.

## Scope

- **In:**
  - a download queue in the server (one shared item per chapter, de-duplicated, retries with back-off, per-source concurrency, rate limits respected);
  - CBZ + ComicInfo writer (atomic writes, SHA-256);
  - naming template; ChapterFile records;
  - "download new chapters" per library entry;
  - a downloads page with progress over SSE;
  - downloads as jobs in the Jobs page model.
- **Out:** image post-processing (later), hard links and adopt-from-local (source-local, later), quotas (later).

## Acceptance criteria

- [ ] AC1: Queuing a chapter that's already downloaded or queued by anyone does nothing new; the file exists once.
- [ ] AC2: A download fetches pages through the chosen variant's source plugin, writes `….tmp` then renames, records pages, size and SHA-256, and retries failures with back-off; a failed page fails the chapter cleanly (no partial file left).
- [ ] AC3: Files land at the configured template path with ComicInfo.xml (series, number, volume, title, writer, summary, genres, language, web, manga RTL, age rating, Panelarr IDs).
- [ ] AC4: Per-source concurrency and rate limits are respected across all users' downloads.
- [ ] AC5: "Download new chapters" on a library entry queues new chapters after update checks.
- [ ] AC6: The downloads page shows queue, progress and failures live (SSE); admins can pause, retry and cancel.
- [ ] AC7: The reader serves downloaded chapters from the CBZ.

## Design notes

[storage layout](../../architecture/storage-layout.md), [domain model](../../architecture/domain-model.md) (ChapterFile).

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| server, web | — | — | — |

## Open questions

- None yet.
