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
compose.yaml           server + postgres, plus profiles: mihon, meta, search-typesense, search-meilisearch, flaresolverr, byparr, vpn
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
