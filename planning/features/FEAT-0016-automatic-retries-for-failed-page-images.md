---
title: "FEAT-0016: Automatic retries for failed page images"
status: accepted
tags: [feature, web, server, plugins, reader, network]
related: [planning/features/FEAT-0006-mobile-first-reader.md, planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md, planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md, planning/features/FEAT-0012-reader-series-page-and-library-polish.md]
inputs: [IN-0079, IN-0080]
milestone: ""
priority: P2
updated: 2026-10-18
---

# FEAT-0016: Automatic retries for failed page images

## Problem

The owner (IN-0079): "one thing i can think for source like SITE_A to try reload the failed image in extension settings or etc"

Some sites fail single page images now and then. Today nothing retries them on its own (checked 2026-10-18):
- the reader shows "Page N didn't load" with a manual **Try again** (web `src/features/reader/page-image.tsx`);
- source-mihon retries only while mihon-source itself can't be reached, and only before any bytes are sent;
- mihon-source re-sends a request only after solving a challenge.

## Outcome

A failed page image is tried again a few times by itself before the reader shows **Try again**. An admin can tune this per extension or source in its settings in Panelarr's admin, so a flaky site gets more attempts.

## Scope

- **In:**
  - retries in the **server's** image fetch, so the reader and downloads both get them (IN-0080);
  - a default of **2 more attempts, after 1 s then 3 s** (IN-0080);
  - set on an **extension** (for all its sources), with an optional override on **one of its sources** (IN-0080), shown with the extension's other settings in Panelarr's admin (FEAT-0009, FEAT-0010);
  - retries only for errors worth retrying (timeouts, 5xx, dropped connections), honouring the site's retry-after and the per-source rate limits; never for 404 or a rejected key;
  - the reader keeps its manual **Try again** for when the automatic attempts run out.
- **Out:** retrying page *lists* or chapter lists (those already show the error with Retry, FEAT-0012); switching to another copy of the chapter (FEAT-0011).

## Acceptance criteria

- [ ] AC1: With a source whose images fail once and then succeed, the page shows without the user tapping anything.
- [ ] AC2: An admin sets attempts on an extension and all its sources use them; an override on one source wins for that source; sources without either use the default (2 attempts, 1 s then 3 s).
- [ ] AC3: A 404 image isn't retried; the reader shows **Try again** at once.
- [ ] AC4: Retries respect the source's rate limit and retry-after.
- [ ] AC5: Downloads get the same retries.

## Design notes

In the server's image fetch, which already knows each source's limits and serves every client. The setting is stored per extension (package) and per source, like network profile assignments (`plugin:package`, FEAT-0010). The server session proposes the exact shape.

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| server | [GOAL-0022](../../agents/goals/GOAL-0022-server-automatic-retries-for-failed-page-images.md) | | S1 retries done (`9d3ddaa`); S2 settings next |
| web | [GOAL-0023](../../agents/goals/GOAL-0023-web-image-retry-settings-in-the-extension-admin.md) | | not started |

## Decisions

- 2026-10-18 (IN-0080): retries live in the server; default 2 more attempts after 1 s then 3 s; set per extension (all its sources) with a per-source override.
