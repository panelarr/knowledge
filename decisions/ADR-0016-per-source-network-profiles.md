---
title: "ADR-0016: Per-source network profiles (proxy, solver, rate limit, UA, cookies)"
status: proposed
tags: [networking, sources]
related: [architecture/networking.md]
inputs: [IN-0002]
updated: 2026-10-11
---

# ADR-0016: Per-source network profiles

- **Date:** 2026-10-11 · **Deciders:** author (proposed)

## Context
IN-0002 asks for "flaresolver/proxies/vpn support for each source individually". Suwayomi has only a global SOCKS proxy and one shared client.

## Decision (proposed)
- A **network profile** is a named bundle: proxy (HTTP/HTTPS/SOCKS5, auth), solver (FlareSolverr/Byparr URL + session policy), rate limit, concurrency, user agent, DoH, extra headers, cookie-jar scope and timeouts.
- Profiles are defined once in server and **assigned per source**, with a default profile as fallback. They are pushed to source plugins through the contract. Each plugin enforces them in its own HTTP stack:
  - Go SDK client factory;
  - per-source OkHttp in mihon-source.
- **VPN** = a gluetun (or similar) container that exposes an HTTP/SOCKS proxy and is referenced by a profile. Panelarr never manages tunnels itself.
