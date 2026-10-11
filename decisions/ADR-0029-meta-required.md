---
title: "ADR-0029: meta is required for the library"
status: accepted
tags: [meta, library, deployment, principles]
related: [decisions/ADR-0028-library-entry-per-work.md, decisions/ADR-0011-composable-opt-in-deployment.md, modules/meta/overview.md, architecture/deployment.md, product/principles.md]
inputs: [IN-0038]
updated: 2026-10-11
---

# ADR-0029: meta is required for the library

- **Date:** 2026-10-11
- **Deciders:** @aurimasniekis
- **Changes:** [ADR-0011](ADR-0011-composable-opt-in-deployment.md) (meta was opt-in; annotated)

## Context

[ADR-0028](ADR-0028-library-entry-per-work.md) anchors every library entry on meta's Entry. meta was optional by principle (ADR-0011), so [Q-0038](../questions/README.md) asked what happens without it. Options: entries without meta that link later (recommended by the keeper), meta required, or meta built into the server. The owner chose **"meta required for the library"** (IN-0038 §1).

## Decision

- **The library needs meta.** A Panelarr install is **server + PostgreSQL + meta**. Every Work is created from a meta Entry; there are no Works without a meta link.
- meta stays its **own service** (Q-0006; its own container and database). It is still usable standalone by other projects.
- Everything else stays opt-in: mihon-source and other source plugins, solvers, proxies/VPN, search engines, trackers.

## Consequences

- **Deploy:** compose runs `postgres`, `server` and `meta` by default; Unraid/AIO templates include meta.
- **A metadata provider is needed too.** meta with no provider has an empty catalogue, so the library can't add anything. Plugins are never bundled ([ADR-0009](ADR-0009-plugins-not-bundled.md)), so the first-run setup must guide the hoster to add a metadata plugin (e.g. meta-mangabaka) and run its first sync. How that wizard looks is open.
- **Server readiness:** the server reports degraded (not down) when meta is unreachable. Reading what's already downloaded keeps working; adding and matching wait.
- **Simpler model:** no meta-less Works, no later merge of duplicates created before linking.
- AGENTS.md, the principles and the deployment doc are updated.
