---
title: "GOAL-0022: server: automatic retries for failed page images"
status: accepted
tags: [goal, agents, server]
related: [planning/features/FEAT-0016-automatic-retries-for-failed-page-images.md, planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md, contracts/source-plugin.md]
inputs: [IN-0079, IN-0080]
repos: [server]
session: "panelarr-server"
features: [FEAT-0016]
updated: 2026-10-18
---

# GOAL-0022: server: automatic retries for failed page images

The brief a coding session works from. Read this file and follow it.

## Status

`accepted`, **Done 2026-10-18** (verified, pass; [test report](../../qa/reports/goal-0022-server-image-retries-done-verification.md)). The owner accepted [FEAT-0016](../../planning/features/FEAT-0016-automatic-retries-for-failed-page-images.md) (IN-0080).

## Context

- Read [FEAT-0016](../../planning/features/FEAT-0016-automatic-retries-for-failed-page-images.md) and [contracts/source-plugin.md](../../contracts/source-plugin.md).
- **Decided (IN-0080):** retries live in the server; the default is 2 more attempts, after 1 s then 3 s; set on an extension (package, all its sources) with an optional override on one of its sources.
- Today a failed image reaches the reader at once (web shows "Try again"); source-mihon retries only while mihon-source is unreachable.
- Same working rules as before: slices, gated checks, merge to local main, never push, `REPORT:` per slice; every merge is redeployed for the owner (IN-0056). Live checks on the owner's stack never change the owner's settings or progress: use a throwaway user and put back anything you change.

## Objective

In the server's image fetch (reader pages and downloads): retry a failed image fetch for errors worth retrying (timeouts, unavailable, 5xx-like, dropped streams before any bytes), never for not found or a rejected key; honour retry-after and the per-source limits; resolve the attempts and delays from source override → extension → default. An admin API to read and set it for an extension and for a source (with the effective value and where it came from), shaped like the network assignments. PROPOSE the shape (storage, API, error classes) before building.

## Definition of Done

- [x] Retries for reader images and downloads, with the resolution order
- [x] Admin API for extension and source, with `effective` and its origin; OpenAPI updated
- [x] Tests: fail-once-then-succeed, not-found not retried, override wins, rate limit respected
- [x] Docs; checks green; leak-check clean
- [x] `DONE:` with evidence per box

## History

- 2026-10-18: brief written from the accepted FEAT-0016.
- 2026-10-18: plan PROPOSEd and accepted by the keeper.
  - One helper `Host.PageImage`, used by the reader's page images and by downloads (covers, icons and browsing stay as they are). Every attempt waits on the per-source image limiter; cancel stops the retries. The image is buffered, so a stream that drops part-way is safe to retry.
  - Retried: Unavailable, DeadlineExceeded, Aborted, Internal, Unknown, SOURCE_DOWN; RATE_LIMITED waits max(next delay, retry_after), and gives up when retry_after is over 30 s (downloads then retry later as a task, as today).
  - Never retried: not found, rejected key or login, bad input or precondition, unsupported, a site challenge (the plugin's solver handles it), too large or not an image, and the server's own errors.
  - The setting is `delays_ms` (default [1000, 3000]; [] means off; at most 5 entries of 0–30000 ms), stored in `image_retry_settings` by target (package `plugin:package` or source) and resolved source → its package → default, cached in memory.
  - API: GET/PUT/DELETE `/plugins/{plugin_id}/packages/{package_id}/image-retries` and `/sources/{source_id}/image-retries`, answering `own`, `effective`, `level` and `from_target_id`; changes are audit-logged; a metric `panelarr_image_retries_total{outcome}`.
  - Slices: S1 the retries, S2 the setting and API.
  - Keeper answers: the 30 s retry_after cap is fine; a challenge stays out of the retry list.
- 2026-10-18: REPORT: **S1 done** (`0913f34`, merge `9d3ddaa`): `Host.PageImage` (internal/plugins/retry.go) for reader pages and downloads; default [1 s, 3 s] paced by the source's image limiter, stopped by cancellation; the agreed error classes (a stream broken off at any point is retried, since the image is buffered); downloads keep their task back-off afterwards; a metric by outcome; debug logs with the error class only. Tests per case with call and wait counts, plus an API test (reader page 200 and a download with the real default; 502 with retries off). Docs in reader.md and downloads.md.
- 2026-10-18: REPORT: **S2 done** (`1217f9d`, merge `6ff0878`): migration 00018 `image_retry_settings`; source → package → default, cached a minute and dropped on writes; the six admin operations with `own` / `effective` / `level` / `from_target_id` ([] = off, absent = inherits); audit-logged. DONE received and verified on a clean clone (`make check`, gen-check, api-breaking). Goal closed.
