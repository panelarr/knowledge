---
title: Public repo engineering standard
status: proposed
tags: [architecture, repos, ci, release, docs]
related: [decisions/ADR-0008-public-repo-standard-and-images.md, decisions/ADR-0019-release-tooling.md, decisions/ADR-0020-public-kb-with-aliases.md, meta/session-protocol.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# Public repo engineering standard

## Summary

Every Panelarr code repo is **public on GitHub** and must look and behave like a well-run open-source project, with full workflows for PRs, quality, tests, builds and releases, plus its own docs ([ADR-0008](../decisions/ADR-0008-public-repo-standard-and-images.md)). Code sessions apply this standard **in their own words**. Public repo docs stand on their own, but **may cite KB IDs and link KB docs** for deeper design (Q-0028, IN-0014). They always use the KB's aliases instead of the real terms ([ADR-0020](../decisions/ADR-0020-public-kb-with-aliases.md)).

## Required files
| File | Notes |
|---|---|
| `README.md` | What it is, standalone usage, quick start (docker + binary), config table, links to docs |
| `LICENSE` | GPL-3.0 for apps, Apache-2.0 for protos and SDKs, with a directory-level `LICENSE` where a repo holds both ([ADR-0025](../decisions/ADR-0025-licences-gpl-3-0-apps-apache-2-0-sdks-and-protos.md)) |
| `CONTRIBUTING.md` | Dev setup (`make setup`), Conventional Commits, PR process |
| `SECURITY.md` | Private vulnerability reporting via GitHub Security Advisories |
| `CODE_OF_CONDUCT.md` | Contributor Covenant. Contact: **team@panelarr.app** (IN-0015) |
| `.github/ISSUE_TEMPLATE/*`, `pull_request_template.md`, `CODEOWNERS` | |
| `docs/` | Usage, configuration, API (generated OpenAPI/proto docs), architecture-for-contributors. Optional public `docs/adr/`, written fresh |
| `Makefile` | `help` (default), `setup`, `build`, `test`, `lint`, `fmt`, `run`, `docker`, `gen` (protos/OpenAPI), `clean` |

## Workflows (`.github/workflows/`)
| Workflow | Trigger | Does |
|---|---|---|
| `ci.yml` | PR, push to main | lint → test → build. **Go:** `golangci-lint`, `go test -race -cover`, `go vet`, `govulncheck`. **Kotlin:** `detekt`, `ktlint`, `gradle test`. **Web:** Biome/ESLint, `tsc --noEmit`, Vitest, Playwright smoke. **Protos:** `buf lint`, `buf breaking` against main. Matrix: DB dialects (server/meta), OS/arch where relevant |
| `pr-title.yml` | PR | Conventional Commit title lint (squash-merge uses the title) |
| `codeql.yml` | PR, weekly | CodeQL for Go / Kotlin / JS |
| `release.yml` | push to main | **release-please** opens a release PR; merging it tags, writes CHANGELOG and creates the GitHub Release. **GoReleaser** attaches binaries and checksums (and plugin signatures + index entry for plugins) |
| `docker.yml` | tag (and main → `:edge`) | **Go repos:** done by GoReleaser in `release.yml`. **Others:** buildx multi-arch → `panelarr/<repo>:{version,major.minor,latest,edge}`, with SBOM + provenance, cosign-signed (proposed) |
| `docs.yml` | main | Build/publish docs (if the central docs site is chosen, [Q-0015](../questions/README.md)) |
| Renovate | schedule | Grouped dependency PRs; automerge patch versions when CI is green |

## Branching and commits
- `main` is protected: required checks, linear history, squash merge.
- Branches: `<type>/<scope>-<slug>`.
- Commit messages come from `/cc` (Conventional Commits) and feed release-please. KB IDs are welcome as `Refs:` footers (Q-0028), and never a real term behind an alias (`python3 tools/kb.py leak-check`).
- Git autonomy for code sessions: **before the first releases**, sessions may merge their own branches into `main` (Q-0010, IN-0014). Pushing needs the owner's word. Revisit at the first release.

## Observability ([ADR-0027](../decisions/ADR-0027-observability-baseline-for-every-service.md))
- Structured logs: `json` (default) or `text`, level configurable via config and env; no secrets in logs.
- Prometheus metrics, configurable, not open on the public port by default; bounded labels.
- `GET /healthz`, `GET /readyz`, and a detailed health view (components, plugins, sources).
- **As built:** meta: metrics off by default, `:9464` private listener or `metrics:read` scope, `GET /v1/admin/health`. mihon-source: `metrics` scope or optional `MIHON_METRICS_PORT`, JSON logs by default. *Suggestion: one scope name (`metrics:read`) and one default metrics port convention across services.*

## Quality bars
- Coverage is reported (Codecov or similar) but not gated at first. Gating starts once modules settle.
- Contract repos get a conformance suite that runs in CI against reference implementations.
- Every public API is documented (OpenAPI/proto comments rendered into docs).
