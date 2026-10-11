---
title: "ADR-0005: Layered sources: source-api, source-mihon, mihon-source"
status: superseded
tags: [sources, plugins, mihon]
related: [architecture/plugins.md, modules/source-api/overview.md, modules/source-mihon/overview.md, modules/mihon-source/overview.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# ADR-0005: Layered sources

- **Date:** 2026-10-11 · **Deciders:** author
- **Superseded by:** [ADR-0021](ADR-0021-mihon-source-standalone-admin.md) on 2026-10-11 (mihon-source gets a minimal admin, clients and extension stores; IN-0006).

## Context
"We will have more than just mihon extensions, so lets do general api of sources and one implementation as mihon" (IN-0003 §2). Then: "source api will be golang and source-mihon will be golang lib but mihon-source will be external api based on kotlin/jvm" and "mihon source is just small tool to interact with mihon extensions directly via api" (IN-0003 §3.3–3.4).

## Decision
- **`source-api`** (Go) is the general source contract and SDK. Every source kind implements it.
- **`source-mihon`** (Go) is the Mihon implementation on the Panelarr side. It owns extension-store logic, trust and orchestration.
- **`mihon-source`** (Kotlin/JVM) is a **small tool** that loads Mihon extensions and exposes them directly over an API. It has no store logic, no library and no database.
- More source kinds plug into source-api: local files ([source-local](../modules/source-local/overview.md)), OPDS, native scrapers, other ecosystems.

## Consequences
- The JVM is confined to the one place that needs it.
- The exact API split between source-mihon and mihon-source is refined by [ADR-0012](ADR-0012-protobuf-grpc-contracts.md) and [Q-0026](../questions/README.md): mihon-source may speak source-api itself.
