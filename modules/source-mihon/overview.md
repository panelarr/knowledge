---
title: source-mihon overview
status: draft
tags: [module, source-mihon, mihon, go]
related: [decisions/ADR-0021-mihon-source-standalone-admin.md, modules/mihon-source/overview.md, contracts/mihon-source-api.md, research/mihon-extension-store.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# source-mihon

## Summary

The Go side of Mihon support ([ADR-0021](../../decisions/ADR-0021-mihon-source-standalone-admin.md), which superseded ADR-0005). It was planned to hold the "smart" logic: **extension stores, signing trust, update checks, install orchestration, caching and retries**. It talks to one or more mihon-source endpoints. Since ADR-0021, mihon-source manages stores itself for standalone use, so this module's store role is open ([Q-0026](../../questions/README.md), [Q-0030](../../questions/README.md)).

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
