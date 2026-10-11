---
title: "ADR-0015: Store downloaded chapters as CBZ with ComicInfo.xml"
status: proposed
tags: [storage, files]
related: [architecture/storage-layout.md, research/comic-archive-formats.md]
inputs: [IN-0002]
updated: 2026-10-11
---

# ADR-0015: CBZ + ComicInfo.xml storage

- **Date:** 2026-10-11 · **Deciders:** author (proposed)

## Decision (proposed)
- Every downloaded chapter is one **CBZ** (stored, not deflated, for speed), with **ComicInfo.xml** at its root.
- Files live in the shared library tree described in [storage layout](../architecture/storage-layout.md).
- Other readers (Komga, Kavita, Mihon local source) can use the library as-is, and a user can walk away with portable files.

## Alternatives considered
| Option | Why not |
|---|---|
| Loose image folders | Many small files; poor portability |
| Content-addressed blob store | Opaque to users and other tools |
