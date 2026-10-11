# Open questions register

Everything we don't know yet. IDs are stable and never reused. When a question is answered, move its row to **Answered** and link to where the answer now lives. Don't delete rows. A big question also gets its own file `Q-NNNN-slug.md` ([template](../meta/templates/question.md)). Add one with `python3 tools/kb.py new question "…" --area <area> --pri P2`.

**Priority:** `P1` blocks current work · `P2` important, not blocking · `P3` later.

## Open

| ID | Question | Area | Pri | Raised in |
|---|---|---|---|---|
| Q-0001 | Go data layer: ent + Atlas vs bun vs sqlc + goose for SQLite/Postgres/MySQL? *Leaning ent + Atlas ([ADR-0018](../decisions/ADR-0018-ent-atlas-data-layer.md)).* | server, meta | P1 | [server](../modules/server/overview.md) |
| Q-0002 | WebView engine for WebView-only Mihon sources: KCEF/JCEF in-process (Suwayomi) vs a headless Chromium sidecar over CDP? Or skip those sources at first? | mihon-source | P2 | [mihon-source](../modules/mihon-source/overview.md) |
| Q-0004 | Tracker OAuth on self-hosted instances (different redirect URI each time): per-instance client registration, PIN/copy-token flows, or a relay? | server, trackers | P2 | [trackers](../architecture/trackers.md) |
| Q-0005 | Default ports for server, meta, mihon-source and plugins. Avoid clashes with other *arr* apps (8989, 7878, 8686, 9696, …). | deploy | P3 | [deployment](../architecture/deployment.md) |
| Q-0006 | By default, is meta embedded in server (one container) or a separate service? | meta, deploy | P2 | [meta](../modules/meta/overview.md) |
| Q-0007 | Extension isolation in mihon-source: all extensions in one JVM (classloader per extension) vs a JVM pool or per-extension processes for crash and memory isolation? | mihon-source | P3 | [mihon-source](../modules/mihon-source/overview.md) |
| Q-0008 | Web UI component kit and styling (e.g. shadcn/ui + Tailwind, Mantine, Park UI)? | web | P2 | [web](../modules/web/overview.md) |
| Q-0009 | Which other extension ecosystems might get source plugins later (Paperback, Aidoku, Kotatsu…)? | sources | P3 | [plugins](../architecture/plugins.md) |
| Q-0010 | Code-session git autonomy: may code sessions commit and merge on branches themselves, or only on request? Who may merge to main and push? *For GOAL-0001 only: commit on its own branches, never push or merge; the owner pushes and merges (IN-0005 §2).* | process | P1 | [session protocol](../meta/session-protocol.md) |
| Q-0011 | Is MySQL/MariaDB support worth its cost? Review after the first migrations and FTS work. | server | P3 | [ADR-0004](../decisions/ADR-0004-database-portability.md) |
| Q-0012 | Licence per public repo (the KB itself was set up as MIT tooling + CC BY 4.0 docs by the template default; confirm): GPL-3.0 (like the *arrs) vs AGPL vs MPL-2.0 vs Apache-2.0. Plugin SDKs may want a permissive licence; mihon-source no longer reuses Suwayomi code (Q-0003), so it has no inherited constraint; it ships without a `LICENSE` until this is answered. | legal | P1 | [repo standard](../architecture/repo-standard.md) |
| Q-0013 | Is the GitHub org **panelarr** available? Is Docker Hub org `panelarr` secured? | repos | P1 | [repo standard](../architecture/repo-standard.md) |
| Q-0014 | Docker Hub only, or also mirror to ghcr.io/panelarr? | deploy | P3 | [repo standard](../architecture/repo-standard.md) |
| Q-0015 | Central docs site (a `docs` repo with Starlight/Docusaurus on GitHub Pages) vs per-repo `docs/` only? | repos | P2 | [repo standard](../architecture/repo-standard.md) |
| Q-0016 | Legal and ToS stance and wording: no bundled extensions or plugins; hosters add indexes; disclaimers; DMCA contact. | legal | P2 | [principles](../product/principles.md) |
| Q-0017 | Plugin repo layout: one repo per plugin (`meta-anilist`, …) or a `plugins` monorepo per kind? | repos | P2 | [plugins](../architecture/plugins.md) |
| Q-0018 | When to support PDF and EPUB in source-local (PDF needs a rasterizer, which may require cgo)? | source-local | P3 | [source-local](../modules/source-local/overview.md) |
| Q-0019 | Rules for inferring series, volume and chapter from file and folder names when there is no ComicInfo. | source-local | P2 | [formats](../research/comic-archive-formats.md) |
| Q-0020 | RPC stack: ConnectRPC (Go) + gRPC-JSON transcoding on the JVM (Armeria? grpc-kotlin + Ktor?) and OpenAPI generation from protos. Is gRPC the primary wire for remote plugins, with JSON optional? | contracts | P1 | [ADR-0012](../decisions/ADR-0012-protobuf-grpc-contracts.md) |
| Q-0021 | Should trackers become a plugin kind (like sources and metadata), or stay built into server? | trackers | P3 | [trackers](../architecture/trackers.md) |
| Q-0022 | Search backends: Typesense first (author's suggestion) then Meilisearch? Is embedded Bleve worth adding? Benchmark CJK title search. | search | P2 | [search](../architecture/search.md) |
| Q-0023 | Where does character data come from (AniList, ComicVine)? Is it stored in meta and indexed for search? | meta, search | P3 | [search](../architecture/search.md) |
| Q-0024 | Plugin signing: key format (minisign vs cosign/sigstore), official key management, the trust UI for third-party indexes. | plugins, security | P2 | [plugin index](../contracts/plugin-index.md) |
| Q-0025 | Should Panelarr be a Mihon "enhanced tracker" / Mihon extension target (like Komga), so the Mihon app can read from and sync with Panelarr? | product | P3 | [trackers research](../research/trackers.md) |
| Q-0026 | Now that mihon-source speaks the source-api protos itself: is source-mihon a pass-through plugin plus store manager, or only a store/trust library used by the plugin host? | sources | P1 | [source-mihon](../modules/source-mihon/overview.md) |
| Q-0027 | Should server auto-discover remote plugins in the same Compose project (mDNS/DNS-SD, self-registration with a join token, DNS probing, Docker labels)? Discovered plugins are only suggested, never auto-enabled. | plugins, deploy | P3 | [plugins](../architecture/plugins.md) |
| Q-0028 | Now that the KB is public: may code repos cite KB IDs (`ADR-`, `Q-`, `FEAT-`), link KB docs, or use `Refs:` footers? Until answered, they don't. | process | P2 | [ADR-0020](../decisions/ADR-0020-public-kb-with-aliases.md) |

## Answered

| ID | Question | Answer |
|---|---|---|
| Q-0003 | Can we reuse Suwayomi's AndroidCompat? | No reuse: mihon-source writes its own Android shims and studies Suwayomi's approach only, copying no code (IN-0005 §2). The licence check is no longer needed for mihon-source. See [mihon-source](../modules/mihon-source/overview.md) |
| Q-0029 | Replace the earlier private KB's pushed history before going public? | Done by the owner: the previous repo was deleted, and this repo starts from a fresh initial commit (IN-0004 §3) |
