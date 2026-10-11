---
title: "ADR-0014: Plugin indexes with checksums and signatures; none preinstalled"
status: proposed
tags: [plugins, security]
related: [contracts/plugin-index.md, architecture/security.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# ADR-0014: Plugin index and signing

- **Date:** 2026-10-11 · **Deciders:** author (proposed)

## Decision (proposed)
- Hosters add **plugin index URLs**, the way Mihon users add extension stores. An official Panelarr index exists but is **not** added silently. The first-run wizard offers it.
- **Entries:** id, kind, versions, minimum host/contract version, per-OS/arch artifacts with **SHA-256**, an optional container image, and a **signature** (leaning: minisign or cosign) checked against the index's published key.
- **Unsigned or unknown-key plugins:** require explicit admin trust.

Format details: [contracts/plugin-index.md](../contracts/plugin-index.md). Key management is open ([Q-0024](../questions/README.md)).
