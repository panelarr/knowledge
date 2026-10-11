---
title: "ADR-0003: Shared content store, per-user libraries"
status: accepted
tags: [multi-user, storage]
related: [architecture/multi-user.md, architecture/storage-layout.md, architecture/domain-model.md]
inputs: [IN-0002, IN-0003]
updated: 2026-10-11
---

# ADR-0003: Shared content store, per-user libraries

- **Date:** 2026-10-11 · **Deciders:** author

## Context
With Suwayomi, three people means three instances, because content can't be shared across separate libraries (IN-0002).

## Decision
- **One copy on disk** of every downloaded chapter, shared by all users.
- **Per user:** library entries, categories, read progress and history, tracker accounts and bindings, content-rating ceiling, permissions and quotas.
- If two users follow the same Work, it is fetched and stored once.

## Consequences
- **Ownership checks happen at the API level:** a user may read a file only if they may see the Work.
- **Deleting content** is an admin or retention-policy action, never a side effect of one user removing a Work from their library.

## Alternatives considered
| Option | Why not |
|---|---|
| One shared library (Komga-style) | Users want their own lists |
| Fully separate per-user stores | Duplicates content, which is the Suwayomi problem |
