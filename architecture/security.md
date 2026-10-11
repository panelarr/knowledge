---
title: Security
status: draft
tags: [architecture, security]
related: [architecture/multi-user.md, architecture/plugins.md, decisions/ADR-0014-plugin-index-and-signing.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# Security

## Summary

There are three main risk areas: **running third-party code** (plugins, Mihon extensions), **multi-user data isolation**, and **secrets** (tracker tokens, proxy credentials). Panelarr is self-hosted and is often exposed through a reverse proxy, so it is treated as internet-facing.

## Third-party code
- **Plugins:** out of process ([ADR-0013](../decisions/ADR-0013-out-of-process-plugins.md)). Binaries are verified by SHA-256 and signature ([ADR-0014](../decisions/ADR-0014-plugin-index-and-signing.md)). Unsigned plugins need explicit admin trust. Each runs as the container user, with its own data dir.
- **Mihon extensions:** arbitrary JVM code inside mihon-source.
  - Verify the signing-key fingerprint against the store's `signingKey` (Suwayomi doesn't).
  - Run mihon-source as its own container with no access to `/data/library` or server's DB.
  - Process isolation per extension is open ([Q-0007](../questions/README.md)).
- **Containers:** non-root user (PUID/PGID), read-only root filesystem where possible, no Docker socket by default.

## Multi-user isolation
- Visibility scope is checked on **every** handler, including page and file streaming ([multi-user](multi-user.md)).
- Authorization has tests: a test matrix per role and grant runs in CI.

## Secrets
- Tracker tokens, proxy passwords and plugin API keys are encrypted at rest with a key in `/config` (or an env var), and never returned by the API once set.
- Service-to-service: API keys, or a local socket for managed plugins. Optional mTLS for remote plugins.

## Web
- HTTP-only, SameSite cookies, CSRF protection for cookie-auth mutations, a strict CSP for the SPA, rate-limited login, and audit logging of admin actions.
- Remote images go through the server image proxy, so the browser never hits sources directly. This avoids leaking user IPs and referers.

## Network profiles to plugins
- Hosts push network profiles, **including proxy passwords**, to plugins (mihon-source, meta plugins via `SetNetworkProfile`). Managed plugins get them over a local socket. **Remote plugins must be reached over a private network or TLS** (or mTLS), since the profile crosses the wire (GOAL-0003 slice 3).
