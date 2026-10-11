---
title: "ADR-0011: Composable, opt-in deployment"
status: accepted
tags: [deployment, principles]
related: [product/principles.md, architecture/deployment.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# ADR-0011: Composable, opt-in deployment

- **Date:** 2026-10-11 · **Deciders:** author

## Context
"Each own hoster can decide what they want to run" (IN-0003 §4), together with "standalone" tools (IN-0002).

## Decision
- **`server` alone is a working install** (SQLite, built-in search, no plugins).
- **Everything else is opt-in and configurable:** meta, search engine, mihon-source, solvers (FlareSolverr/Byparr), proxies/VPN, Postgres/MySQL, every plugin.
- **Standalone tools** (mihon-source, meta, source plugins) remain usable without Panelarr.

## Consequences
- Every integration needs a graceful "not configured" path.
- The deploy repo uses compose **profiles** and Unraid templates per component.
