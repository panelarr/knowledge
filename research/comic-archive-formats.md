---
title: Comic archive and e-book formats
status: draft
tags: [research, files, local]
related: [modules/source-local/overview.md, architecture/storage-layout.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# Comic archive and e-book formats

> Compiled 2026-10-11 from general knowledge.

## Summary

Users' own collections ([IN-0003](../inputs/IN-0003-architecture-round-1.md) §3.5) are mostly **comic book archives**: renamed archive files containing page images in reading order.

| Ext | Container | Notes |
|---|---|---|
| **.cbz** | ZIP | Most common. Panelarr's own download format. Go stdlib `archive/zip` |
| **.cbr** | RAR | Very common in older collections. Read-only via a pure-Go RAR reader (e.g. `rardecode`) **[unverified]** |
| **.cb7** | 7z | Less common. Needs a 7z reader (pure-Go libraries exist **[unverified]**) |
| **.cbt** | TAR | Rare. Go stdlib `archive/tar` |
| folder of images | — | Common for rips |
| **.epub** | ZIP + XHTML | Often used for manga volumes (fixed layout). Extract images from the spine |
| **.pdf** | PDF | Needs rasterization (e.g. a pdfium/mupdf binding) → may come later ([Q-0018](../questions/README.md)) |

## ComicInfo.xml
- The Anansi Project schema (v2.0/2.1) lives at the archive root. Fields include Series, Number, Volume, Title, Summary, Writer, Penciller, Genre, Tags, LanguageISO, Manga (YesAndRightToLeft), AgeRating, Web, GTIN and more.
- Panelarr **writes** it into every downloaded CBZ and **reads** it in source-local.

## Naming conventions (no ComicInfo)
- Common patterns: `Series Name v01 c001`, `Series - Chapter 12.5`, `[Group] Series - c012 (v02)`, and folder = series.
- Inference rules are open ([Q-0019](../questions/README.md)).
