# IN-0009: Metadata protocol with ingestion types; meta Seerr-style; mangabaka dump first

- **Received:** 2026-10-11
- **From:** @aurimasniekis
- **Distilled into:** ADR-0018 (accepted, then superseded), ADR-0022 (supersedes ADR-0004; annotates ADR-0011), ADR-0023 (supersedes ADR-0018), Q-0001, Q-0011, Q-0017 and Q-0032 answered, AGENTS.md, product/principles.md, architecture/, contracts/metadata-plugin.md, modules/meta/overview.md, modules/meta-mangabaka/, product/scope.md, planning/roadmap.md, GOAL-0002, kb.config.json (repos)

---

## §1 Idea

on another side maybe we can define the metadata providers DTO/protocol/interfaces like multiple different types of "ingestion" like API/Scrape/Dump downloads and etc and then we can start working on first source of `mangabaka` download sqlite files to read dumps and update our metadata db?

## §2 Answers to the keeper's questions

1. *Repo layout for metadata (Q-0017). Where do the protocol, the meta service and the mangabaka provider live?* Options: meta + one repo per plugin (recommended); meta + plugins monorepo; everything in meta for now.
   → **"meta + one repo per plugin (Recommended)"**: `meta` holds the metadata.v1 protos, Go SDK and the meta service; `meta-mangabaka` is its own repo.
2. *How far should the first metadata goal go?* Options: end to end into the meta DB (recommended); protocol + mangabaka plugin only.
   → Wrote: "end to end the meta is "service" which provides metadata information / search and etc to the library and etc, later on integration with search and etc. Assume its like `Seerr` style part of the app it provides browsing/search and etc"
3. *meta needs a Go data layer for its DB (Q-0001; ADR-0018 proposes ent + Atlas).* Options: accept ent + Atlas (recommended); session spikes and proposes; not needed yet.
   → **"Accept ent + Atlas (Recommended)"**

## §3 Follow-up

also maybe migrations too like goose or etc?

## §4 Follow-up

or maybe lets just do postgres solo and thats all

## §5 Answers to the keeper's questions

1. *"Just do Postgres solo": what scope?* Options: keep ADR-0004 and build Postgres first; meta only Postgres-only; whole app Postgres-only; Postgres + SQLite, drop MySQL.
   → **"Whole app: Postgres-only"**: replace ADR-0004; every service needs Postgres; SQLite/MySQL dropped.
2. *With Postgres only, which Go data layer?* Options: sqlc + pgx + goose (recommended); keep ent + Atlas; ent + goose.
   → **"sqlc + pgx + goose (Recommended)"**
