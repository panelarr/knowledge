---
title: source-mihon overview
status: draft
tags: [module, source-mihon, mihon, go]
related: [modules/mihon-source/overview.md, contracts/mihon-source-api.md, research/mihon-extension-store.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# source-mihon

## Summary

The Go side of Mihon support ([ADR-0005](../../decisions/ADR-0005-layered-source-architecture.md)). It holds the "smart" logic so that mihon-source can stay a small tool: **extension stores, signing trust, update checks, install orchestration, caching and retries**. It talks to one or more mihon-source endpoints.

## Responsibilities
- **Stores:**
  - add store URLs (`repo.json` → `index.pb` protobuf / JSON, legacy `index.min.json`) ([research](../../research/mihon-extension-store.md));
  - refresh on a schedule;
  - map `contentWarning` to Panelarr content ratings.
- **Trust:** pin each store's `signingKey` fingerprint. Before `InstallExtension`, pass the expected fingerprint and SHA-256 to mihon-source, which refuses a mismatch.
- **Install and update:** pick the `jarUrl` (else `apkUrl`), call mihon-source `InstallExtension`, track versions, offer updates, roll back if loading fails.
- **Source surface:** expose the sources of the installed extensions as `panelarr.source.v1`, either by **proxying** to mihon-source (adding caching and retries) or by letting server talk to mihon-source directly while source-mihon stays the store manager. Open: [Q-0026](../../questions/README.md).
- **Network profiles:** forward per-source profiles to mihon-source.

## Open
- [Q-0026](../../questions/README.md) (the role split). Multiple mihon-source instances, e.g. one per network zone (suggestion).

## Implementation status
Not started (M1).
