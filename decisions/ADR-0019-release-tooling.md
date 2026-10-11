---
title: "ADR-0019: Release-please, GoReleaser, buildx multi-arch, Renovate, CodeQL"
status: proposed
tags: [ci, release]
related: [architecture/repo-standard.md, decisions/ADR-0008-public-repo-standard-and-images.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# ADR-0019: Release and CI tooling

- **Date:** 2026-10-11 · **Deciders:** author (proposed)

## Decision (proposed)
- **Versioning:** **release-please** in every repo (Conventional Commits from `/cc` → semver, CHANGELOG, release PR → tag).
- **Go repos:** **GoReleaser**, which the author suggested (IN-0003 §8). It runs on the tag and builds:
  - cross-platform binaries (linux/darwin/windows × amd64/arm64), archives and checksums;
  - **multi-arch Docker images** `panelarr/<repo>` (`dockers` + `docker_manifests`, or `ko`);
  - SBOMs (syft);
  - **cosign signatures** for checksums and images;
  - for plugins, the plugin-index entry (via a post-hook or a small tool).
  This also covers the plugin artifacts a managed plugin host downloads ([ADR-0013](ADR-0013-out-of-process-plugins.md)).
- **Non-Go repos:** **docker buildx** multi-arch → `panelarr/<repo>` with SBOM and provenance (mihon-source, deploy AIO). web ships a `dist` tarball on GitHub Releases, which server embeds.
- **Dependencies and security:** **Renovate** for updates, **CodeQL** for security scanning, PR-title lint for Conventional Commits.
- **Contracts:** `buf lint` + `buf breaking` on proto repos.

Full detail: [repo-standard](../architecture/repo-standard.md).
