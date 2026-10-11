---
title: source-local overview
status: draft
tags: [module, source-local, files, go]
related: [research/comic-archive-formats.md, architecture/storage-layout.md, contracts/source-plugin.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# source-local

## Summary

A source plugin (Go) for the **user's own files**: "another source could be users own manga and etc files" (IN-0003 §3.5). It reads mounted folders **read-only** and presents them through `panelarr.source.v1`, so local series can be added to libraries, matched to metadata, tracked and read like any other.

## Formats ([research](../../research/comic-archive-formats.md))
- **First:** CBZ (zip), CBR (rar), CB7 (7z), CBT (tar), plain image folders.
- **Later:** EPUB (images from the spine), then PDF (rasterization; [Q-0018](../../questions/README.md)).

## Behaviour
- **Sources:** one source per configured root folder (e.g. `local:manga`, `local:comics`). Popular/latest = recently modified; search over the scanned index.
- **Scanning:** periodic scan plus filesystem watch (fsnotify where it works; polling fallback for NFS/SMB). Results are cached in the plugin's data dir.
- **Series and chapter detection:** ComicInfo.xml first, else folder and file naming rules ([Q-0019](../../questions/README.md)). A local `cover.jpg` or the first page becomes the cover.
- **Pages:** `ListPages` enumerates archive entries in natural sort order. `FetchImage` streams the entry.
- **Never** writes to user folders. Adopting into the managed library is a server action ([storage layout](../../architecture/storage-layout.md)).

## Open
- Own repo or a package inside source-api / server? ([Q-0017](../../questions/README.md)). It runs as a managed plugin, but needs the folders mounted where the plugin runs.

## Implementation status
Not started (M2).
