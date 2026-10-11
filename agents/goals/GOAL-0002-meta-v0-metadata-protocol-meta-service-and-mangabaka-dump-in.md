---
title: "GOAL-0002: meta v0: metadata protocol, meta service and MangaBaka dump ingest"
status: accepted
tags: [goal, agents, meta, metadata, mangabaka, go]
related: [contracts/metadata-schema.md, modules/meta/overview.md, modules/meta-mangabaka/overview.md, contracts/metadata-plugin.md, research/mangabaka.md, research/metadata-providers.md, architecture/search.md, architecture/plugins.md, architecture/repo-standard.md]
inputs: [IN-0007, IN-0009, IN-0010, IN-0011, IN-0012, IN-0013, IN-0014]
repos: [meta, meta-mangabaka]
session: "panelarr-meta"
features: []
updated: 2026-10-11
---

# GOAL-0002: meta v0: metadata protocol, meta service and MangaBaka dump ingest

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0002 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`accepted`: dispatched to `panelarr-meta` on 2026-10-11 (IN-0011). Scope from IN-0009, schema from IN-0010.

## Context

- Code: `~/Projects/Panelarr/meta` and `~/Projects/Panelarr/meta-mangabaka` (clones of `github.com/panelarr/meta` and `github.com/panelarr/meta-mangabaka`, created by the owner; empty, no commits yet) · no extra worktrees · branches `<type>/<scope>-<slug>`, e.g. `feat/proto-metadata-v1`
- Milestone: M3 work pulled forward to run alongside M1 ([roadmap](../../planning/roadmap.md)). There are no `FEAT-` docs yet. The DoD below stands in for acceptance criteria.
- **Read first, in this order:**
  1. [product/principles.md](../../product/principles.md) and [product/scope.md](../../product/scope.md): opt-in and composable; meta is optional and usable standalone.
  2. [modules/meta/overview.md](../../modules/meta/overview.md) and [modules/meta-mangabaka/overview.md](../../modules/meta-mangabaka/overview.md): what each repo owns. **These are the main spec.**
  3. [contracts/metadata-plugin.md](../../contracts/metadata-plugin.md) (ingestion types, the plugin service, the `Sync` event stream, the meta API; draft) and [contracts/metadata-schema.md](../../contracts/metadata-schema.md) (the **entry schema**: ProviderEntry vs merged Entry, building blocks, shared Person/Company/Tag, enums with raw values; proposed). Refine both, then `REPORT:` what you changed.
  4. [research/mangabaka.md](../../research/mangabaka.md) and [research/metadata-providers.md](../../research/metadata-providers.md): the dump and API, schema highlights, licence.
  5. [architecture/plugins.md](../../architecture/plugins.md) (managed vs remote plugins, the common plugin surface: settings schema, common services), [architecture/search.md](../../architecture/search.md) (`SearchIndex`), [architecture/security.md](../../architecture/security.md), [architecture/repo-standard.md](../../architecture/repo-standard.md).
  6. ADRs, **accepted (law):** [ADR-0006](../../decisions/ADR-0006-technology-stack.md), [ADR-0008](../../decisions/ADR-0008-public-repo-standard-and-images.md), [ADR-0009](../../decisions/ADR-0009-plugins-not-bundled.md), [ADR-0011](../../decisions/ADR-0011-composable-opt-in-deployment.md) (with its annotation), [ADR-0020](../../decisions/ADR-0020-public-kb-with-aliases.md), [ADR-0022](../../decisions/ADR-0022-postgresql-only.md) (Postgres only), [ADR-0023](../../decisions/ADR-0023-sqlc-pgx-goose-data-layer.md) (sqlc + pgx + goose). **Proposed (strong guidance, cheap to change):** [ADR-0012](../../decisions/ADR-0012-protobuf-grpc-contracts.md), [ADR-0013](../../decisions/ADR-0013-out-of-process-plugins.md), [ADR-0017](../../decisions/ADR-0017-search-interface-builtin-default.md), [ADR-0019](../../decisions/ADR-0019-release-tooling.md).
- **Aliases:** read `~/Projects/Panelarr/knowledge/.kb-aliases.env` (local, never committed). Write only aliases in code, docs, commits and branches.
- **Accepted decisions are law.** If code and KB disagree, the KB wins, or send `CONFLICT:`.

## Objective

Build the first metadata stack end to end (IN-0009):

- **`meta`:** the `panelarr.metadata.v1` plugin protocol with **ingestion types** (`lookup`, `scrape`, `dump`, `delta`, open-ended), a Go plugin SDK, and the **meta service**. It ingests plugin records into Postgres and serves **Seerr-style** Browse / Search / Get over the whole catalogue through `panelarr.meta.v1` (gRPC + HTTP/JSON + OpenAPI).
- **`meta-mangabaka`:** the first plugin. It downloads the MangaBaka **SQLite dump**, verifies and reads it, streams normalized records to meta, and does API lookups for freshness.

Result: a hoster runs meta + Postgres + meta-mangabaka, triggers a sync, and browses and searches tens of thousands of series with attribution.

## Owner's choices for this goal (IN-0009)

- **Repos:** `meta` holds the protos, the SDK and the service; each plugin gets its own repo (Q-0017).
- **Scope:** end to end. meta is the service that provides metadata, browsing and search to the library and the app, Seerr-style. External search engines come later.
- **Database:** **PostgreSQL only** (ADR-0022), with **sqlc + pgx (v5) + goose** (ADR-0023). Migrations are plain SQL files, embedded and applied at startup and through a `migrate` subcommand.

## Slices (suggested order)

Each slice works end to end, has tests and ends with `make check` green and a `REPORT:`.

1. **Scaffold both repos** to the repo standard: Go module, `Makefile` (`help` default, `setup`, `build`, `test`, `lint`, `fmt`, `run`, `docker`, `gen`, `clean`, `check`), golangci-lint, `go test -race`, govulncheck, `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `.github/` (CI with a Postgres service, PR title lint, templates), `docs/`, `PROGRESS.md`. `AGENTS.md` from [kits/code-repo/AGENTS.public-repo.md](../../kits/code-repo/AGENTS.public-repo.md) plus a one-line `CLAUDE.md`. **Licences** ([ADR-0025](../../decisions/ADR-0025-licences-gpl-3-0-apps-apache-2-0-sdks-and-protos.md)): `meta` is GPL-3.0 with `proto/` and the plugin SDK under Apache-2.0 (own `LICENSE` + SPDX headers); `meta-mangabaka` is GPL-3.0.
2. **Protocol + SDK** (`meta`): `proto/panelarr/metadata/v1` and `proto/panelarr/meta/v1` from the [contract](../../contracts/metadata-plugin.md), `buf lint`, Go codegen. `GetInfo` declares the ingestion types, limits per type, capabilities and the common services a plugin can use (IN-0007). `Sync` is a server stream of events (started, upsert, removed, merge, checkpoint, finished). SDK: `plugin.Serve(impl)` runs managed (go-plugin handshake) or standalone (`--listen`). Add a small conformance harness that runs a plugin through `GetInfo` → `Sync` and checks the events.
3. **meta DB:** goose migrations for the [entry schema](../../contracts/metadata-schema.md): provider_entries (as received, raw JSONB), entries (merged view) and their parts, shared persons/companies/tags, field locks, merges/redirects and sync_runs; sqlc queries; pgx pool; tests against a real Postgres (testcontainers or the CI service).
4. **meta-mangabaka `dump`:** settings schema (dump variant, download dir, optional URL override, schedule hint); download with resume, `.sha1` check, zstd decompression, read-only SQLite via a pure-Go driver (no cgo); map each series to a `ProviderEntry` in the entry schema (titles in every language, plain-string authors/artists as Persons without IDs, tags with spoiler/explicit flags, covers with blurhash/thumbhash and size variants, status, type, content rating, external IDs from the `source` map, relations, links, raw enums kept); `merged_with` → merge events; checkpoints every N records; raw fields kept as extras.
5. **meta ingest:** plugin host (managed binary and remote URL + API key), sync scheduler with manual runs (`MetaAdmin.RunSync`), batched upserts of ProviderEntries committed at checkpoints (`COPY` into staging tables if it pays off), building or updating merged Entries (per-field provider priority, manual locks honoured; with one provider it's a straight copy), linking by shared external IDs, merge redirects, removed-after-snapshot marking, sync run records with counts and errors, attribution stored per record. A full re-sync of an unchanged dump makes no changes.
6. **meta API:** `panelarr.meta.v1` over gRPC + HTTP/JSON with OpenAPI: `Browse` with filters (genre, tag, type, status, year, content rating, language) and sort (popularity, rating, updated, year), `Search` (titles in every language and alt titles, people) via a `SearchIndex` interface backed by Postgres FTS + `pg_trgm` (design it so meta's **optional, configurable engine adapters** plug in later: Typesense, Meilisearch, maybe OpenSearch/Algolia, IN-0017/IN-0018; a `search.backend` setting with only `postgres` implemented now), `Get` with full details and attribution, `LookupExternal` (e.g. `anilist:30013`), `MetaAdmin` (providers, runs). Old IDs resolve through merge redirects. Auth: a service API key from config (suggestion; `PROPOSE:` if you see better).
7. **meta-mangabaka `lookup`:** `Search` / `Get` through the MangaBaka API within its limits (search 30/min, other GETs 180/min), backing off on 429. meta uses it to refresh a stale record on demand.
8. **Images + docs:** images `panelarr/meta` and `panelarr/meta-mangabaka` (standalone mode), a `compose.yaml` example (meta + postgres + meta-mangabaka; any layout that's convenient for dev). In the **production setup** (the deploy repo, later) meta and server share one Postgres server, each with its own database (IN-0012, IN-0013), so meta takes its own DSN and keeps everything inside its own database (no server-wide settings or superuser needs); a quick start in each README, and `docs/` for configuration, the protocol, how to write a metadata plugin, and the API.

## Tests and fixtures

- **No MangaBaka data in the repos.** It is CC BY-NC-SA 4.0: no dump, extract or real records in fixtures, tests or docs. Build a **synthetic SQLite fixture** that mirrors the dump schema (a few dozen made-up series covering merges, multiple languages, tags with flags, missing fields), and serve it zstd-compressed with a `.sha1` from a local test server.
- **The owner may run a real dump by hand.** Provide a `make` target or a documented command for that, outside CI. REPORT ingest time and DB size when you or the owner have run one.
- Postgres in tests: real Postgres only, never a substitute.

## How to work

1. Build in **slices**. Each slice works end to end (logic, interface, tests, docs).
2. One branch per slice, per repo. Conventional Commits.
3. After each slice: `make check` passes in every repo you touched → `REPORT:` to the keeper (`panelarr-knowledge`, via session messages) with what you built, what you assumed and how to test it.
4. Keep `PROGRESS.md` in `meta` covering both repos: these slices ticked off, plus the next one. **Re-read it whenever you lose context.**
5. Don't stop after each slice to ask. Go on to the next one unless blocked on the owner's decision. Before the first release, merge each finished slice into `main` yourself once `make check` is green, then branch the next slice off `main`. Say what you merged in the REPORT.
6. Until `meta` publishes tagged versions, `meta-mangabaka` uses the SDK through a Go `replace` directive pointing at the local `meta` clone (or a workspace, `go.work`, kept out of git). Say which in a REPORT.

## When something isn't decided

- `ASK:` the keeper first.
- Still open? `PROPOSE:` a concrete working assumption that fits the accepted decisions, then build it **cheap to change** (config/data, not hard-coded).
- Never present an assumption as decided, and never change an accepted decision yourself.
- **meta is a standalone service** with library integration through its API (Q-0006, IN-0015); **default port 8901** (server 8900, mihon-source 8902); meta-mangabaka in standalone mode **8903** (IN-0016). Known open points: Q-0020 (RPC stack: ConnectRPC on Go is the lead), Q-0022 (external search engines: later), Q-0023 (characters: out of scope).

## Constraints

- **Git:** commit on your own feature branches. **Before the first release you may merge your own branches into `main` yourself** once `make check` is green (IN-0014): fast-forward or squash, keep history linear, never rewrite `main`. **Never push**: the owner pushes. No forge actions (issues, PRs, comments).
- **Public repo** ([ADR-0008](../../decisions/ADR-0008-public-repo-standard-and-images.md), [ADR-0020](../../decisions/ADR-0020-public-kb-with-aliases.md)): everything you write is public. Explain the *why* in your own words. **You may cite KB IDs** (`ADR-`, `Q-`, `GOAL-`) in docs and in `Refs:` commit footers, and **link KB docs** at `https://github.com/panelarr/knowledge/blob/main/<path>` (Q-0028, IN-0014). Never local KB paths. Aliases only. Never say where extensions can be obtained. Before each REPORT, run `python3 ~/Projects/Panelarr/knowledge/tools/kb.py leak-check` (no arguments: it scans every registered repo).
- **Respect upstreams:** honour MangaBaka's rate limits, identify the client with a clear User-Agent, show attribution wherever its data is served, never redistribute its data.
- **Opt-in:** meta runs without any plugin (empty catalogue, clear "no providers" state). The plugin runs without network profiles.
- **Out of scope:** matching source series to metadata, characters, other providers, external search engines, server integration, UI.

## Definition of Done

- [ ] Both repos scaffolded to the repo standard; `make check` green; CI runs against Postgres
- [ ] `metadata.v1` and `meta.v1` protos, `buf lint` clean; ingestion types, limits and common services declared in `GetInfo`; contract changes REPORTed
- [ ] Go SDK: one plugin binary runs managed (go-plugin) and standalone (`--listen`); conformance harness passes against meta-mangabaka
- [ ] goose migrations applied at startup and through `migrate`; sqlc queries; tests on real Postgres
- [ ] meta-mangabaka dump ingest against the synthetic fixture: download, checksum (mismatch refused), zstd, SQLite read, mapping, merges, checkpoints
- [ ] Entry schema implemented: ProviderEntry stored as received (raw kept), merged Entry with per-field provenance, raw values kept next to enums
- [ ] meta ingest: idempotent re-sync, merge redirects resolve old IDs, removed-after-snapshot marking, sync runs recorded, attribution stored
- [ ] meta API: Browse (filters + sort), Search (multi-language titles via Postgres FTS + trigram behind `SearchIndex`), Get, LookupExternal, MetaAdmin; OpenAPI served
- [ ] meta-mangabaka lookup within rate limits, 429 back-off tested with a mock server
- [ ] Images build; the compose example and README quick starts work as written; docs cover config, protocol, writing a plugin, API
- [ ] Tests pass; `make check` passes; leak-check clean; no MangaBaka data committed
- [ ] `DONE:` sent with evidence: branches and commits per repo, test output, how to verify by hand (and real-dump numbers if run)

## History

- 2026-10-11: brief written from IN-0009 (`proposed`).
- 2026-10-11: entry schema added from the owner's schema ideas (IN-0010).
- 2026-10-11: owner gave the go; repos created: `accepted`, dispatched (IN-0011).
- 2026-10-11: production setup shares one Postgres server with server, a database each; dev doesn't matter (IN-0012, IN-0013).
- 2026-10-11: owner answers (IN-0014): Armeria accepted (ADR-0024); licences GPL-3.0 apps / Apache-2.0 protos and SDKs (ADR-0025); sessions may merge their own branches into `main` before the first release (no push); repos may cite KB IDs and link KB docs.
- 2026-10-11: REPORT: **slice 1 (scaffold) done** in both repos and merged into `main` (meta `e7763e4`, meta-mangabaka `ed0e201`; `main` created at the scaffold commit; not pushed). Go 1.26 module (toolchain go1.27.2); `make setup` pins tools into `./bin` (buf, sqlc, golangci-lint, govulncheck, protoc plugins incl. connect-go and connect-openapi); `make check` = fmt-check, vet, golangci-lint, buf lint (once protos exist), govulncheck, `go test -race -cover`. CI for meta runs postgres:18 with a non-superuser role (CREATEDB only), which proves meta needs no superuser; `buf breaking` on PRs. meta-mangabaka uses the SDK through a committed `replace => ../meta` and checks out meta beside it in CI. GPL-3.0 at both roots, SPDX `GPL-3.0-or-later`; Apache-2.0 for `proto/`, `gen/`, `sdk/` from slice 2. **Assumptions:** testcontainers (postgres:18) by default, or `META_TEST_DATABASE_URL`; global-gitignore names avoided. Keeper checked both `main` trees and ran leak-check (clean); `make check` not re-run. Next: slice 2 on `feat/proto-metadata-v1`.
- 2026-10-11: owner answers (IN-0015): SPDX `GPL-3.0-or-later` confirmed; Code of Conduct contact team@panelarr.app; ports server 8900, meta 8901, mihon-source 8902; source-mihon delegates stores to mihon-source; meta is a standalone service.
- 2026-10-11: plugin ports from 8903 confirmed; meta-mangabaka standalone on 8903 (IN-0016).
- 2026-10-11: meta's search engine integrations are optional and configurable, adapters later; they are meta's, not the library's (IN-0017, IN-0018).
