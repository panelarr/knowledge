# Open questions register

Everything we don't know yet. IDs are stable and never reused. When a question is answered, move its row to **Answered** and link to where the answer now lives. Don't delete rows. A big question also gets its own file `Q-NNNN-slug.md` ([template](../meta/templates/question.md)). Add one with `python3 tools/kb.py new question "…" --area <area> --pri P2`.

**Priority:** `P1` blocks current work · `P2` important, not blocking · `P3` later.

## Open

| ID | Question | Area | Pri | Raised in |
|---|---|---|---|---|
| Q-0002 | WebView engine for WebView-only Mihon sources: KCEF/JCEF in-process (Suwayomi) vs a headless Chromium sidecar over CDP? Or skip those sources at first? | mihon-source | P2 | [mihon-source](../modules/mihon-source/overview.md) |
| Q-0004 | Tracker OAuth on self-hosted instances (different redirect URI each time): per-instance client registration, PIN/copy-token flows, or a relay? | server, trackers | P2 | [trackers](../architecture/trackers.md) |
| Q-0007 | Extension isolation in mihon-source: all extensions in one JVM (classloader per extension) vs a JVM pool or per-extension processes for crash and memory isolation? | mihon-source | P3 | [mihon-source](../modules/mihon-source/overview.md) |
| Q-0008 | Web UI component kit and styling (e.g. shadcn/ui + Tailwind, Mantine, Park UI)? | web | P2 | [web](../modules/web/overview.md) |
| Q-0009 | Which other extension ecosystems might get source plugins later (Paperback, Aidoku, Kotatsu…)? | sources | P3 | [plugins](../architecture/plugins.md) |
| Q-0014 | Docker Hub only, or also mirror to ghcr.io/panelarr? | deploy | P3 | [repo standard](../architecture/repo-standard.md) |
| Q-0015 | Central docs site (a `docs` repo with Starlight/Docusaurus on GitHub Pages) vs per-repo `docs/` only? | repos | P2 | [repo standard](../architecture/repo-standard.md) |
| Q-0016 | Legal and ToS stance and wording: no bundled extensions or plugins; hosters add indexes; disclaimers; DMCA contact. | legal | P2 | [principles](../product/principles.md) |
| Q-0018 | When to support PDF and EPUB in source-local (PDF needs a rasterizer, which may require cgo)? | source-local | P3 | [source-local](../modules/source-local/overview.md) |
| Q-0019 | Rules for inferring series, volume and chapter from file and folder names when there is no ComicInfo. | source-local | P2 | [formats](../research/comic-archive-formats.md) |
| Q-0020 | RPC stack on the Go side: ConnectRPC + OpenAPI generation from protos? Is gRPC the primary wire for remote plugins, with JSON optional? *JVM side answered: Armeria ([ADR-0024](../decisions/ADR-0024-armeria-for-the-jvm-rpc-server.md)).* | contracts | P1 | [ADR-0012](../decisions/ADR-0012-protobuf-grpc-contracts.md) |
| Q-0021 | Should trackers become a plugin kind (like sources and metadata), or stay built into server? | trackers | P3 | [trackers](../architecture/trackers.md) |
| Q-0022 | Search backends: Typesense first (author's suggestion) then Meilisearch? Is embedded Bleve worth adding? Benchmark CJK title search. | search | P2 | [search](../architecture/search.md) |
| Q-0023 | Where does character data come from (AniList, ComicVine)? Is it stored in meta and indexed for search? | meta, search | P3 | [search](../architecture/search.md) |
| Q-0024 | Plugin signing: key format (minisign vs cosign/sigstore), official key management, the trust UI for third-party indexes. | plugins, security | P2 | [plugin index](../contracts/plugin-index.md) |
| Q-0025 | Should Panelarr be a Mihon "enhanced tracker" / Mihon extension target (like Komga), so the Mihon app can read from and sync with Panelarr? | product | P3 | [trackers research](../research/trackers.md) |
| Q-0027 | Should server auto-discover remote plugins in the same Compose project (mDNS/DNS-SD, self-registration with a join token, DNS probing, Docker labels)? Discovered plugins are only suggested, never auto-enabled. | plugins, deploy | P3 | [plugins](../architecture/plugins.md) |

## Answered

| ID | Question | Answer |
|---|---|---|
| Q-0005 | Default ports? | server **8900**, meta **8901**, mihon-source **8902** (IN-0015 §1). Plugins in standalone mode: from 8903 up (suggestion). See [deployment](../architecture/deployment.md) |
| Q-0006 | Is meta embedded in server or a separate service by default? | A **standalone service** (its own container) with library integration (IN-0015 §1). See [meta](../modules/meta/overview.md) |
| Q-0013 | Are the GitHub org and Docker Hub org `panelarr` secured? | Yes, both: the GitHub repos exist, and the owner confirmed Docker Hub (IN-0015 §1) |
| Q-0031 | Does source-mihon parse extension stores itself or delegate to mihon-source? | **Delegate**: the store logic lives once, in mihon-source; source-mihon declares the config and passes it on through mihon-source's store API (IN-0015 §1). See [source-mihon](../modules/source-mihon/overview.md) |
| Q-0010 | Code-session git autonomy? | **Before the first releases**, coding sessions may merge their own branches into `main` themselves (IN-0014 §2). Pushing still needs the owner's word. Revisit at the first release. See the goal briefs |
| Q-0012 | Licence per public repo? | GPL-3.0 for apps and services, Apache-2.0 for protos and SDKs (IN-0014 §2). See [ADR-0025](../decisions/ADR-0025-licences-gpl-3-0-apps-apache-2-0-sdks-and-protos.md) |
| Q-0028 | May code repos cite KB IDs and link KB docs? | Yes: IDs in docs and commits (`Refs:` footers), and links to KB docs (IN-0014 §2). Aliases still apply. See [repo standard](../architecture/repo-standard.md) |
| Q-0001 | Go data layer? | First ent + Atlas (IN-0009 §2), then, once Postgres became the only database, **sqlc + pgx + goose** (IN-0009 §5). See [ADR-0023](../decisions/ADR-0023-sqlc-pgx-goose-data-layer.md) |
| Q-0011 | Is MySQL/MariaDB support worth its cost? | No: PostgreSQL is the only database (IN-0009 §5). See [ADR-0022](../decisions/ADR-0022-postgresql-only.md) |
| Q-0032 | How are migrations applied at runtime? | goose: plain SQL migrations embedded in the binary, applied at startup (IN-0009 §5). See [ADR-0023](../decisions/ADR-0023-sqlc-pgx-goose-data-layer.md) |
| Q-0017 | Plugin repo layout: one repo per plugin or a monorepo per kind? | One repo per plugin, e.g. `meta-mangabaka`; protos and the SDK live in the host module's repo (`meta`) (IN-0009 §2). See [modules](../modules/README.md) |
| Q-0026 | Is source-mihon a pass-through plugin plus store manager, or only a store/trust library? | source-mihon is the Panelarr-side plugin. Like every plugin, it tells the main app **what config it expects** (extension repos/stores and other settings) and **which common services it can use**; the main app manages that config. Store parsing location: Q-0031 (IN-0007 §1). See [plugins](../architecture/plugins.md#common-plugin-surface-all-kinds) |
| Q-0030 | How does mihon-source pick up config from the Panelarr side, and which wins over the local admin? | In the Panelarr stack, config comes from the main app through source-mihon. The mihon-source admin is for people who run mihon-source **standalone**, without the Panelarr stack (IN-0007 §1). See [mihon-source](../modules/mihon-source/overview.md) |
| Q-0003 | Can we reuse Suwayomi's AndroidCompat? | No reuse: mihon-source writes its own Android shims and studies Suwayomi's approach only, copying no code (IN-0005 §2). The licence check is no longer needed for mihon-source. See [mihon-source](../modules/mihon-source/overview.md) |
| Q-0029 | Replace the earlier private KB's pushed history before going public? | Done by the owner: the previous repo was deleted, and this repo starts from a fresh initial commit (IN-0004 §3) |
