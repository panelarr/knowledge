---
title: "ADR-0013: Plugins run out of process: managed binaries or remote endpoints"
status: proposed
tags: [plugins]
related: [architecture/plugins.md, decisions/ADR-0009-plugins-not-bundled.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# ADR-0013: Out-of-process plugins

- **Date:** 2026-10-11 · **Deciders:** author (proposed)

## Decision (proposed)
A plugin (kind `source` or `metadata`) runs in one of two modes:
1. **Managed binary:** the host downloads a release binary for its OS/arch from a [plugin index](ADR-0014-plugin-index-and-signing.md), verifies it, and runs it as a child process via **HashiCorp go-plugin** (gRPC over a local socket). It is restarted on crash and isolated from the host's memory.
2. **Remote endpoint:** the plugin runs elsewhere (a container, another host), and the host connects by URL and API key over the same protos ([ADR-0012](ADR-0012-protobuf-grpc-contracts.md)). This is also the **standalone** mode.

## Alternatives considered
| Option | Why not |
|---|---|
| Go `plugin` package (.so) | Linux-only, needs an exact toolchain and dependency match, can't unload |
| WASM plugins (wazero) | Promising, but networking/TLS and solver access from WASM are immature; may revisit |
| Compile everything in | Contradicts opt-in ([ADR-0009](ADR-0009-plugins-not-bundled.md)) |
