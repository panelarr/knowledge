---
title: "GOAL-0005: mihon-source v0.1 follow-ups"
status: accepted
tags: [goal, agents, mihon-source]
related: [agents/goals/GOAL-0001-mihon-source-v0-run-mihon-extensions-over-the-source-api.md, modules/mihon-source/overview.md, contracts/source-plugin.md, contracts/mihon-source-api.md]
inputs: [IN-0024, IN-0025, IN-0027]
repos: [mihon-source]
session: "panelarr-mihon-source"
features: []
updated: 2026-10-11
---

# GOAL-0005: mihon-source v0.1 follow-ups

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0005 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`accepted`, **Done 2026-10-11** (verified; [test report](../../qa/reports/goal-0005-mihon-source-v0-1-done-verification.md)). The owner gave this list to `panelarr-mihon-source` directly (confirmed, IN-0025).

## Context

- Code: `~/Projects/Panelarr/mihon-source` · one branch per item · same rules as GOAL-0001 (merge your own branches before the first release, never push, leak-check, aliases, KB IDs allowed).
- Builds on the [GOAL-0001](GOAL-0001-mihon-source-v0-run-mihon-extensions-over-the-source-api.md) v0 and the [module](../../modules/mihon-source/overview.md).

## Objective

The owner's follow-up list for mihon-source, in this order:

1. **Extension icons:** served by the service, both for installed extensions (from the extension file) and for store icons proxied through the service; shown in the admin UI.
2. **Metrics:** per-source request counts, errors and latency as a Prometheus endpoint.
3. **Container hardening docs:** read-only root filesystem, only `/data` writable, guidance for untrusted extensions. **Plus a VPN example** (IN-0027): **gluetun** running an OpenVPN or WireGuard config and exposing its HTTP proxy, with a network profile pointing at it (e.g. `vpn → http://gluetun:8888`) for chosen sources. Mention the alternative `network_mode: "service:gluetun"` (all traffic through the VPN, all or nothing) with its trade-offs. A compose snippet with placeholders only: no provider credentials, no real server names.
4. **Compatibility checker:** a generic CLI that works against a running service. By default it installs and loads; selected calls are optional (popular, latest, search, details, chapters, pages, image). It can target all extensions, a random N, or a name/lang filter, and writes a report.
5. **Android-style date parsing:** an ICU-backed `SimpleDateFormat` replacement via bytecode rewrite (planned in the module's "ASM fix-ups").
6. **Scheduled store refresh,** configurable.
7. **ResolveUrl:** a search-based fallback for sources that accept a pasted URL as a query.
8. **Result cache:** a short-TTL in-memory cache of source API results, with concurrent identical calls merged into one, invalidation on settings, profile and extension changes, `Cache-Control: no-cache` bypass and configurable TTLs. **Images are not cached** (the owner's choice).
9. **Structured logs** ([ADR-0027](../../decisions/ADR-0027-observability-baseline-for-every-service.md)): `json` (default) or `text` and the level, configurable via config and env (today logback is plain text only). Add `/healthz` and `/readyz` next to the gRPC `Health` if they're missing.
10. **Per-source health with a self-check** (IN-0024): occasionally probe configured sources (suggestion: the first page of popular, jittered, within rate limits; interval configurable; per-source opt-out; **off by default**). Record per source: ok / failing with the error reason (`CLOUDFLARE_CHALLENGE`, `SOURCE_DOWN`, `NEEDS_WEBVIEW`, …), latency and last checked. Show it in a detailed health endpoint, metrics and the admin UI (Sources and Extensions). Also report it through the source API (e.g. per-source status in `ListSources`/`GetSource`, additive).

## Constraints (keeper notes, from the KB)

- **Compatibility checker:** it runs against the owner's real stores locally. **Reports must stay out of git** (write to a git-ignored path by default). No extension, store or site names in code, tests, docs or commits ([ADR-0020](../../decisions/ADR-0020-public-kb-with-aliases.md)). Tests use the in-repo test extensions and fixture store.
- **Scheduled store refresh** refreshes indexes only. It must **not auto-install updates**: v0 shows updates and installs on request, and update policy isn't decided.
- **Metrics:** don't expose them unauthenticated on the public port by default. Require a key or scope, or use a separate configurable listen address. No URLs with query strings or credentials in labels; keep label cardinality bounded (source ID, operation, outcome).
- **Result cache:** keyed per source, operation and arguments; no user data in keys; size-bounded.
- **ResolveUrl:** a fallback only when the source has no native resolver, and reported as best-effort in the capability.

## Definition of Done

- [x] Logs, metrics and health meet ADR-0027; per-source self-check with status in health, metrics and the UI
- [x] Each item merged with tests; `make check` green; leak-check clean
- [x] Docs updated (configuration, API, hardening, checker usage)
- [x] A REPORT after each merge; `DONE:` with evidence per item

## History

- 2026-10-11: recorded from `panelarr-mihon-source`'s REPORT of the owner's direct request (`proposed` until the owner confirms to the keeper).
- 2026-10-11: items 9 (structured logs) and 10 (per-source health self-check) added from the owner (IN-0024, ADR-0027).
- 2026-10-11: owner confirmed (IN-0025): `accepted`.
- 2026-10-11: REPORT: **item 1 (icons) merged** (`4d91e3f`). Taken from the highest-density launcher icon in the APK or jar, falling back to the store's icon URL at install; max 512 KB, type checked. Routes: `/v1/sources/{id}/icon` (sources:read), admin extension and store-icon proxy (cached a week). `Source.icon_url` is a plugin-relative path. Admin UI shows icons with a letter fallback, and nothing loads from third parties. Next: items 2 + 9 (metrics, logs, health), then 3, then 4 + 10, then 5–8.
- 2026-10-11: REPORT: **items 2 (metrics) and 9 (logs, health) merged** (`168bc7b`). Prometheus via Micrometer: JVM, per-source call timings by source/operation/outcome, solver solves, extension and source counts, with bounded labels (a test checks no site URL appears). `/metrics` needs the new `metrics` scope (or admin) on the API port, or runs unauthenticated on an optional separate `MIHON_METRICS_PORT`. JSON logs by default (`MIHON_LOG_FORMAT`, `MIHON_LOG_LEVEL`). `/healthz` and `/readyz` without credentials. Meets ADR-0027 except the per-source self-check (item 10). Next: the SOCKS5 auth gap fix (GOAL-0001), then hardening docs.
- 2026-10-11: the owner asked for a gluetun VPN-to-proxy example in the docs (IN-0027), added to item 3.
- 2026-10-11: REPORT: **item 3 (hardening + VPN docs) merged** (`aa199db`, plus lint fix `e5f4fb8`). `docs/deployment.md`: why the container is the boundary, a hardening table (read-only root, tmpfs /tmp, cap_drop ALL, no-new-privileges, uid 10001, limits), secrets via `_FILE`, a TLS reverse proxy, keeping metrics internal, and the gluetun VPN recipe (HTTP proxy 8888 + profile; the `network_mode` alternative; why not run tunnels). Hardening verified on the real image. A hardened `compose.example.yaml`. New: every `MIHON_*` var accepts `NAME_FILE`. **Process slip, owned by the session:** a lint failure was merged and fixed in the next commit; merges are now gated on the check result.
- 2026-10-11: REPORT: **item 10 (per-source health) merged** (`bcd643c`, gated on `make check`). A shared prober walks popular → latest → search → details → chapters → pages → image (first 64 KB), through each source's profile and limits, with metrics labelled `check_*`. `CheckSources` (`POST /v1/admin/checks`) and per-source opt-out (`SetHealthCheck`). `Source.health` (OK / FAILING + reason, incl. NEEDS_WEBVIEW; latency; checked_at; checks_disabled) in `ListSources`/`GetSource` (additive). Scheduled self-check **off by default** (`MIHON_HEALTH_CHECK_INTERVAL`), popular page 1, random order, jittered, persisted. Gauge `mihon_source_health`. Admin UI: health column, badge, "Check now", per-source switch. Next: item 4 (compatibility checker CLI on CheckSources).
- 2026-10-11: REPORT: **item 4 (compatibility checker) merged** (`ce4e1f9`). `make compat ARGS=…` drives a running service with the admin token: adds a store if needed; selects all / random N (seeded) / package list, with lang and query filters; **load-only by default (no site calls)**; `--checks` runs the item-10 probe; uninstalls what it installed unless `--keep`; classifies load failures (missing class/member, bad bytecode, needs WebView, unsupported lib, signature) and groups failing checks by step and reason. Reports go to the git-ignored `build/compat-reports/` (keeper checked: ignored, none committed, leak-check clean). **Real-world sample (local only):** 30/30 random extensions loaded with no host-API gaps; 5 of 10 passed the full popular → image walk, 3 hit Cloudflare challenges (no solver set in that dev data), 2 failed on the site side.
- 2026-10-11: REPORT: **item 5 (Android-style dates) merged** (`cfd8a5b`). The evidence was real: ICU vs JDK differ on `ZZZZZ` (ISO offsets) and `SSSSSS` (fractions). `IcuSimpleDateFormat` (ICU4J) in android-compat, plus a class-definition rewrite of `new SimpleDateFormat` in extensions (jar and dex2jar paths; byte-scan skip). Tests, including end to end. Local regression: 25/25 loaded, 20 of 27 sources passed through chapters with dates parsed, no rewrite errors. Next: item 6 (store refresh, indexes only).
- 2026-10-11: REPORT: **item 6 (scheduled store refresh) merged** (`75e70b4`). Every `MIHON_STORE_REFRESH_INTERVAL` (default 12h + up to 10% jitter; `0`/`off` disables): indexes only, never auto-install; errors recorded on the store and retried; the key pin is enforced on every refresh; available updates are logged. Next: item 7 (ResolveUrl fallback).
- 2026-10-11: REPORT: **item 7 (ResolveUrl fallback) merged** (`22ab5f6`). Native resolvers first; otherwise search same-site sources with the URL as the query and accept a URL-matching result (or the single result); additive `ResolveUrlResponse.best_effort`; the `RESOLVE_URL` capability still means native only. Next: item 8 (result cache).
- 2026-10-11: **Logo** (IN-0030/0031, [brand](../../product/brand.md)): add `panelarr-icon.svg` to the admin UI (header lockup "Panelarr Mihon Source", favicon, login, page title); a small follow-up task.
- 2026-10-11: REPORT: **item 8 (result cache) merged** (`8de2708`). In memory, default 5 m for lists and search, 10 m for details and chapters, 30 m for pages, 1 h for filters; size-bounded LRU (64 MB); keys are source + operation + a request hash (no user data); identical calls share one request; no-cache bypass; errors and images never cached; invalidated on settings, profile, extension and integration changes; hit/miss metric. **Logo added** (`7a442e0`): header lockup, login, favicon, page title, CC BY 4.0 note. DONE to follow.
- 2026-10-11: **DONE received and verified.** Clean clone of `main` @ `7a442e0`: 138 JUnit + 76 Vitest, 0 failures; DoD ticked ([test report](../../qa/reports/goal-0005-mihon-source-v0-1-done-verification.md)).
- 2026-10-11: post-done, owner-requested: `refresh` flag on GetSeries/ListChapters to bypass and replace the cache (`db067fc`); noted in contracts/source-plugin.md.
