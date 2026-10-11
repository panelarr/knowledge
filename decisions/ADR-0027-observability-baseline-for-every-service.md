---
title: "ADR-0027: Observability baseline for every service"
status: accepted
tags: [ops, observability, logging, metrics, health]
related: [architecture/repo-standard.md, architecture/security.md, modules/mihon-source/overview.md, modules/meta/overview.md, modules/server/overview.md]
inputs: [IN-0024]
updated: 2026-10-11
---

# ADR-0027: Observability baseline for every service

- **Date:** 2026-10-11
- **Deciders:** @aurimasniekis

## Context

"services should all user confiurable struct json log and prometheus metrics and health endpoints and mihon can also have health endpoint for all configured sources, like it can do occasional self check which ones work or failing and etc" (IN-0024 §1). Today meta has configurable JSON/text logs and `/healthz` + `/readyz` but no metrics; mihon-source has a gRPC `Health`, plain-text logs, and metrics planned in GOAL-0005.

## Decision

Every Panelarr service (server, meta, mihon-source, plugins in standalone mode) provides:

- **Structured logs, configurable by the user:** format `json` (default) or `text`, and the level, via config and env. JSON lines carry at least time, level, message, service and component, plus context such as request ID and source or provider ID where relevant. Secrets, tokens, cookies and proxy credentials are never logged.
- **Prometheus metrics,** configurable: on/off, and a separate listen address or a scoped key, so they're not open on the public API port by default. Labels stay bounded: no URLs, user data or credentials.
- **Health endpoints:** `GET /healthz` (liveness), `GET /readyz` (readiness: own dependencies, e.g. the database) and a detailed health view for the admin and API (components, plugins, sources).
- **mihon-source extra:** **per-source health**, from an **occasional self-check** of configured sources (which work and which fail, with the error reason, e.g. `CLOUDFLARE_CHALLENGE`, `SOURCE_DOWN`), shown in the detailed health, metrics and admin UI.
  - *Suggestion:* configurable interval and per-source opt-out.
  - *Suggestion:* a light probe (e.g. the first page of popular), jittered and within the source's rate limits.
  - *Suggestion:* off by default, so no service hits sites unprompted (the opt-in principle; respect upstreams).

## Consequences

- The repo standard gains an observability section. Each goal brief carries it.
- Exact metric names and the self-check defaults are settled per service by REPORT.
