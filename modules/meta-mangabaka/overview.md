---
title: meta-mangabaka overview
status: draft
tags: [module, meta-mangabaka, metadata, mangabaka, go]
related: [modules/meta/overview.md, contracts/metadata-plugin.md, research/mangabaka.md]
inputs: [IN-0009]
updated: 2026-10-11
---

# meta-mangabaka

## Summary

The first metadata plugin (IN-0009 §1). It implements `panelarr.metadata.v1` with the `meta` SDK and feeds meta from **MangaBaka**: a `dump` ingestion from the nightly SQLite dump, and a `lookup` ingestion through the REST API for freshness ([research](../../research/mangabaka.md)). One repo per plugin (Q-0017).

## Ingestion
- **`dump`:**
  1. download the dump the hoster chose (default or full variant), with resume where possible;
  2. verify the published `.sha1`; decompress zstd;
  3. open the SQLite file read-only (pure-Go driver, no cgo);
  4. map each series to the normalized record, keeping raw fields as extras;
  5. stream `Sync` events: upserts, `merged_with` → merge events, checkpoints.
- **`lookup`:** `Search` and `Get` against the API, within its limits (search 30/min, other GETs 180/min per IP) and backing off on 429.
- **Common services:** may use the main app's network profiles for downloads and API calls (IN-0007).

## Owns / doesn't own
- **Owns:** MangaBaka URLs, download, checksum, decompression, the dump schema mapping, API client, attribution text.
- **Doesn't own:** the metadata DB, scheduling, browse/search (all meta).

## Licence and data
MangaBaka data is CC BY-NC-SA 4.0. The plugin downloads it on the hoster's instruction; no dump or extract is ever committed, bundled or published. Tests use synthetic fixtures.

## Implementation status
Not started. Part of [GOAL-0002](../../agents/goals/GOAL-0002-meta-v0-metadata-protocol-meta-service-and-mangabaka-dump-in.md).
