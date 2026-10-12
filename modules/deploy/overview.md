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
