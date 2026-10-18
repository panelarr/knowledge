---
title: "FEAT-0016: Automatic retries for failed page images"
status: proposed
tags: [feature, web, server, plugins, reader, network]
related: [planning/features/FEAT-0006-mobile-first-reader.md, planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md, planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md, planning/features/FEAT-0012-reader-series-page-and-library-polish.md]
inputs: [IN-0079]
milestone: ""
priority: P3
updated: 2026-10-18
---

# FEAT-0016: Automatic retries for failed page images

## Problem

The owner (IN-0079): "one thing i can think for source like SITE_A to try reload the failed image in extension settings or etc"

Some sites fail single page images now and then. Today nothing retries them on its own (checked 2026-10-18):
- the reader shows "Page N didn't load" with a manual **Try again** (web `src/features/reader/page-image.tsx`);
- source-mihon retries only while mihon-source itself can't be reached, and only before any bytes are sent;
- mihon-source re-sends a request only after solving a challenge.

## Outcome (suggested)

A failed page image is tried again a few times by itself before the reader shows **Try again**. An admin can tune this per extension or source in its settings in Panelarr's admin, so a flaky site gets more attempts.

## Scope (suggested)

- **In:**
  - a per-source (or per-extension) setting: retry attempts and delay, with a sensible default; shown with the extension's other settings in Panelarr's admin (FEAT-0009, FEAT-0010);
  - retries only for errors worth retrying (timeouts, 5xx, dropped connections), honouring the site's retry-after and the per-source rate limits; never for 404 or a rejected key;
  - the reader keeps its manual **Try again** for when the automatic attempts run out.
- **Out:** retrying page *lists* or chapter lists (those already show the error with Retry, FEAT-0012); switching to another copy of the chapter (FEAT-0011).

## Acceptance criteria (draft)

- [ ] AC1: With a source whose images fail once and then succeed, the page shows without the user tapping anything.
- [ ] AC2: An admin can change the attempts for one source; another source keeps the default.
- [ ] AC3: A 404 image isn't retried; the reader shows **Try again** at once.
- [ ] AC4: Retries respect the source's rate limit and retry-after.

## Design notes

Where the retries live is to be settled (see the open questions). Suggestion: in the server's image fetch, which already knows each source's limits and serves every client (web, downloads), with the setting stored per source next to the network profile choice (FEAT-0010); a plugin could offer a default through its settings.

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| | | | |

## Open questions

- Retries in the server (one place, also covers downloads) or in each source plugin (where the site's own setting lives)? Suggestion: server.
- Default attempts and delay? Suggestion: 2 more attempts, 1 s then 3 s.
- Per source, per extension, or both (extension default, source override)?
