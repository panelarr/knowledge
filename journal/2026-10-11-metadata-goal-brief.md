# 2026-10-11: metadata goal brief

- **Participants:** @aurimasniekis, panelarr-knowledge
- **Inputs:** IN-0009, IN-0010, IN-0011, IN-0012, IN-0013, IN-0014, IN-0015, IN-0016, IN-0017, IN-0018, IN-0019

## Discussed

- The owner suggested ("maybe") defining the metadata provider protocol with several ingestion types (API, scrape, dump downloads, …), then starting with MangaBaka's SQLite dump feeding the metadata DB (IN-0009 §1).
- Answers: one repo per plugin; scope end to end, with meta as the Seerr-style service for metadata, browsing and search; ent + Atlas (IN-0009 §2). Then goose for migrations ("maybe", §3), then "just do postgres solo" (§4). Asked about scope, the owner chose Postgres-only for the whole app, and with it sqlc + pgx + goose (§5).
- Meanwhile `panelarr-mihon-source` REPORTed slice 1 done (recorded in GOAL-0001; see the mihon-source journal entry).
- The owner shared their schema ideas for meta's items and asked for a more generic version that other providers can fill too (IN-0010).

## Changed in the KB

- Decisions: [ADR-0022](../decisions/ADR-0022-postgresql-only.md) Postgres only (supersedes ADR-0004, annotates ADR-0011). [ADR-0023](../decisions/ADR-0023-sqlc-pgx-goose-data-layer.md) sqlc + pgx + goose (supersedes ADR-0018, which was accepted and then superseded the same day).
- Questions: Q-0001, Q-0011, Q-0017 and Q-0032 answered.
- [Metadata contract](../contracts/metadata-plugin.md): ingestion types (`lookup`, `scrape`, `dump`, `delta`), the `Sync` event stream, Seerr-style `Browse` and `MetaAdmin`.
- [meta overview](../modules/meta/overview.md) rewritten; new module [meta-mangabaka](../modules/meta-mangabaka/overview.md); modules index, scope (Seerr-style discovery), roadmap (meta pulled forward).
- Postgres-only reflected in AGENTS.md, principles, architecture overview, deployment, storage layout, search, ADR-0017 (proposed), server and deploy modules.
- [GOAL-0002](../agents/goals/GOAL-0002-meta-v0-metadata-protocol-meta-service-and-mangabaka-dump-in.md) (`proposed`) for `panelarr-meta`; repos `meta` and `meta-mangabaka` registered; board updated.
- [Entry schema](../contracts/metadata-schema.md) (`proposed`): ProviderEntry as received + merged Entry with per-field provider priority and manual locks; one credits list, genres as tags, image variants, raw values next to enums, the owner's enum lists. Contract, meta overview and GOAL-0002 now use it; meta's catalogue item is an **Entry**, separate from server's Work.
- GOAL-0002 slice 1 REPORTed and recorded; board `working`.
- GOAL-0002 slice 2 REPORTed and recorded; the contracts got "as built" sections; ConnectRPC PROPOSE recorded on Q-0020.
- GOAL-0002 slice 3 REPORTed: DB layer merged; working assumptions (merge on write, linking rule, name-only sharing) recorded in the schema doc.

## Decided

- Owner (IN-0009 §2): one repo per metadata plugin; meta end to end as the Seerr-style metadata, browse and search service.
- Owner (IN-0009 §5): PostgreSQL is the only database for the whole app; the Go data layer is sqlc + pgx + goose.
- Owner (IN-0012): in compose, meta and the library share one Postgres server, each with its own database. Recorded in deployment, deploy, meta and GOAL-0002; sent to `panelarr-meta`. Clarified right after: that's the production setup, dev doesn't matter (IN-0013).
- Owner (IN-0014), asked for open questions: Armeria accepted ([ADR-0024](../decisions/ADR-0024-armeria-for-the-jvm-rpc-server.md)); GPL-3.0 apps + Apache-2.0 protos/SDKs ([ADR-0025](../decisions/ADR-0025-licences-gpl-3-0-apps-apache-2-0-sdks-and-protos.md)); before the first release, sessions merge their own branches (no push); repos may cite KB IDs and link KB docs. Q-0010, Q-0012, Q-0028 answered; Q-0020 narrowed to the Go side. Repo standard and both briefs updated; both sessions told.
- Owner (IN-0015): `GPL-3.0-or-later`; contact team@panelarr.app; Docker Hub org secured; ports 8900/8901/8902; source-mihon delegates stores; meta standalone with library integration. Q-0005, Q-0006, Q-0013, Q-0031 answered; both sessions told.
- Owner (IN-0016): plugin ports from 8903 up confirmed.
- Owner (IN-0017): meta gets optional, configurable search engine integrations (Typesense, Meilisearch; maybe OpenSearch/Algolia). The keeper first wrote this as applying to server too; the owner corrected it (IN-0018): these are meta's, and the library uses built-in Postgres search. Recorded in meta, search, ADR-0017 and GOAL-0002.
- Owner (IN-0019): after hearing the case against, accepted ConnectRPC with the gRPC wire rule ([ADR-0026](../decisions/ADR-0026-connectrpc-on-go-grpc-as-the-plugin-wire.md)); Q-0020 closed.

## New open questions

- None new at first. The ingestion-type list is a draft for the session to refine.
- Q-0033: OpenSearch/Algolia vs ADR-0010.

## Next

- The owner created both repos and gave the go (IN-0011): GOAL-0002 `accepted`, board `briefed`.
- Owner: start `panelarr-meta` with the paste-in prompt. Keeper: handle its messages; board to `working` on the first REPORT.
