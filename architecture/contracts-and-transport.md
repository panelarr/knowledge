---
title: Contracts and transport
status: proposed
tags: [architecture, contracts, grpc, openapi]
related: [decisions/ADR-0012-protobuf-grpc-contracts.md, contracts/README.md, architecture/plugins.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# Contracts and transport

## Summary

**Protobuf is the source of truth** for service-to-service contracts. Services talk **gRPC**. The same protos also produce **HTTP/JSON + OpenAPI**, so standalone tools work with curl. The **browser API** is hand-designed **REST + OpenAPI 3.1 + SSE** ([ADR-0012](../decisions/ADR-0012-protobuf-grpc-contracts.md), proposed).

## Where each contract lives (public repos)

| Contract | Proto package | Owner repo | Implemented by | Consumed by |
|---|---|---|---|---|
| Source plugin | `panelarr.source.v1` | `source-api` | mihon-source, source-mihon, source-local, future | server, source-mihon |
| Mihon admin (extensions, prefs) | `panelarr.mihon.v1` | `mihon-source` | mihon-source | source-mihon |
| Metadata plugin | `panelarr.metadata.v1` | `meta` | meta-* plugins | meta |
| Meta service | `panelarr.meta.v1` | `meta` | meta | server |
| Plugin index | JSON Schema | `source-api` (shared plugin kit, [Q-0017](../questions/README.md)) | indexes | server |
| Server API (browser + 3rd party) | OpenAPI 3.1 (REST) | `server` | server | web, 3rd parties |
| Events | SSE (JSON) | `server` | server | web |

The reasoning behind each contract lives in [contracts/](../contracts/README.md).

## Rules
- **Versioned packages** (`v1`, `v2`). Breaking changes need a new package, and `buf breaking` runs in CI.
- **Errors:** gRPC status codes, plus a typed `ErrorInfo` reason (`CLOUDFLARE_CHALLENGE`, `RATE_LIMITED`, `SOURCE_DOWN`, `NOT_FOUND`, `UNAUTHENTICATED`, …). In JSON these map to `application/problem+json`.
- **Binary data:** images and archive pages are **server-streaming** (chunks) on gRPC and a plain streamed `GET` on HTTP.
- **Auth between services:** a pre-shared API key (metadata header / `Authorization: Bearer`), or a local socket for managed plugins. mTLS is optional for remote plugins.
- **Capabilities:** every service exposes `GetInfo` (name, version, contract versions, capabilities), so hosts degrade gracefully.

## Stack (leaning, [Q-0020](../questions/README.md))
- **Go:** **ConnectRPC** serves gRPC, gRPC-Web and Connect JSON from one handler. OpenAPI comes from protos (e.g. `protoc-gen-connect-openapi`). `buf` handles generation, lint and breaking checks.
- **JVM (mihon-source):** grpc-kotlin with Ktor for JSON, or **Armeria** (built-in gRPC + HTTP/JSON transcoding + docs service). To be decided.
- **Browser API:** OpenAPI 3.1 written for `server`. web generates a typed client from it.
