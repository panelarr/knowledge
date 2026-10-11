---
title: "ADR-0012: Protobuf contracts; gRPC between services, REST/OpenAPI for browsers and as an option"
status: proposed
tags: [contracts, grpc, openapi]
related: [architecture/contracts-and-transport.md, contracts/README.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# ADR-0012: Protobuf contracts, gRPC between services

- **Date:** 2026-10-11 · **Deciders:** author (proposed by keeper from IN-0003 §6)

## Context
The author: "maybe for inter service we can use grpc or etc? also the mihon one could be standalone tool with our source api grpc or openapi options" (IN-0003 §6). We have many services and plugins in two languages (Go, Kotlin), so a schema-first, codegen-friendly contract is wanted.

## Decision (proposed)
- **Protobuf is the source of truth** for every service-to-service contract: source plugin, metadata plugin, mihon-source, meta.
- **gRPC** carries traffic between services and plugins. HashiCorp go-plugin already uses gRPC for managed plugins.
- The same protos also produce an **HTTP/JSON + OpenAPI** surface, so standalone tools work with curl and any language. Leaning: **ConnectRPC** in Go, which serves gRPC, gRPC-Web and JSON over HTTP from one handler, with OpenAPI generated from the protos.
- **mihon-source implements the source-api protos itself.** It is directly usable as a standalone tool *and* as a remote source plugin, with gRPC and OpenAPI options.
- The **browser ↔ server** API stays **REST + OpenAPI 3.1 + SSE**: TanStack Query friendly, and easy for third-party *arr* tooling.

## Consequences
- Proto packages are versioned (`panelarr.source.v1`) and linted for breaking changes with `buf breaking` in CI.
- The JVM side needs a gRPC + JSON-transcoding stack ([Q-0020](../questions/README.md)).
- source-mihon's role narrows to store, trust and orchestration ([Q-0026](../questions/README.md)).

## Alternatives considered
| Option | Why not |
|---|---|
| REST/OpenAPI everywhere | Weaker typing and streaming; two-language codegen is clumsier |
| gRPC only | Hard to use from curl/browsers; standalone tools lose approachability |
