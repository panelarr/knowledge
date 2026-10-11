---
title: source-api overview
status: proposed
tags: [module, source-api, go, contract]
related: [contracts/source-plugin.md, contracts/plugin-index.md, architecture/plugins.md, architecture/networking.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# source-api

## Summary

The **general source layer** in Go ([ADR-0005](../../decisions/ADR-0005-layered-source-architecture.md)). It defines the `panelarr.source.v1` protos ([contract](../../contracts/source-plugin.md)) and ships what plugin authors and hosts need: a Go SDK, generated clients, an HTTP client factory that applies network profiles, and a conformance suite. It is likely also the home of the shared **plugin kit** (go-plugin handshake, plugin index schema and verifier) used by both server and meta ([Q-0017](../../questions/README.md)).

## Contents
```
proto/panelarr/source/v1/   *.proto (buf module, published to BSR optional)
gen/go/                     generated Go (connect + grpc)
sdk/                        plugin.Serve(impl): managed (go-plugin) or --listen standalone; capability helpers
sdk/httpx/                  NewClient(profile): proxy (http/socks5), solver round-tripper, rate limit, cookie jar, DoH
pluginkit/                  index schema + client, sha256/signature verify, go-plugin host helpers
conformance/                `source-conformance --target host:port` test runner
openapi/                    generated OpenAPI for the JSON mapping
```

## Notes
- Breaking changes are blocked with `buf breaking` in CI.
- `sdk/httpx` is the Go twin of mihon-source's per-source OkHttp setup ([networking](../../architecture/networking.md)). Both must behave the same in conformance tests (proxy honoured, solver called on challenge).

## Implementation status
Not started (M0).
