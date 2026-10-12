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
