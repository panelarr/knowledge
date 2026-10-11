---
title: Storage layout
status: proposed
tags: [architecture, storage, files]
related: [decisions/ADR-0015-cbz-comicinfo-storage.md, research/comic-archive-formats.md, architecture/domain-model.md]
inputs: [IN-0002]
updated: 2026-10-11
---

# Storage layout

## Summary

Two volumes, like other *arr* apps: **`/config`** (DB, plugins, caches, settings) and **`/data`** (library). Downloaded chapters are **CBZ + ComicInfo.xml** in a human-readable tree ([ADR-0015](../decisions/ADR-0015-cbz-comicinfo-storage.md), proposed). User folders read by source-local are mounted **read-only** and never modified.

```
/config/
  plugins/<id>/<version>/     # managed plugin binaries + data dir
  cache/covers/  cache/pages/ # rebuildable
  search/                     # embedded index (if Bleve), rebuildable
  logs/
/data/
  library/
    <Work Title> [<work-id>]/
      cover.jpg
      Vol.01 Ch.0001 - <title> [<scanlator>].cbz
      Ch.0012.5 [<scanlator>].cbz
  import/                     # drop zone for adopting files (optional)
/media/manga  (example, read-only)  # user collections for source-local
```

## Rules
- **Naming:** the template is configurable (`{work}/{vol} {ch} - {title} [{group}].cbz`). Names are sanitised for SMB/NTFS. The `[work-id]` suffix avoids title collisions and survives renames.
- **Archives:** CBZ is *stored* (no compression). Pages are named `0001.ext`. ComicInfo.xml carries Series, Number, Volume, Title, Writer, Summary, Genre, LanguageISO, Web, Manga (RTL), AgeRating and Panelarr IDs in custom fields.
- **Atomic writes:** download to `…/.tmp`, verify, then rename. The SHA-256 is recorded in `ChapterFile`.
- **Adopting user files** (source-local → library): copy (default) or move, behind an explicit admin action.
- **Hard links:** possible when source and destination share a filesystem (*arr* convention).
- **Image post-processing** (optional, per rule): split double pages, convert to WebP/AVIF, strip junk pages (later).
