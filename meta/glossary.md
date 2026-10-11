---
title: Glossary
status: draft
tags: [meta, glossary]
related: [meta/conventions.md]
updated: 2026-10-11
---

# Glossary

Terms with a specific meaning in Panelarr and in this KB. Add a term the first time it appears with a meaning that a newcomer could get wrong.

## Project terms

| Term | Meaning |
|---|---|
| **Work** | The canonical series in Panelarr (one manga/manhwa/comic), independent of where it comes from. Optionally linked to a metadata record. |
| **Source** | One site or catalogue that a source plugin can browse, e.g. a single Mihon extension source or a local folder root. ID: `plugin:sourceId`. |
| **SourceSeries** | A Work as it appears on one Source. A Work has one or more. |
| **SourceChapter / Chapter** | A chapter as listed by one source, versus the canonical chapter of a Work (number/volume) chosen among variants. |
| **Plugin** | An out-of-process extension that Panelarr hosts. Kinds: `source`, `metadata` (maybe `tracker` later). None installed by default. |
| **Plugin index** | A JSON list of installable plugins (versions, per-arch binaries, checksums, signing keys) that a hoster adds by URL. |
| **Provider** | Loose word for "whatever supplies something" (source provider, metadata provider). Prefer *source plugin* / *metadata plugin*. |
| **Mihon extension** | An Android APK/jar built for Mihon/Tachiyomi (e.g. the EXTREPO collection). Run by **mihon-source**. |
| **Extension store** | Mihon's index of extensions (`repo.json` → `index.pb`/JSON, legacy `index.min.json`). Handled by **source-mihon**. |
| **Network profile** | Named per-source networking settings: proxy, solver (FlareSolverr/Byparr), rate limit, UA, DoH, cookies. |
| **Solver** | A service that clears anti-bot challenges (FlareSolverr, Byparr). |
| **Shared store** | The single on-disk copy of downloaded chapters, shared by all users ([ADR-0003](../decisions/ADR-0003-shared-store-per-user-libraries.md)). |
| **Library (per user)** | The Works one user follows, with their categories, progress and trackers. |
| **Tracker** | An external progress service (AniList, MAL, …) bound per user and per Work. |
| **Search backend** | The engine behind search: built-in DB full-text (default), Typesense, Meilisearch. |
| **Hoster** | The person running a Panelarr instance and choosing which optional parts to run. |
| **EXTREPO** | Alias for a large community collection of Mihon extensions. Real name in `.kb-aliases.env`. Never link to it ([ADR-0020](../decisions/ADR-0020-public-kb-with-aliases.md)) |

## KB terms

| Term | Meaning |
|---|---|
| **Owner** | The human who decides. Only the owner makes knowledge `accepted` |
| **Operator** | The person running the agent sessions day to day. Often the owner |
| **Keeper** | The agent session that curates this KB and performs the roles in `playbooks/` |
| **Consumer** | Any other session or contributor. Reads the KB and messages the keeper |
| **Input** | The owner's words, kept verbatim (`IN-NNNN`) |
| **ADR** | Architecture/any decision record (`ADR-NNNN`). Append-only |
| **Goal** | A brief with a Definition of Done, dispatched to a coding session (`GOAL-NNNN`) |
| **Feature** | A unit of product scope with acceptance criteria (`FEAT-NNNN`) |
| **Digest** | A snapshot of open issues and PRs across repos (`ops/digests/`) |
| **Outbox** | Drafted forge actions waiting for approval (`ops/outbox/`) |
| **Working assumption** | A consumer's proposed answer to an open question, built cheap to change and not yet decided |
| **Alias** | A short stand-in (e.g. `FB`) for a confidential term. Real terms live only in the git-ignored `.kb-aliases.env` |
| **Ops round** | One pass of the scheduled loop: digest, triage, reviews, board, report |
