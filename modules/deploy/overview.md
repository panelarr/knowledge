---
title: deploy overview
status: draft
tags: [module, deploy, docker, unraid]
related: [architecture/deployment.md, architecture/repo-standard.md]
inputs: [IN-0002, IN-0003]
updated: 2026-10-11
---

# deploy

## Summary

The public repo for **running Panelarr**:
- a `compose.yaml` with **profiles** for every optional component ([deployment](../../architecture/deployment.md));
- `.env.example`;
- **Unraid Community Applications** templates (one per image);
- later, an **AIO image** (s6-overlay) and maybe Helm.

## Contents (planned)
```
compose.yaml           server + postgres (one server; databases `panelarr` and `meta`, created by an init script), plus profiles: mihon, meta, search-typesense, search-meilisearch, flaresolverr, byparr, vpn
.env.example
unraid/                panelarr-server.xml, panelarr-mihon-source.xml, panelarr-meta.xml, …
aio/                   Dockerfile (later)
docs/                  install guides: Docker, Unraid, reverse proxy, VPN per source
```

## Notes
- The compose example wires gluetun as a proxy target for network profiles ([networking](../../architecture/networking.md)).
- Plugin auto-discovery inside one compose project is an idea ([Q-0027](../../questions/README.md)).

## Implementation status
Not started (M5). Early compose files may appear with M1/M2 for testing.

## Local full stack (2026-10-12)

Until the `deploy` repo exists, the owner has a local Compose setup in `~/Projects/Panelarr/compose` (not a repo), built by `panelarr-meta` (IN-0045, IN-0046): Postgres (databases per service), meta + meta-mangabaka, mihon-source + source-mihon, the server image (its own Dockerfile, with the web app embedded), and profiles for Typesense, Meilisearch, FlareSolverr and gluetun. Admin ports bind to localhost. A smoke test passed: all images built, the services healthy, the setup wizard and admin pages work against the real server, and no Panelarr errors in the logs. Findings: console noise from expected 401/409 probes on a fresh install (web), the version shown as "vdev" (web), and no HEALTHCHECK in the mihon-source image.

**Rebuilt with the full import (2026-10-12, owner's go):** images from server `0fd607b` (web `9617cd7` embedded), meta `5117089`, mihon-source `0b0e1b1` (HEALTHCHECK works; source-mihon waits on it). Full MangaBaka sync started from Panelarr's Start sync: 16m22s, 564,155 upserts, 258,068 merges, **306,084 active entries**, meta database 6.85 GB (Postgres volume 8.3 GB, dump volume 3.5 GB). Docker Desktop's virtual disk (32 GB) is the real limit, not the Mac's disk: 11 GB were left free at the lowest point. Metadata checklist all green, Browse and search return results, no ERROR/WARN in any log; the IN-0047/IN-0048 fixes confirmed on the stack. The app is published on the LAN (`APP_BIND=0.0.0.0`) at the owner's choice.

**Rebuild #2 (2026-10-12):** server `844b43f` (web `5015c14` embedded, built from a clean archive), meta `1787dcf`, source-mihon `cc57126`, all services recreated; the import survived (306,084 entries). A plugin briefly down during recreation recovered by the 10s recheck. Extension stores save from Panelarr's admin end to end; a store that can't be fetched shows as the plugin's health problem about 5s after saving (mihon-source refuses to list it). The owner added a real store. Docker disk: 6.5 GB free at the lowest point during the build, 11.1 GB after pruning.

**Standing rule (IN-0056, 2026-10-12):** after every change merged to a service's main, the local compose stack (`~/Projects/Panelarr/compose`) is rebuilt and redeployed so the owner can try it. Keep `.env` and `secrets/`, never `down -v`, keep the data; build the web dist from a clean archive of web main; prune the build cache afterwards; watch Docker's disk. `panelarr-meta` runs the redeploys; the keeper asks for one when a REPORT lands.

**Redeploy #3 (2026-10-12, FEAT-0009):** server `b80bf84` (web `344f5bc`), meta-mangabaka rebuilt against meta `805d263`, source-mihon `b5dbae0`, mihon-source `17f1f2b`; services built one at a time with the cache pruned in between (disk low point 9.25 GB). Live: the Extensions tab lists the owner's store (about 1,400 packages; the list API answers in 26–62 ms, about 1 MB), icons through signed links, the `languages` setting in order, Admin → Sources, no source browsing for a regular user, catalogue intact. Found: source icons on Admin → Sources fail (the server sends source-mihon's plugin-relative icon path through the image RPC); the Extensions tab renders every row and refetches the full list about every 5 s.

**Redeploys #4–#6 (2026-10-12):** server `470bf23` (source icons via plugin-relative paths), then `58dcc32` with web `743eb09` (icons fall back to the extension icon; Admin → Sources shows 2 sources and "Show hidden (41)", 43/43 icons; the extensions list loads once and reloads only on Reload; no WARN or ERROR in the logs), then `7cd42fa` (quieter logs only on image routes; a jobs cancel race fixed).

**Redeploy #7 (2026-10-12):** server `d409c60` (built from a clean archive, since the checkout had work in progress) with web `647cb99` (reader reads on into the next chapter), mihon-source `c5ea860`, source-mihon `6140031`; all healthy; the owner's store and extensions intact; no profiles pushed.

**Redeploy #8 (2026-10-12):** server `1708381` with web `f61ad6e`, source-mihon `f709407` (image budget), all from clean archives (a compose build from a dirty server checkout failed once, so the server is now always built from a clean archive). Reader timing on the owner's webtoon, phone viewport: before the image limits, page waits grew to 78 s at p50 and the next chapter never loaded in 209 s; after, p50 1.5 s, p90 2.6 s, and the next chapter's pages loaded as the reader reached them. Series page, bookmarks, source settings and the `network.meta` job checked live. Found: the reader refetches the chapter's page list about every 2 s; a client closing mid-request is logged as a 500 ERROR. The reader tests marked some of the owner's chapters as read.

**Redeploy #9 (2026-10-12):** server `4c68d52` (canceled requests quiet) with web `d132205` (reader bars and settings sheet). Checked on a phone viewport: the bars hide while reading and return on a centre tap, the settings sheet opens, the page list is fetched once per chapter. The reader jump fix (IN-0066) is not in this build.

**Redeploy #10 (2026-10-12):** server `311a1c8` (meta admin proxied, custom solvers and proxies) with web `d132205`, source-mihon `7be5a70` (origins, details, reload). Meta's jobs, providers, duplicates, judge and search engine answer for the owner with no secrets in the responses. No duplicate pairs yet: meta's duplicates job first runs on this catalogue at 04:30 UTC tomorrow.

**Redeploy #11 (2026-10-12):** server `0eef78e` with web `daa764c` (reader jump fix). Phone test on a slow, throttled connection: the page being read moved 0 px while pages loaded, in three runs; opening a chapter no longer loads the previous one.

**Redeploy #12 (2026-10-12):** server `e596c82` with web `d107983` (Admin → Network), mihon-source `9e8b3fc`, source-mihon `466cbf4`. Live: source-mihon's jobs (plugin sync every 15 min, store refresh every 12 h, health checks off as before), the owner's store with its package count, extension details with the signing key matching the store's, Admin → Network empty and ready. No warnings or errors.

**Redeploys #13–#15 (2026-10-12):** server `f28a50e`, then `ae9666f` with web `06c718a` (clean chapter titles in the app). The keeper had `chapters.reunify` run once: in 94 ms Solo Leveling went from no volumes to 181 of 261 chapters with volumes 1–13; chapter IDs, chosen copies and the owner's progress unchanged.

**Redeploy #16 (2026-10-12):** web `645caa3` (library). The owner's library shows Solo Leveling with "258 unread" and a Continue button to chapter 1, checked read-only; the sheet was tried by a throwaway user (sort and display saved and kept after a reload), which was then deleted with its data.

**Redeploy #17 (2026-10-12):** web `9f66ccc` (one Jobs view, Admin → Metadata). Read-only check: meta's jobs grouped by kind, source-mihon's three jobs on its Jobs tab, the meta line on System. Found: cron schedules shown as "Runs by hand only" (sent to web). The mangabaka sync's last run shows the morning's deliberate provider-down test as failed; tonight's 03:00 sync replaces it.

**Redeploy #18 (2026-10-12):** web `2dbd31a`. Plugin tabs Overview | Extensions | Sources | Jobs | Network; the owner's store with its count and refresh time; installed-extension details with the signing key matching the store's; cron jobs in words. Found: the Sources tab also lists the 41 language-off sources (sent to web to hide by default, as on Admin → Sources).

**Redeploy #19 (2026-10-12):** server `4ab5574` with web `86ff8a9`. Metadata Overview health (database 0 ms, search 419 ms, the mangabaka provider 1 ms), Providers with 564,155 records and the daily 03:00 UTC sync; source-mihon's Sources tab shows its 2 live sources with the other 41 hidden. Read-only; no syncs started.

**Redeploy #20 (2026-10-12):** web `c40ed4a` (Metadata → Search; GOAL-0021 complete). A sweep of every new admin tab (plugin, Metadata, Network) found no HTTP, console or page errors. Found: the built-in (postgres) search engine is shown as "Degraded" because the page reads `ready`, which only applies to external engines (sent to web).

**Redeploy #21 (2026-10-12):** web `f530dc5`. Metadata → Search reads Healthy for the built-in engine. meta confirmed `search-rebuild` and `search-indexer` are no-ops with postgres (recorded as skipped with a reason); hiding them on the Jobs tab, or a per-job "available" flag in meta, is a possible later polish, not scheduled.

**Redeploy #22 (2026-10-12):** server `061fb9d`, web `40bf625`, source-mihon `1e087cb`, meta `f8e976b`. Metadata → Jobs shows meta's two search-index jobs as "Can't run now" (built-in search), everything else runnable; source-mihon's three jobs runnable. No errors.

**Fix (2026-10-18, IN-0068):** mihon-source's /tmp is mounted `rw,exec,size=128m` in the compose stack (other services keep noexec): extensions' HTTP clients unpack zstd/brotli native libraries to /tmp and load them. Without exec, some chapters' page lists failed with `source_failed` (UnsatisfiedLinkError). **Durable fix** in mihon-source `b128f56`: its entrypoint picks `java.io.tmpdir` at launch (`MIHON_TMP_DIR`, else /tmp if it can run code, else `$MIHON_DATA_DIR/tmp`, emptied at start), and warns at startup if the tmpdir still can't run code; compose.example.yaml carries the same tmpfs. Only zstd needs exec (OkHttp's brotli decoder is pure Java). The stack's override stays as it is.

**Redeploy #23 (2026-10-18):** server `7743817` (history API, updates feed; migrations 00016–00017) with web `c052bd1` (reader flicker fix). Docker Compose had been upgraded to 5.6, which hashes service config differently, so this `up` recreated postgres once (same image and volume, data intact, about 6 s down); meta will be recreated once the same way on its next `up`. Docker Desktop's disk is now about 126 GB (98 GB free). Owner's updates status shows one series whose last check failed, most likely from before the mihon-source /tmp fix; the next scheduled check (20:21 UTC) should clear it.

**Redeploy #24 (2026-10-18):** web `4ce796b` (reader errors). Server-only with `up -d --no-build --no-deps server`, which keeps Compose 5.6 from recreating postgres; use `--no-deps` for single-service redeploys from now on. Chapter 199 opens (48 pages); no zstd errors.

**Redeploy #25 (2026-10-18):** server `8a13bb6` with web `4654cc3` (no app header on phones, Home Screen app bands fixed). Healthy; no warnings.

**Redeploy #26–#29 (2026-10-18):** web `b753025` (compact series page), `ff7d11f` (library search icon, back to the series), `3f7b93f` (reader seams and scroll-up), then `6bedb02` (History tab and a reader regression fix). The keeper's request named the commits in the wrong order, so `6c860b8` (History without the fix) was live for about 79 s before `6bedb02`. Redeploy requests now name the branch head to deploy, and the deploy script stops when the requested commit doesn't contain the expected ones.

**Redeploy #30 (2026-10-18):** web `fd0b653` (Updates tab). The owner's feed has 4 new chapters; the earlier failing update check has cleared. The throwaway `sim-check` user was deleted; `owner` is the only account.

**Redeploy #31 (2026-10-18):** web `621c97a` (Browse → library, IN-0081 a) with server `8a13bb6` unchanged; server-only `up -d --no-build --no-deps`, nothing else recreated; build cache pruned (1.31 GB).

**Redeploy #32 (2026-10-18):** server `9d3ddaa` (page image retries, GOAL-0022 S1) with web `621c97a` unchanged; server only, `--no-deps`; build cache pruned (1.34 GB). The retry path itself wasn't exercised live (GET-only checks).

**Redeploy #33 (2026-10-18):** server `6ff0878` (image retry settings, GOAL-0022 S2; migration 00018 adds `image_retry_settings`) with web `621c97a` unchanged; server only, `--no-deps`. GET on two sources' `image-retries` answers level `default`, [1000, 3000]. Build cache pruned (3.25 GB).

**Redeploy #34 (2026-10-18):** web `6a8b95f` (previous chapter loaded ahead, IN-0081 b) with server `6ff0878` unchanged; server only, `--no-deps`; new shell `index-DP_Ntbhi.js`. The reader wasn't opened (it would write the owner's progress). Build cache pruned (1.35 GB).

**Redeploy #35 (2026-10-18):** web `3f73d90` (image retry settings UI, GOAL-0023) with server `6ff0878` unchanged; server only, `--no-deps`; new shell `index-Cx8AHmoA.js`. GET on both installed packages' and both sources' `image-retries` answers level `default`, [1000, 3000]; no PUT or DELETE. Build cache pruned (3.40 GB).

**Redeploy #36 (2026-10-18):** web `2271320` (nested-list markup fix) with server `6ff0878` unchanged; server only, `--no-deps`; new shell `index-DqdhXhSL.js`. Build cache pruned (1.5 GB).
