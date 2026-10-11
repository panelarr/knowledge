---
title: "ADR-0026: ConnectRPC on the Go side, gRPC as the plugin wire"
status: accepted
tags: [contracts, rpc, go, plugins]
related: [decisions/ADR-0012-protobuf-grpc-contracts.md, decisions/ADR-0013-out-of-process-plugins.md, decisions/ADR-0024-armeria-for-the-jvm-rpc-server.md, architecture/contracts-and-transport.md, contracts/metadata-plugin.md]
inputs: [IN-0019]
updated: 2026-10-11
---

# ADR-0026: ConnectRPC on Go, gRPC as the plugin wire

- **Date:** 2026-10-11
- **Deciders:** @aurimasniekis (proposed by `panelarr-meta` after building meta slice 2; wire rule suggested by the keeper)

## Context

[Q-0020](../questions/README.md) asked for the Go RPC stack and whether gRPC is the primary wire for remote plugins. The JVM side is Armeria ([ADR-0024](ADR-0024-armeria-for-the-jvm-rpc-server.md)). `panelarr-meta` built the plugin SDK and meta's API on ConnectRPC and PROPOSEd it. The owner asked for the case against. The costs were two Go stacks (go-plugin needs grpc-go), vanguard being younger than grpc-gateway, and Connect being a Buf project. The owner accepted ConnectRPC with the wire rule below (IN-0019).

## Decision

- **Go services and plugins use ConnectRPC** (`connect-go`). One handler serves gRPC, gRPC-Web and the Connect protocol.
- **Managed plugins** (go-plugin, [ADR-0013](ADR-0013-out-of-process-plugins.md)) use **grpc-go**, which go-plugin requires. The SDK hides the difference behind one client.
- **REST/JSON** follows the `google.api.http` paths in the protos. On Go, it is served through vanguard transcoding. grpc-gateway is the fallback if vanguard falls short.
- **The wire rule:**
  - **Standard gRPC is the canonical wire for remote plugins and services.** Every Panelarr service and plugin, Go or JVM, must speak it, and hosts call remote plugins over it.
  - REST/JSON (per `google.api.http`) is offered for browsers, curl and the standalone admin tools.
  - The Connect protocol is an extra, never required of a plugin.
  - So a plugin in any language only needs gRPC.

## Consequences

- Q-0020 is answered.
- Third-party plugins need nothing Buf-specific; plain protobuf + gRPC works.
- Two server setups on Go (Connect and grpc-go) share interceptors for auth and errors through the SDK. The conformance harness runs over both.
- Connect-go clients calling JVM services (mihon-source on Armeria) use the gRPC protocol option.

## Alternatives considered

| Option | Why not |
|---|---|
| grpc-go everywhere + grpc-gateway | No gRPC-Web/Connect from one handler; more glue for browsers and the standalone tools |
| Drop go-plugin, Connect over a local socket for managed plugins | A custom supervisor to write and maintain, for little gain |
