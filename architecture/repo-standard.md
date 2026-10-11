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

Every Panelarr code repo is **public on GitHub** and must look and behave like a well-run open-source project, with full workflows for PRs, quality, tests, builds and releases, plus its own docs ([ADR-0008](../decisions/ADR-0008-public-repo-standard-and-images.md)). Code sessions apply this standard **in their own words**. Public repo docs stand on their own. Until [Q-0028](../questions/README.md) is answered they don't cite KB IDs, and they always use the KB's aliases instead of the real terms ([ADR-0020](../decisions/ADR-0020-public-kb-with-aliases.md)).

## Required files
| File | Notes |
|---|---|
| `README.md` | What it is, standalone usage, quick start (docker + binary), config table, links to docs |
| `LICENSE` | Per [Q-0012](../questions/README.md) |
| `CONTRIBUTING.md` | Dev setup (`make setup`), Conventional Commits, PR process |
| `SECURITY.md` | Private vulnerability reporting via GitHub Security Advisories |
| `CODE_OF_CONDUCT.md` | Contributor Covenant |
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
- Commit messages come from `/cc` (Conventional Commits) and feed release-please. No KB IDs in messages until [Q-0028](../questions/README.md) is answered, and never a real term behind an alias (`python3 tools/kb.py leak-check`).
- Git autonomy for code sessions is not settled ([Q-0010](../questions/README.md)).

## Quality bars
- Coverage is reported (Codecov or similar) but not gated at first. Gating starts once modules settle.
- Contract repos get a conformance suite that runs in CI against reference implementations.
- Every public API is documented (OpenAPI/proto comments rendered into docs).
