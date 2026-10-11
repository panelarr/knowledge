---
title: MangaBaka database and API
status: draft
tags: [research, metadata, mangabaka]
related: [research/metadata-providers.md, modules/meta/overview.md]
inputs: [IN-0002]
updated: 2026-10-11
---

# MangaBaka database and API

> Checked on 2026-10-11 (mangabaka.org/data/database, live `GET /v1/series/1`).

## Summary

MangaBaka is an aggregated manga metadata database. It publishes **nightly dumps** (JSON, JSONL, SQLite) and a **REST API** (OpenAPI 3.1). Its cross-reference of external IDs (AniList, MAL, MangaUpdates, Kitsu…) makes it the natural **backbone** for the `meta-mangabaka` plugin. Its licence (**CC BY-NC-SA 4.0**) means Panelarr must never redistribute it: each hoster downloads it.

## Dumps
- **URL:** `https://api.mangabaka.org/v1/database/series[.full].{json,jsonl,sqlite}.{tar.gz,zst}`, each with a `.sha1`.
- **Variants:** *default*, and *full* (adds raw upstream responses in `*_response` fields).
- **Size (measured 2026-10-11, default variant):** about 396 MB as `.sqlite.zst`, 3.4 GB decompressed; 564,040 series rows, of which 258,029 are merged into others and 306,008 active. Reading and mapping them all took about 1.5 minutes on the owner's machine. **Full import into meta (measured 2026-10-11, IN-0029):** 13m23s for 564,155 records (402,155 changed after a resumed run, 258,068 merges), **306,084 active entries**, **meta database 6.6 GB** (the synthetic projection said 4–5 GB; raw JSONB is the likely difference). The first attempt failed when Docker Desktop's disk filled. Plan disk for about 7 GB of database plus about 4 GB of dump files.
- **Freshness:** built nightly at 00:00 UTC. Each series refreshes every 1–7 days; the whole database weekly. Sizes aren't published.
- **Schema stability:** no 1.0 promise; changes are "likely additive". Code defensively.
- **Licence:** MangaBaka's own data is CC BY-NC-SA 4.0. Third-party data stays under each provider's terms. Attribution is expected, and commercial use needs an arrangement.

## Series schema highlights
- **Identity:** `id`, `state` (active/merged), `merged_with`. Follow merges.
- **Titles:** `title`, `native_title`, `romanized_title`, `titles[]` (`{language, traits, title, note, is_primary}`), `secondary_titles`. This feeds [search](../architecture/search.md).
- **People:** `authors[]`, `artists[]` (plain strings), `publishers`.
- **Covers:** raw plus 150/250/350 widths at x1–x3, with **blurhash/thumbhash**. Handy for SPA placeholders.
- **Classification:** `genres`, `tags`, `tags_v2` (hierarchical, with spoiler/explicit flags), `content_rating`, `type`, `original_language`.
- **Publication:** `status`, `year`, `published`, `final_volume`, `total_chapters`, `is_licensed`, `rating`, `popularity`, `links_v2`, `relationships_v2`, `anime`.
- **`source` map:** anilist, anime_planet, anime_news_network, kitsu, manga_updates, my_anime_list, shikimori. **No MangaDex ID.**
- **Characters:** none in the schema seen. Character data must come from another plugin, e.g. AniList ([Q-0023](../questions/README.md)).

## API
- **Base:** `https://api.mangabaka.org/`, with an explorer at `/data/api/explorer` and an MCP endpoint at `/data/mcp`.
- **Rate limits:** per-IP leaky bucket, applied only to uncached responses (`cf-cache-status: HIT` is free). Over the limit returns 429.

| Endpoint | Limit |
|---|---|
| `GET /series/search` | 30/min |
| Other `GET`s | 180/min |
| `/my/*` | 180/min (never cached) |

- **Tracker:** MangaBaka is also a **tracker** in Mihon (OAuth2) ([trackers](trackers.md)).

## What it means for Panelarr
- `meta-mangabaka` imports the SQLite dump (zstd) on a schedule chosen by the hoster, and diffs by `id`, honouring `merged_with`. It uses the API only for on-demand freshness.
- The UI shows attribution wherever MangaBaka data appears.

## Sources
- https://mangabaka.org/data/database · https://mangabaka.org/data/api · https://api.mangabaka.org/v1/series/1
