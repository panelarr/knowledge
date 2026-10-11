---
title: Principles
status: proposed
tags: [product, principles]
related: [product/vision.md, decisions/ADR-0011-composable-opt-in-deployment.md, decisions/ADR-0020-public-kb-with-aliases.md]
inputs: [IN-0002, IN-0003, IN-0004]
updated: 2026-10-11
---

# Principles

## Summary

These tests apply to every design choice. Most are accepted ADRs; this page states them as product rules.

1. **Opt-in and composable.** The hoster decides what runs. `server` alone works. meta, the search engine, solvers, VPN, external DBs and every plugin are optional, configurable, and fail gracefully when absent ([ADR-0011](../decisions/ADR-0011-composable-opt-in-deployment.md)).
2. **Nothing bundled that touches content providers.** Sources and metadata providers are plugins the hoster adds ([ADR-0009](../decisions/ADR-0009-plugins-not-bundled.md)). Legal wording is still open ([Q-0016](../questions/README.md)).
3. **Multi-user first.** Every feature is designed for *N* users sharing one store: permissions, content ratings, quotas, ownership checks on every file read ([ADR-0003](../decisions/ADR-0003-shared-store-per-user-libraries.md)).
4. **Standalone pieces.** If a component is useful without Panelarr (mihon-source, meta, plugins), it gets a clean public API and its own docs.
5. **Portable data.** Library files are CBZ with ComicInfo.xml, readable by other tools. The DB can be SQLite, Postgres or MySQL. Indexes can be rebuilt.
6. **Per-source control.** Networking, rate limits and preferences are per source, never global-only.
7. **Respect upstreams.** Honour rate limits, attribute metadata (MangaBaka CC BY-NC-SA), and never redistribute dumps.
8. **Open code, open planning.** Code and this KB are public on GitHub. Sensitive names (copyright-adjacent projects, private projects) appear only as aliases, and the KB never says where extensions can be obtained ([ADR-0020](../decisions/ADR-0020-public-kb-with-aliases.md)).
