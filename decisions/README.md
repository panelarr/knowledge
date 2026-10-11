# Decisions (ADRs)

Numbered, append-only decision records. An accepted ADR is never rewritten. A newer ADR supersedes it, and both link to each other. Create one with `python3 tools/kb.py new adr "Use X for Y"` ([template](../meta/templates/decision.md)).

| ADR | Decision | Status |
|---|---|---|
| [ADR-0001](ADR-0001-knowledge-base.md) | Keep project knowledge in this agent-curated Markdown KB | accepted |
| [ADR-0002](ADR-0002-split-repositories.md) | One repository per module | accepted |
| [ADR-0003](ADR-0003-shared-store-per-user-libraries.md) | Shared content store, per-user libraries | accepted |
| [ADR-0004](ADR-0004-database-portability.md) | SQLite (default), PostgreSQL, MySQL/MariaDB | accepted |
| [ADR-0005](ADR-0005-layered-source-architecture.md) | Layered sources: source-api ← source-mihon → mihon-source (small JVM tool) | accepted |
| [ADR-0006](ADR-0006-technology-stack.md) | Go services, Kotlin/JVM for Mihon, React + TanStack SPA/PWA | accepted |
| [ADR-0007](ADR-0007-private-kb-public-code.md) | Public code repos never reference the private KB. Superseded by ADR-0020 | superseded |
| [ADR-0008](ADR-0008-public-repo-standard-and-images.md) | Full GitHub workflows, public docs, `panelarr/<repo>` images | accepted |
| [ADR-0009](ADR-0009-plugins-not-bundled.md) | Sources and metadata providers are opt-in plugins; none by default | accepted |
| [ADR-0010](ADR-0010-optional-search-engine.md) | Optional lightweight search engine chosen by the hoster | accepted |
| [ADR-0011](ADR-0011-composable-opt-in-deployment.md) | Composable, opt-in deployment; server alone works | accepted |
| [ADR-0012](ADR-0012-protobuf-grpc-contracts.md) | Protobuf contracts; gRPC between services; REST/OpenAPI for browsers and as an option | proposed |
| [ADR-0013](ADR-0013-out-of-process-plugins.md) | Plugins out of process: go-plugin managed binaries or remote endpoints | proposed |
| [ADR-0014](ADR-0014-plugin-index-and-signing.md) | Plugin indexes with checksums and signatures | proposed |
| [ADR-0015](ADR-0015-cbz-comicinfo-storage.md) | CBZ + ComicInfo.xml storage | proposed |
| [ADR-0016](ADR-0016-per-source-network-profiles.md) | Per-source network profiles | proposed |
| [ADR-0017](ADR-0017-search-interface-builtin-default.md) | Search interface; DB full-text default; Typesense adapter first | proposed |
| [ADR-0018](ADR-0018-ent-atlas-data-layer.md) | ent + Atlas as the Go data layer | proposed |
| [ADR-0019](ADR-0019-release-tooling.md) | release-please, GoReleaser, buildx, Renovate, CodeQL | proposed |
| [ADR-0020](ADR-0020-public-kb-with-aliases.md) | The KB is public; sensitive terms only as aliases; no pointers to where extensions are obtained | accepted |
