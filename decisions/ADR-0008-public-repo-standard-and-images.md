---
title: "ADR-0008: Full GitHub workflows, public docs and panelarr/<repo> images for every repo"
status: accepted
tags: [repos, ci, release, docker]
related: [architecture/repo-standard.md, decisions/ADR-0019-release-tooling.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# ADR-0008: GitHub workflows, docs, images

- **Date:** 2026-10-11 · **Deciders:** author

## Decision
- Every repo defines **full GitHub workflows**: PR checks, code quality, tests, builds and releases.
- Every repo has its **own public docs**.
- Container images publish as **`panelarr/<repo>`**.

The concrete standard is in [repo-standard](../architecture/repo-standard.md). The tool choices in it are [ADR-0019](ADR-0019-release-tooling.md), still proposed.
