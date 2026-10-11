---
title: "GOAL-0001: mihon-source v0: run Mihon extensions over the source API"
status: proposed
tags: [goal, agents, mihon-source, mihon, kotlin]
related: [modules/mihon-source/overview.md, contracts/mihon-source-api.md, contracts/source-plugin.md, research/suwayomi-server.md, research/mihon-extensions.md, architecture/networking.md, architecture/repo-standard.md]
inputs: [IN-0005]
repos: [mihon-source]
session: "panelarr-mihon-source"
features: []
updated: 2026-10-11
---

# GOAL-0001: mihon-source v0: run Mihon extensions over the source API

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0001 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`proposed`: brief written for the owner to review (IN-0005). It becomes `accepted` when dispatched.

## Context

- Code: `~/Projects/Panelarr/mihon-source` (clone of `github.com/panelarr/mihon-source`, created by the owner) · no extra worktree (single session) · branches `<type>/<scope>-<slug>`, e.g. `feat/loader-dex2jar`
- Milestone: **M1 Mihon sources** ([roadmap](../../planning/roadmap.md)). There are no `FEAT-` docs for it yet. The DoD below stands in for acceptance criteria.
- **Read first, in this order:**
  1. [product/principles.md](../../product/principles.md): opt-in and composable. mihon-source must run **standalone**.
  2. [modules/mihon-source/overview.md](../../modules/mihon-source/overview.md): what this repo owns and what it doesn't. **This is the main spec.**
  3. [contracts/mihon-source-api.md](../../contracts/mihon-source-api.md) and [contracts/source-plugin.md](../../contracts/source-plugin.md): the two services you serve.
  4. [research/suwayomi-server.md](../../research/suwayomi-server.md) and [research/mihon-extensions.md](../../research/mihon-extensions.md): how extensions load on a plain JVM, the lib versions and the host classpath they expect.
  5. [architecture/networking.md](../../architecture/networking.md): per-source OkHttp clients, no JVM-global proxy.
  6. [architecture/repo-standard.md](../../architecture/repo-standard.md): files, workflows, `make` targets (proposed, follow it as guidance).
  7. ADRs: [ADR-0005](../../decisions/ADR-0005-layered-source-architecture.md), [ADR-0006](../../decisions/ADR-0006-technology-stack.md), [ADR-0008](../../decisions/ADR-0008-public-repo-standard-and-images.md), [ADR-0009](../../decisions/ADR-0009-plugins-not-bundled.md), [ADR-0020](../../decisions/ADR-0020-public-kb-with-aliases.md) are **accepted (law)**. [ADR-0012](../../decisions/ADR-0012-protobuf-grpc-contracts.md), [ADR-0013](../../decisions/ADR-0013-out-of-process-plugins.md), [ADR-0016](../../decisions/ADR-0016-per-source-network-profiles.md), [ADR-0019](../../decisions/ADR-0019-release-tooling.md) are proposed (strong guidance; build them cheap to change).
- **Aliases:** read `~/Projects/Panelarr/knowledge/.kb-aliases.env` (local, never committed). Write only the alias (e.g. `EXTREPO`) in code, comments, docs, commits, branch names and test fixtures.
- **Accepted decisions are law.** If code and KB disagree, the KB wins, or send `CONFLICT:`.

## Objective

Build **mihon-source v0**: a small Kotlin/JVM 21 service that installs Mihon extensions (jar, or APK via dex2jar), loads them in child-first classloaders behind our own Android shims, and serves their sources over the **`panelarr.source.v1`** API plus the small **`panelarr.mihon.v1`** admin API, over gRPC and HTTP/JSON with OpenAPI docs. It runs on its own: `docker run panelarr/mihon-source`, install an extension by URL, `curl /v1/sources/{id}/popular`. No store logic, no library, no database ([module](../../modules/mihon-source/overview.md)).

## Owner's choices for this goal (IN-0005 §2)

- **Protos live in this repo for now.** source-api (M0) isn't started. Write `proto/panelarr/source/v1/` and `proto/panelarr/mihon/v1/` here from the contract sketches, and build against them. They move to the `source-api` repo once it exists, so keep them self-contained: no Mihon- or JVM-specific types in `source.v1`, `buf lint` clean.
- **Our own Android shims.** Study Suwayomi's approach (AndroidCompat, dex2jar, classloaders, GraalJS behind the QuickJS API), but **copy no Suwayomi code**. Q-0003 is answered this way.
- **Git:** commit on your own feature branches. **Never push, never merge to `main`.** The owner pushes and merges.

## Slices (suggested order)

Each slice works end to end, has tests and ends with `make check` green and a `REPORT:`.

1. **Scaffold.** Gradle (Kotlin DSL, version catalog), JVM 21, `Makefile` with the standard targets (`help` default, `setup`, `build`, `test`, `lint`, `fmt`, `run`, `docker`, `gen`, `clean`, `check`), detekt + ktlint, `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `.github/` (CI workflow, PR title lint, PR template, issue templates), `docs/`. `AGENTS.md` from the KB's [kits/code-repo/AGENTS.public-repo.md](../../kits/code-repo/AGENTS.public-repo.md) plus a one-line `CLAUDE.md` with `@AGENTS.md`. **No `LICENSE` yet** (Q-0012 is open): note it in `README.md` as "licence to be decided".
2. **Protos + server skeleton.** The two proto packages, `buf lint` in `make check`, Kotlin codegen, a server answering `GetInfo`/`Health`/`ListSources` (empty) over gRPC and HTTP/JSON, with OpenAPI generated from the protos. The JVM RPC stack is open (Q-0020: Armeria vs grpc-kotlin + Ktor): do a short spike, `PROPOSE:` your pick with reasons, and keep it behind a thin layer.
3. **Extension loading + admin API.** `InstallExtension` from a URL or uploaded bytes (jar preferred, APK → jar via dex2jar, APK assets copied in), extension metadata and lib-version check (**1.4–1.6**), `Source`/`SourceFactory` instantiation, one child-first classloader per extension, `ListExtensions` / `UninstallExtension` / `ReloadExtension`. Report each extension's **signing fingerprint (SHA-256)**, and refuse an install when an expected SHA-256 or fingerprint is given and doesn't match. Load errors are reported per extension and never crash the service. Files under `/data/extensions/`.
4. **Host classpath + Android shims.** Vendored `eu.kanade.tachiyomi.source.*` API surface, including the EXTREPO lib 1.6 base source class. Host libraries matching extensions-lib 1.4–1.6 (OkHttp 5.x, jsoup, kotlinx.serialization, coroutines, Injekt, RxJava 1). Our own shims for what extensions use: Context, SharedPreferences (file-backed JSON in `/data/prefs/<sourceId>.json`), Base64, Log, Uri, Html, Bitmap/BitmapFactory, androidx.preference, QuickJS/Duktape API backed by GraalJS. ASM fix-ups where needed (e.g. SimpleDateFormat).
5. **Source API.** Map `SManga`/`SChapter`/`Page`/`FilterList` onto `source.v1`: `ListSources`, `GetFilters`, `Popular`, `Latest`, `Search`, `GetSeries`, `ListChapters`, `ListPages`, `FetchImage` (streamed), `ResolveUrl` where the source supports it. Prefs → `GetSettingsSchema` (JSON Schema) / `GetSettings` / `SetSettings`. Capabilities and error reasons as in [source-plugin](../../contracts/source-plugin.md). WebView-only sources report `needs_webview` and are otherwise unsupported (Q-0002 is open).
6. **Per-source networking.** One `OkHttpClient` per source built from its network profile: proxy (HTTP/SOCKS5 with auth), UA, rate limit (per source and per host), timeouts, per-source persisted cookie jar (`/data/cookies/<sourceId>.json`), and a solver interceptor (FlareSolverr/Byparr) **coalesced per host**. `SetNetworkProfile` applies a profile. **No JVM-global proxy properties.** Everything optional: with no profile the source goes direct.
7. **Image + docs.** Multi-arch Docker image `panelarr/mihon-source` (JRE 21, no browser), a `/data` volume, the standalone quick start in `README.md`, and `docs/` for configuration and the API.

## Tests and fixtures

- **No third-party extensions in the repo**: no binaries, no download URLs, no site names in tests or docs ([ADR-0020](../../decisions/ADR-0020-public-kb-with-aliases.md)).
- Build **your own small test extension(s)** inside the repo against the extensions-lib API (a lib 1.4-style `HttpSource` and a lib 1.6-style one), served by a local mock HTTP server (e.g. OkHttp `MockWebServer`). Use them for loader, shim, mapping and networking tests, including one that goes through the APK → dex2jar path if you can build an APK fixture cheaply; if not, `REPORT:` it and test the jar path.
- The owner may try real extensions by hand. That's not part of CI.

## How to work

1. Build in **slices**. Each slice works end to end (logic, interface, tests, docs).
2. One branch per slice. Conventional Commits (the repo's `CONTRIBUTING.md`).
3. After each slice: `make check` passes → `REPORT:` to the keeper with what you built, what you assumed and how to test it.
4. Keep `PROGRESS.md` in the repo: these slices ticked off, plus the next one. **Re-read it whenever you lose context.**
5. Don't stop after each slice to ask. Go on to the next one unless blocked on the owner's decision. The owner merges finished branches; you may branch the next slice off the previous one if it isn't merged yet, and say so in the REPORT.

## When something isn't decided

- `ASK:` the keeper first.
- Still open? `PROPOSE:` a concrete working assumption that fits the accepted decisions, then build it **cheap to change** (config/data, not hard-coded).
- Never present an assumption as decided, and never change an accepted decision yourself.
- Known open points you'll meet: Q-0020 (JVM RPC stack), Q-0007 (isolation: build one JVM with a classloader per extension, as planned), Q-0002 (WebView: out of scope), Q-0012 (licence: none yet), Q-0028 (no KB IDs in the repo).

## Constraints

- **Git:** commit on your own branches only. Never push, never merge to `main`, never rewrite `main`. No forge actions (issues, PRs, comments).
- **Public repo** ([ADR-0008](../../decisions/ADR-0008-public-repo-standard-and-images.md), [ADR-0020](../../decisions/ADR-0020-public-kb-with-aliases.md)): everything you write is public. Explain the *why* in your own words. **No KB IDs or KB paths** in code, docs, commits or branches until Q-0028 is answered. Aliases only. Never say where extensions can be obtained. Before each REPORT, run `python3 ~/Projects/Panelarr/knowledge/tools/kb.py leak-check mihon-source` (read-only; it scans the repo for KB references and real terms behind aliases).
- **Small tool:** no database, no store index parsing, no update policy, no trust decisions (only report the fingerprint and enforce an expected one), no users, no downloads queue.
- **Security:** extension code is untrusted. Don't give extensions access to the service's own files beyond their prefs/cookies, bound admin endpoints to config (listen address configurable), validate install URLs and sizes, and never log cookies or proxy credentials.
- **Opt-in:** FlareSolverr/Byparr, proxies and GraalJS-backed JS must all be optional at runtime. The service starts with none of them.

## Definition of Done

- [ ] Repo scaffolded to the repo standard (files, `make` targets, CI workflow, PR title lint), `make check` green locally
- [ ] `source.v1` and `mihon.v1` protos in `proto/`, `buf lint` clean, self-contained enough to move to source-api
- [ ] Service serves both APIs over gRPC and HTTP/JSON, with OpenAPI docs reachable from the running service
- [ ] Install by URL and by upload, jar and APK (dex2jar) paths; lib 1.4–1.6 accepted, others rejected with a clear error; fingerprint reported; expected SHA-256/fingerprint enforced; uninstall and reload work; a broken extension doesn't take the service down
- [ ] Own Android shims (no copied Suwayomi code); prefs and cookies persisted as files under `/data`
- [ ] Popular/Latest/Search with filters, GetSeries, ListChapters, ListPages and FetchImage work against the in-repo test extensions; settings schema/get/set work; error reasons mapped
- [ ] Per-source OkHttp clients from network profiles (proxy, UA, rate limit, cookies, solver interceptor coalesced per host); no JVM-global proxy settings; a test proves two sources use different proxies
- [ ] Docker image builds (`make docker`) and the standalone quick start in `README.md` works as written
- [ ] Tests pass; `make check` passes; leak-check clean
- [ ] Docs in the repo: `README.md`, `docs/` (configuration, API, architecture for contributors), `PROGRESS.md` current
- [ ] `DONE:` sent with evidence: branches and commits, test output, how to verify by hand

## History

- 2026-10-11: brief written from IN-0005 (`proposed`).
