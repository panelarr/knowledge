---
title: "ADR-0009: Sources and metadata providers are opt-in plugins"
status: accepted
tags: [plugins, sources, metadata]
related: [architecture/plugins.md, decisions/ADR-0013-out-of-process-plugins.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# ADR-0009: Opt-in plugins

- **Date:** 2026-10-11 · **Deciders:** author

## Context
"Sources could be like plugins, like by default they dont come and u need to add it urself, same for metadata" (IN-0003 §4).

## Decision
- Source providers (Mihon, local files, …) and metadata providers (MangaBaka, AniList, …) are **plugins**.
- A fresh install has **none**. The hoster adds plugin indexes and installs what they want. The UI may *suggest* plugins but never installs them silently.

## Consequences
- Panelarr ships no content-access code by default, which is a cleaner legal posture ([Q-0016](../questions/README.md)).
- Needs a plugin host, a plugin index format, and trust and signing ([ADR-0013](ADR-0013-out-of-process-plugins.md), [ADR-0014](ADR-0014-plugin-index-and-signing.md)).
- The core must be useful with zero plugins: an empty library, plus later import of existing CBZs.
