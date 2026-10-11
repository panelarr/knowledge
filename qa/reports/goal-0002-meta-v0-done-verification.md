---
title: "Test report: GOAL-0002 meta v0 DONE verification"
status: draft
tags: [qa, report, meta, meta-mangabaka]
related: [agents/goals/GOAL-0002-meta-v0-metadata-protocol-meta-service-and-mangabaka-dump-in.md, modules/meta/overview.md, modules/meta-mangabaka/overview.md]
updated: 2026-10-11
---

# Test report: GOAL-0002 meta v0 DONE verification

- **Build under test:** meta@fca9551, meta-mangabaka@15c03d8 (local `main`s, not pushed)
- **Plan:** the [GOAL-0002 Definition of Done](../../agents/goals/GOAL-0002-meta-v0-metadata-protocol-meta-service-and-mangabaka-dump-in.md#definition-of-done)
- **Tester:** panelarr-knowledge, plus the owner's real-dump run of the plugin
- **Verdict:** **pass**

## Results

| Case | Result | Notes / evidence |
|---|---|---|
| `make setup && make check` in a clean clone of meta `main` | pass | Exit 0. golangci-lint `0 issues`, govulncheck `No vulnerabilities found`; every package with tests `ok` (cmd/meta, api, catalog, config, enums, ingest, store, textnorm, sdk/client, sdk/conformance, sdk/plugin, sdk/settings); no skipped tests, so the Postgres tests ran (testcontainers) |
| `make setup && make check` in a clean clone of meta-mangabaka `main`, beside the meta clone (`replace => ../meta`) | pass | Exit 0; cmd, api, dump, mangabaka and mapping tests `ok`; no skips |
| DoD evidence per box | pass (as reported) | The session's DONE names a test for each box (conformance over every transport, migrate up/down, no-superuser, idempotent re-sync, redirects, snapshot removal, Browse/Search/Get/Lookup, 429 back-off, the end-to-end serve test) |
| Owner's real-dump run (plugin only) | pass | 564,040 series read and mapped in 1m27s after the relative-path fix ([research](../../research/mangabaka.md)) |
| No MangaBaka data committed | pass | Fixtures are generated in Go; `data/`, `*.sqlite`, `*.zst` git-ignored; leak-check clean |

## Bugs found

- Relative download dir broke the SQLite DSN (found by the owner's run). Fixed in meta-mangabaka `5dec196`, with regression tests.

## Risks and untested areas

- The keeper did not build the images or run the compose quick start; the session reports it did (meta healthy, provider OK, 401 without a key).
- **A full real-dump ingest into Postgres hasn't been run yet.** The projected ~8–9 min and ~4–5 GB come from synthetic data. The owner's compose run is the real acceptance test. The Docker Desktop disk was near full during the session's scale tests.
- Release workflows haven't run (nothing pushed; Docker Hub secrets needed). meta-mangabaka depends on `replace => ../meta` until meta is tagged.
- Working assumptions still open for the owner: same-provider linking, name-only people shared by name, `is_licensed` read as English.
