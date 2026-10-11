---
title: "ADR-0024: Armeria for the JVM RPC server"
status: accepted
tags: [contracts, rpc, jvm, mihon-source]
related: [decisions/ADR-0012-protobuf-grpc-contracts.md, modules/mihon-source/overview.md, contracts/mihon-source-api.md]
inputs: [IN-0014]
updated: 2026-10-11
---

# ADR-0024: Armeria for the JVM RPC server

- **Date:** 2026-10-11
- **Deciders:** @aurimasniekis (proposed by `panelarr-mihon-source` after a spike)

## Context

mihon-source must serve its protos over gRPC and HTTP/JSON with OpenAPI ([ADR-0012](ADR-0012-protobuf-grpc-contracts.md), proposed). [Q-0020](../questions/README.md) left the JVM stack open: Armeria, or grpc-kotlin + Ktor. The coding session spiked Armeria in slice 2 of GOAL-0001 and PROPOSEd it. The owner accepted it (IN-0014 §2).

## Decision

- JVM services (today mihon-source) use **Armeria**. One port serves gRPC, gRPC-Web and HTTP/JSON transcoding from the `google.api.http` annotations.
- Services stay plain **grpc-kotlin** coroutine services, and auth is a standard gRPC interceptor. Armeria-specific code lives in one place, so a swap stays cheap.
- OpenAPI is generated from the protos at build time, not by Armeria.
- The Go side of Q-0020 (ConnectRPC) is not decided here.

## Consequences

- Armeria pins protobuf-java 3.25.x and gRPC 1.84. Extensions never see these classes: the extension classloader exposes only the extension API and host libraries.
- One server also covers static files (the admin SPA, Swagger UI), streaming responses, multipart upload and graceful shutdown.

## Alternatives considered

| Option | Why not |
|---|---|
| grpc-kotlin + Ktor | Ktor has no gRPC transcoding: it needs a second server or hand-written JSON routes per RPC, which drift from the protos |
