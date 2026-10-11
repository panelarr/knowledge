---
title: "GOAL-0001: mihon-source v0: run Mihon extensions over the source API"
status: accepted
tags: [goal, agents, mihon-source, mihon, kotlin]
related: [decisions/ADR-0021-mihon-source-standalone-admin.md, modules/mihon-source/overview.md, contracts/mihon-source-api.md, research/mihon-extension-store.md, architecture/security.md, contracts/source-plugin.md, research/suwayomi-server.md, research/mihon-extensions.md, architecture/networking.md, architecture/repo-standard.md]
inputs: [IN-0005, IN-0006, IN-0007, IN-0008, IN-0014]
repos: [mihon-source]
session: "panelarr-mihon-source"
features: []
updated: 2026-10-11
---

# GOAL-0001: mihon-source v0: run Mihon extensions over the source API

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0001 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`accepted`: dispatched to `panelarr-mihon-source` on 2026-10-11 (IN-0007 §2). Scope from IN-0005, widened with the minimal admin, clients and extension stores (IN-0006, ADR-0021). It becomes `accepted` when dispatched.

## Context

- Code: `~/Projects/Panelarr/mihon-source` (clone of `github.com/panelarr/mihon-source`, created by the owner; empty, no commits yet) · no extra worktree (single session) · branches `<type>/<scope>-<slug>`, e.g. `feat/loader-dex2jar`
- Milestone: **M1 Mihon sources** ([roadmap](../../planning/roadmap.md)). There are no `FEAT-` docs for it yet. The DoD below stands in for acceptance criteria.
- **Read first, in this order:**
  1. [product/principles.md](../../product/principles.md): opt-in and composable. mihon-source must run **standalone**.
  2. [ADR-0021](../../decisions/ADR-0021-mihon-source-standalone-admin.md) and [modules/mihon-source/overview.md](../../modules/mihon-source/overview.md): what this repo owns and what it doesn't. **These are the main spec.**
  3. [contracts/mihon-source-api.md](../../contracts/mihon-source-api.md) and [contracts/source-plugin.md](../../contracts/source-plugin.md): the two services you serve.
  4. [research/suwayomi-server.md](../../research/suwayomi-server.md), [research/mihon-extensions.md](../../research/mihon-extensions.md) and [research/mihon-extension-store.md](../../research/mihon-extension-store.md): how extensions load on a plain JVM, the lib versions and host classpath they expect, and the store index format.
  5. [architecture/networking.md](../../architecture/networking.md) (per-source OkHttp clients, no JVM-global proxy) and [architecture/security.md](../../architecture/security.md) (secrets at rest, untrusted code).
  6. [architecture/repo-standard.md](../../architecture/repo-standard.md): files, workflows, `make` targets (proposed, follow it as guidance).
  7. ADRs: [ADR-0021](../../decisions/ADR-0021-mihon-source-standalone-admin.md), [ADR-0006](../../decisions/ADR-0006-technology-stack.md), [ADR-0008](../../decisions/ADR-0008-public-repo-standard-and-images.md), [ADR-0009](../../decisions/ADR-0009-plugins-not-bundled.md), [ADR-0020](../../decisions/ADR-0020-public-kb-with-aliases.md) are **accepted (law)**. [ADR-0012](../../decisions/ADR-0012-protobuf-grpc-contracts.md), [ADR-0013](../../decisions/ADR-0013-out-of-process-plugins.md), [ADR-0016](../../decisions/ADR-0016-per-source-network-profiles.md), [ADR-0019](../../decisions/ADR-0019-release-tooling.md) are proposed (strong guidance; build them cheap to change).
- **Aliases:** read `~/Projects/Panelarr/knowledge/.kb-aliases.env` (local, never committed). Write only the alias (e.g. `EXTREPO`) in code, comments, docs, commits, branch names and test fixtures.
- **Accepted decisions are law.** If code and KB disagree, the KB wins, or send `CONFLICT:`.

## Objective

Build **mihon-source v0**: a small Kotlin/JVM 21 service that installs Mihon extensions (jar, or APK via dex2jar), loads them in child-first classloaders behind our own Android shims, and serves their sources over the **`panelarr.source.v1`** API plus the small **`panelarr.mihon.v1`** admin API, over gRPC and HTTP/JSON with OpenAPI docs. It runs on its own: `docker run panelarr/mihon-source`, install an extension by URL, `curl /v1/sources/{id}/popular`. It also has a **minimal admin** (a small React SPA served by the service) for browsing and testing sources, extension stores, clients with scoped API keys, and integrations (solvers, network profiles). No library, no users, no database ([ADR-0021](../../decisions/ADR-0021-mihon-source-standalone-admin.md)).

## Owner's choices for this goal (IN-0005 §2)

- **Protos live in this repo for now.** source-api (M0) isn't started. Write `proto/panelarr/source/v1/` and `proto/panelarr/mihon/v1/` here from the contract sketches, and build against them. They move to the `source-api` repo once it exists, so keep them self-contained: no Mihon- or JVM-specific types in `source.v1`, `buf lint` clean.
- **Our own Android shims.** Study Suwayomi's approach (AndroidCompat, dex2jar, classloaders, GraalJS behind the QuickJS API), but **copy no Suwayomi code**. Q-0003 is answered this way.
- **Git:** commit on your own feature branches. **Before the first release you may merge your own branches into `main` yourself** once `make check` is green (IN-0014): fast-forward or squash, keep history linear, never rewrite `main`. **Never push**: the owner pushes. No forge actions (issues, PRs, comments).
- **Minimal admin** (IN-0006): a small **React SPA** on the web module's stack (React + TanStack, [ADR-0006](../../decisions/ADR-0006-technology-stack.md)), built in a multi-stage image and served by the service. **One admin token** (env var, or generated on first start and printed once). Clients get **scoped API keys**. The admin manages **solvers, proxies/network profiles and extension stores**. **The admin is for people who run mihon-source standalone**, without the Panelarr stack. In the stack, the main app owns the config and source-mihon passes it to mihon-source through the same `mihon.v1` APIs with an admin-scope key (Q-0026/Q-0030, IN-0007 §1). So: **everything the SPA does must be a plain API call**, with no SPA-only logic, and config lives behind one interface.

## Slices (suggested order)

Each slice works end to end, has tests and ends with `make check` green and a `REPORT:`.

1. **Scaffold.** Gradle (Kotlin DSL, version catalog), JVM 21, `Makefile` with the standard targets (`help` default, `setup`, `build`, `test`, `lint`, `fmt`, `run`, `docker`, `gen`, `clean`, `check`), detekt + ktlint, `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `.github/` (CI workflow, PR title lint, PR template, issue templates), `docs/`. `AGENTS.md` from the KB's [kits/code-repo/AGENTS.public-repo.md](../../kits/code-repo/AGENTS.public-repo.md) plus a one-line `CLAUDE.md` with `@AGENTS.md`. **`LICENSE`: GPL-3.0** for the service, **Apache-2.0** for `proto/` (its own `LICENSE` there + SPDX headers) ([ADR-0025](../../decisions/ADR-0025-licences-gpl-3-0-apps-apache-2-0-sdks-and-protos.md)).
2. **Protos, server skeleton and auth.** The two proto packages (`source.v1`, and `mihon.v1` with the admin, stores, clients and integrations services from the [contract](../../contracts/mihon-source-api.md)), `buf lint` in `make check`, Kotlin codegen, a server answering `GetInfo`/`Health`/`ListSources` (empty) over gRPC and HTTP/JSON, with OpenAPI generated from the protos. **Auth from the start:** admin token, client API keys with scopes (`sources:read`, `admin`, suggested names), keys hashed at rest and shown once, `MihonClients` working. The JVM RPC stack is open (Q-0020: Armeria vs grpc-kotlin + Ktor): do a short spike, `PROPOSE:` your pick with reasons, and keep it behind a thin layer.
3. **Extension loading + admin API.** `InstallExtension` from a URL or uploaded bytes (jar preferred, APK → jar via dex2jar, APK assets copied in), extension metadata and lib-version check (**1.4–1.6**), `Source`/`SourceFactory` instantiation, one child-first classloader per extension, `ListExtensions` / `UninstallExtension` / `ReloadExtension`. Report each extension's **signing fingerprint (SHA-256)**, and refuse an install when an expected SHA-256 or fingerprint is given and doesn't match. Load errors are reported per extension and never crash the service. Files under `/data/extensions/`.
4. **Host classpath + Android shims.** Vendored `eu.kanade.tachiyomi.source.*` API surface, including the EXTREPO lib 1.6 base source class. Host libraries matching extensions-lib 1.4–1.6 (OkHttp 5.x, jsoup, kotlinx.serialization, coroutines, Injekt, RxJava 1). Our own shims for what extensions use: Context, SharedPreferences (file-backed JSON in `/data/prefs/<sourceId>.json`), Base64, Log, Uri, Html, Bitmap/BitmapFactory, androidx.preference, QuickJS/Duktape API backed by GraalJS. ASM fix-ups where needed (e.g. SimpleDateFormat).
5. **Source API.** Map `SManga`/`SChapter`/`Page`/`FilterList` onto `source.v1`: `ListSources`, `GetFilters`, `Popular`, `Latest`, `Search`, `GetSeries`, `ListChapters`, `ListPages`, `FetchImage` (streamed), `ResolveUrl` where the source supports it. Prefs → `GetSettingsSchema` (JSON Schema) / `GetSettings` / `SetSettings`. Capabilities and error reasons as in [source-plugin](../../contracts/source-plugin.md). WebView-only sources report `needs_webview` and are otherwise unsupported (Q-0002 is open).
6. **Per-source networking and integrations.** One `OkHttpClient` per source built from its network profile: proxy (HTTP/SOCKS5 with auth), UA, rate limit (per source and per host), timeouts, per-source persisted cookie jar (`/data/cookies/<sourceId>.json`), and a solver interceptor (FlareSolverr/Byparr) **coalesced per host**. `MihonIntegrations` manages solvers and profiles locally and assigns profiles per source; `SetNetworkProfile` (pushed by a host) overrides the local assignment. Proxy credentials encrypted at rest, never returned. **No JVM-global proxy properties.** Everything optional: with no profile the source goes direct.
7. **Extension stores.** `MihonStores`: add a store URL (`repo.json` → `index.pb` / JSON, legacy `index.min.json` as fallback), **pin its `signingKey` fingerprint**, refresh, list available extensions with installed version and update flag, install and update from the store (jar else APK) with the signing key and SHA-256 verified. Map `contentWarning` into the extension info. No store is configured by default.
8. **Admin SPA.** `admin/` (or `web/`) React + TanStack app, built by `make build` and served at `/`: log in with the admin token; **sources** (list, popular/latest/search with generated filter forms, details, chapters, page preview, settings form from the JSON Schema); **extensions** (install by URL/upload, uninstall, reload, load errors); **stores** (add, refresh, available, install/update); **clients** (create, rotate, delete, key shown once); **integrations** (solvers, profiles, per-source assignment). Minimal and functional: no design system work.
9. **Image + docs.** Multi-arch Docker image `panelarr/mihon-source` (multi-stage: Node builds the SPA, runtime is JRE 21 only, no browser), a `/data` volume, the standalone quick start in `README.md`, and `docs/` for configuration, auth and the API.

## Tests and fixtures

- **No third-party extensions in the repo**: no binaries, no download URLs, no site names in tests or docs ([ADR-0020](../../decisions/ADR-0020-public-kb-with-aliases.md)).
- Build **your own small test extension(s)** inside the repo against the extensions-lib API (a lib 1.4-style `HttpSource` and a lib 1.6-style one), served by a local mock HTTP server (e.g. OkHttp `MockWebServer`). Use them for loader, shim, mapping and networking tests, including one that goes through the APK → dex2jar path if you can build an APK fixture cheaply; if not, `REPORT:` it and test the jar path.
- For stores, serve an **in-repo fixture store** (`repo.json` + index + your test extensions, signed with a test key) from the mock server.
- The owner may try real extensions and stores by hand. That's not part of CI.

## How to work

1. Build in **slices**. Each slice works end to end (logic, interface, tests, docs).
2. One branch per slice. Conventional Commits (the repo's `CONTRIBUTING.md`).
3. After each slice: `make check` passes → `REPORT:` to the keeper with what you built, what you assumed and how to test it.
4. Keep `PROGRESS.md` in the repo: these slices ticked off, plus the next one. **Re-read it whenever you lose context.**
5. Don't stop after each slice to ask. Go on to the next one unless blocked on the owner's decision. Before the first release, merge each finished slice into `main` yourself once `make check` is green, then branch the next slice off `main`. Say what you merged in the REPORT.

## Parallel frontend (optional)

The owner suggested you may hand the admin SPA (slice 8) to a **sub-agent** working in parallel while you do the backend (IN-0008). It's your call when and whether it pays off. If you do it:

- **Start it after slice 2**, once `mihon.v1`/`source.v1` and the generated OpenAPI exist. The API is the contract between you. The sub-agent works against the generated TypeScript client plus a mock server or fixtures, and switches to the real service as slices land.
- **Ownership:** the sub-agent owns only `admin/` (the SPA and its build config). You own everything else, including `proto/`, the OpenAPI output and the `Makefile`. If the sub-agent needs an API change, it asks you; it never edits the protos or the backend.
- **Isolation:** give it its own git worktree and branch (`feat/admin-…`), off your latest slice. Same git rules: commit on its branch, never push. You merge its work, not the sub-agent.
- **You stay the only one who talks to the keeper.** Fold its progress into your `REPORT:`s and `PROGRESS.md`. Its work counts for slice 8 and the SPA DoD box only after you've checked it against the API and `make check` passes.

## When something isn't decided

- `ASK:` the keeper first.
- Still open? `PROPOSE:` a concrete working assumption that fits the accepted decisions, then build it **cheap to change** (config/data, not hard-coded).
- Never present an assumption as decided, and never change an accepted decision yourself.
- **Default port 8902** (server 8900, meta 8901; IN-0015). source-mihon will drive stores through your `MihonStores` API (Q-0031 answered), so keep it complete. Known open points you'll meet: Q-0007 (isolation: build one JVM with a classloader per extension, as planned), Q-0002 (WebView: out of scope).

## Constraints

- **Git:** commit on your own feature branches. **Before the first release you may merge your own branches into `main` yourself** once `make check` is green (IN-0014): fast-forward or squash, keep history linear, never rewrite `main`. **Never push**: the owner pushes. No forge actions (issues, PRs, comments).
- **Public repo** ([ADR-0008](../../decisions/ADR-0008-public-repo-standard-and-images.md), [ADR-0020](../../decisions/ADR-0020-public-kb-with-aliases.md)): everything you write is public. Explain the *why* in your own words. **You may cite KB IDs** (`ADR-`, `Q-`, `GOAL-`) in docs and in `Refs:` commit footers, and **link KB docs** at `https://github.com/panelarr/knowledge/blob/main/<path>` (Q-0028, IN-0014). Never local KB paths. Aliases only. Never say where extensions can be obtained. Before each REPORT, run `python3 ~/Projects/Panelarr/knowledge/tools/kb.py leak-check` with no arguments (read-only; it scans every registered repo, this one included, for KB references and real terms behind aliases). A bare repo name is read as a path relative to the KB and gets skipped.
- **Stay small:** no database (state is files under `/data`), no users beyond the admin token and clients, no library, no downloads queue. Stores are in scope; automatic update policy is not (show updates, install on request).
- **Security:** extension code is untrusted. Don't give extensions access to the service's own files beyond their prefs/cookies, validate install and store URLs and sizes, and never log tokens, keys, cookies or proxy credentials. Every endpoint except `Health` needs a key. The admin token and API keys are hashed at rest; proxy credentials encrypted; none returned once set. The SPA uses the token via an `Authorization` header (no cookie, so no CSRF surface) and a strict CSP.
- **Opt-in:** FlareSolverr/Byparr, proxies and GraalJS-backed JS must all be optional at runtime. The service starts with none of them.

## Definition of Done

- [ ] Repo scaffolded to the repo standard (files, `make` targets, CI workflow, PR title lint), `make check` green locally
- [ ] `source.v1` and `mihon.v1` protos in `proto/`, `buf lint` clean, self-contained enough to move to source-api
- [ ] Service serves both APIs over gRPC and HTTP/JSON, with OpenAPI docs reachable from the running service
- [ ] Admin token and scoped client API keys enforced on every endpoint but `Health`; keys hashed, shown once, rotatable; a test proves a `sources:read` key can't call admin APIs
- [ ] Install by URL and by upload, jar and APK (dex2jar) paths; lib 1.4–1.6 accepted, others rejected with a clear error; fingerprint reported; expected SHA-256/fingerprint enforced; uninstall and reload work; a broken extension doesn't take the service down
- [ ] Own Android shims (no copied Suwayomi code); prefs and cookies persisted as files under `/data`
- [ ] Popular/Latest/Search with filters, GetSeries, ListChapters, ListPages and FetchImage work against the in-repo test extensions; settings schema/get/set work; error reasons mapped
- [ ] Per-source OkHttp clients from network profiles (proxy, UA, rate limit, cookies, solver interceptor coalesced per host); no JVM-global proxy settings; a test proves two sources use different proxies
- [ ] Solvers and profiles managed through `MihonIntegrations`; a pushed `SetNetworkProfile` overrides the local assignment
- [ ] Stores: add, refresh, list available, install/update from a store against an in-repo fixture store; signing-key mismatch refused; legacy index fallback tested
- [ ] Admin SPA covers sources (browse, search with filters, details, chapters, page preview, settings), extensions, stores, clients and integrations, logging in with the admin token
- [ ] Docker image builds (`make docker`) and the standalone quick start in `README.md` works as written
- [ ] Tests pass; `make check` passes; leak-check clean
- [ ] Docs in the repo: `README.md`, `docs/` (configuration, API, architecture for contributors), `PROGRESS.md` current
- [ ] `DONE:` sent with evidence: branches and commits, test output, how to verify by hand

## History

- 2026-10-11: brief written from IN-0005 (`proposed`).
- 2026-10-11: widened with the minimal admin SPA, clients and API keys, integrations and extension stores (IN-0006, ADR-0021).
- 2026-10-11: admin clarified as standalone-only; the Panelarr stack configures mihon-source through source-mihon (IN-0007 §1). Owner created the repo and gave the go: `accepted`, dispatched (IN-0007 §2).
- 2026-10-11: optional parallel frontend sub-agent for slice 8 (IN-0008).
- 2026-10-11: REPORT: **slice 1 (scaffold) done** on `chore/repo-scaffold` @ `16ad730` (root commit). Gradle 9.8.1 + Kotlin DSL + version catalog + `build-logic/` conventions (Kotlin 2.4.21, JVM 21, detekt 2.0.0-alpha.6, ktlint, JUnit 6); `Makefile` targets wrap Gradle tasks (the owner asked the session to "use gradle if possible"); repo docs, `docs/`, `PROGRESS.md`, `.github/` (ci, pr-title, templates, CODEOWNERS). Not yet: CodeQL, release-please, Renovate, docker.yml (ADR-0019 proposed; docker.yml in slice 9). Assumption: CoC contact is a private GitHub report or the org profile contact. Keeper checked the branch file list and ran leak-check (clean); `make check` not re-run by the keeper. Next: slice 2 on `feat/api-protos-auth`.
- 2026-10-11: REPORT: **slice 2 (protos, server skeleton, auth) done** on `feat/api-protos-auth` @ `2124d96` (off `chore/repo-scaffold`, which got fix-up `ab391f7`: the owner's global gitignore has `/server/` and `*.jar`, so the Gradle module was silently left out; it is now named `service`). `make check` green (20 tests). Protos `panelarr/source/v1` and `panelarr/mihon/v1`, buf STANDARD lint, buf run through Gradle. One port serves gRPC, gRPC-Web and HTTP/JSON transcoding; `/openapi.yaml` generated from the protos (CI fails when stale); Swagger UI at `/docs/`; reflection admin-only. Auth: admin token (env or generated, printed once, hashed), `msk_` client keys SHA-256 hashed, scopes `sources:read`, `sources:write`, `admin`; tests prove a read key is denied admin APIs over gRPC and HTTP. **Assumptions:** buf STANDARD names (`SourcePluginService`, `MihonAdminService`, … with Request/Response per RPC); a third scope `sources:write` (SetSettings, SetNetworkProfile); SHA-256 for random 256-bit tokens; JSON errors use Armeria's body, **not `application/problem+json`** as [contracts and transport](../../architecture/contracts-and-transport.md) says, to revisit in slice 5. **PROPOSE:** Armeria for the JVM RPC stack (Q-0020), recorded as a working assumption. Frontend sub-agent started on `feat/admin-spa` (owns `admin/`). Keeper checked the branch file list and ran leak-check (clean); `make check` not re-run. Next: slice 3 on `feat/extension-loader`.
- 2026-10-11: REPORT from `panelarr-mihon-source`: started; read the brief and its docs; slice 1 (scaffold) in progress on `chore/repo-scaffold`.
- 2026-10-11: owner answers (IN-0014): Armeria accepted (ADR-0024); licences GPL-3.0 apps / Apache-2.0 protos and SDKs (ADR-0025); sessions may merge their own branches into `main` before the first release (no push); repos may cite KB IDs and link KB docs.
- 2026-10-11: owner answers (IN-0015): SPDX `GPL-3.0-or-later` confirmed; Code of Conduct contact team@panelarr.app; ports server 8900, meta 8901, mihon-source 8902; source-mihon delegates stores to mihon-source; meta is a standalone service.
- 2026-10-11: Q-0020 closed (IN-0019, ADR-0026): ConnectRPC on Go; **standard gRPC is the canonical wire** every service and plugin must speak; REST/JSON per google.api.http; Connect optional.
