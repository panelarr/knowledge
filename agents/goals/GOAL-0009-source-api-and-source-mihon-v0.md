---
title: "GOAL-0009: source-api and source-mihon v0"
status: accepted
tags: [goal, agents, source-api, source-mihon, go]
related: [modules/source-api/overview.md, modules/source-mihon/overview.md, contracts/source-plugin.md, contracts/mihon-source-api.md, decisions/ADR-0028-library-entry-per-work.md]
inputs: [IN-0007, IN-0015, IN-0037, IN-0038, IN-0040]
repos: [source-api, source-mihon, mihon-source]
session: "panelarr-mihon-source"
features: []
updated: 2026-10-11
---

# GOAL-0009: source-api and source-mihon v0

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0009 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`accepted`: dispatched to `panelarr-mihon-source` on 2026-10-11 (owner's go, IN-0040). Repos `panelarr/source-api` and `panelarr/source-mihon` created by the owner.

## Context

- Code: `~/Projects/Panelarr/source-api` and `~/Projects/Panelarr/source-mihon` (new, Go), plus `~/Projects/Panelarr/mihon-source` (switching it to consume the protos from source-api). Same rules as your earlier goals.
- **Read first:**
  1. [modules/source-api/overview.md](../../modules/source-api/overview.md) and [contracts/source-plugin.md](../../contracts/source-plugin.md) (including the as-built notes from mihon-source).
  2. [modules/source-mihon/overview.md](../../modules/source-mihon/overview.md); [architecture/plugins.md](../../architecture/plugins.md) (common surface: config schema, common services); Q-0026, Q-0031 (delegate stores), Q-0030.
  3. **Reuse meta's patterns:** meta's Go SDK (`sdk/plugin`, `sdk/client`, `sdk/httpx`, `sdk/conformance`) solves the same problems for metadata plugins. Copy its structure and behaviour (managed via go-plugin and standalone `--listen`, gRPC canonical per [ADR-0026](../../decisions/ADR-0026-connectrpc-on-go-grpc-as-the-plugin-wire.md), profile-driven HTTP client, conformance harness). Don't import meta's code across repos; the shapes should match.
  4. [ADR-0028](../../decisions/ADR-0028-library-entry-per-work.md): the server will search sources by title and alternative titles to match Works, so `Search` quality and `ResolveUrl` matter.
- Licences ([ADR-0025](../../decisions/ADR-0025-licences-gpl-3-0-apps-apache-2-0-sdks-and-protos.md)): source-api is **Apache-2.0** (protos, generated code, SDK); source-mihon is **GPL-3.0**.

## Objective

1. **source-api:** the home of `panelarr.source.v1`. The protos move here from mihon-source unchanged. Plus generated Go code, a Go plugin SDK (managed and standalone), `sdk/httpx` (the Go twin of mihon-source's per-source networking) and a conformance runner any source plugin must pass.
2. **mihon-source** consumes the protos from source-api (buf dependency or vendored by a pinned version) instead of owning them; no API change.
3. **source-mihon:** a Go source plugin that the Panelarr server talks to. It:
   - **declares its config** (mihon-source endpoint and key, stores) and the **common services** it uses (network profiles, solvers) per IN-0007;
   - **serves `source.v1` by delegating to mihon-source** (pass-through with retries, error mapping and optional caching);
   - **delegates stores** to mihon-source's `MihonStores` (Q-0031);
   - **pushes network profiles** it receives on to mihon-source.

## Slices (suggested)

1. **Scaffold** both repos to the repo standard (Go, Makefile, CI, licences, AGENTS/CLAUDE, docs).
2. **source-api protos + codegen:** move `proto/panelarr/source/v1` from mihon-source, `buf lint` + `buf breaking`, Go codegen (connect + grpc), OpenAPI.
3. **source-api SDK:** `plugin.Main` (managed or standalone, Bearer key), a client over managed/remote/in-process, `httpx`, settings validation, and a **conformance** suite (list → popular → search → details → chapters → pages → image; error mapping; capabilities; health).
4. **mihon-source consumes source-api** (same API, CI green), tagged or pinned.
5. **source-mihon:** config schema (mihon-source URL, API key, optional default stores), pass-through of every `source.v1` RPC to mihon-source over gRPC, `ListSources` merged with health, error mapping, profile pass-through (`SetNetworkProfile` → mihon-source), store management via `MihonStores`; conformance passes against mihon-source plus a test extension.
6. **Images + docs:** a `panelarr/source-mihon` image (standalone, port 8903+ convention), a compose example (source-mihon + mihon-source), docs.

## Constraints

- **Observability** per [ADR-0027](../../decisions/ADR-0027-observability-baseline-for-every-service.md) (JSON logs, metrics, health) and a **Jobs** surface only if source-mihon gets background work (not expected).
- No real extension, store or site names in either repo; tests use mihon-source's test extensions and fixture store.

## Definition of Done

- [ ] source-api: protos moved (no wire change), lint and breaking checks in CI, Go SDK managed + standalone, httpx, conformance runner; Apache-2.0
- [ ] mihon-source builds against source-api's protos; its tests are unchanged and green
- [ ] source-mihon: config schema and common services declared; every source.v1 RPC passed through; stores via MihonStores; profiles forwarded; conformance passes end to end against mihon-source
- [ ] Images, compose example, docs; `make check` green in all three repos; leak-check clean
- [ ] `DONE:` with evidence per box

## History

- 2026-10-11: brief written (`proposed`); waiting for the repos and the owner's go.
- 2026-10-11: owner's go and repos created (IN-0040): `accepted`, dispatched.
- 2026-10-11: REPORT: **slices 1–2 done** in source-api (`bc396c2` scaffold, `69a73ff` protos): Go module and tooling pinned like meta; CI with gen-check, breaking against main, CodeQL, release-please; Apache-2.0. `source_plugin.proto` copied byte-for-byte from mihon-source; Go messages, gRPC and Connect stubs, OpenAPI. Port: **source-mihon standalone = 8904** (meta-mangabaka has 8903). Next: slice 3 (SDK).
- 2026-10-11: PROPOSE accepted: plugin-level `GetConfig`/`SetConfig` in source.v1 (additive; writeOnly fields redacted; validated against config_schema). Recorded in contracts/source-plugin.md.
- 2026-10-11: REPORT: **slice 3 (SDK) done** (`dcf0c7d`; GetConfig/SetConfig protos `aab3ecf`). plugin (managed/standalone, typed errors with reasons and retry hints, config handling), client (managed, remote gRPC/Connect, host connection, in-process), httpx (per-source profiles incl. SOCKS5 auth, solver, limits, DoH, shared jars), settings, a conformance runner (CLI with --strict) and a fake plugin for host tests. The server's asks (1) importable remote client and (2) an in-process fixture are met. Next: slice 4 (mihon-source consumes source-api).
- 2026-10-11: REPORT: **slice 4 done**: mihon-source consumes source-api's protos (`d892a22`), vendored byte-identical under `third_party/source-api` with a pinned commit and checksum; a build check blocks edits; `make sync-source-api` re-pins; GetConfig/SetConfig answered UNIMPLEMENTED. `JOB_TRIGGER_SYSTEM` added (`a3906c0`). Next: slice 5 (source-mihon).
- 2026-10-11: REPORT: **slice 5 (source-mihon) done** (`adcfb82` scaffold, `c16adaf` plugin; source-api `f62b01a` SDK routes). Config schema (mihon-source URL, writeOnly key, stores, extensions) via SetConfig, env or file; limits 2 concurrent and 30/min per source; full pass-through with retries only while mihon-source is unreachable and errors kept (incl. retry_after); health passed through; profiles forwarded; stores and extensions reconciled through MihonStores every 15 min (add only, updates stay in mihon-source); metrics. **End to end:** real mihon-source + test extension + a made-up site: conformance 2 sources, every step OK, 0 problems; title search finds both languages. Slice 6 (image, compose, release) approved by the keeper as part of the goal.
