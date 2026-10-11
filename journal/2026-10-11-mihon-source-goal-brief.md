# 2026-10-11: mihon-source goal brief

- **Participants:** @aurimasniekis, panelarr-knowledge
- **Inputs:** IN-0005, IN-0006

## Discussed

- The owner wants to start the Mihon extension service (mihon-source, M1) with a coding session (IN-0005 §1).
- Then the owner asked for a minimal admin on mihon-source: interact with sources, manage clients and integrations, API keys (IN-0006 §1). Their picks: solvers, proxies/network profiles and extension stores, with config later picked up from the Panelarr side; a React SPA; one admin token (IN-0006 §2).
- Blockers found in the KB: source-api (M0) isn't started, so the `panelarr.source.v1` protos don't exist; Q-0003 (AndroidCompat reuse) and Q-0012 (licence) are open; Q-0010 (code-session git autonomy) is open; the repo doesn't exist. The keeper asked four questions (IN-0005 §2).

## Changed in the KB

- [GOAL-0001](../agents/goals/GOAL-0001-mihon-source-v0-run-mihon-extensions-over-the-source-api.md) written (`proposed`): seven slices from scaffold to Docker image, in-repo test extensions only, DoD.
- `mihon-source` registered in `kb.config.json` → `repos[]` (`../mihon-source`, `panelarr/mihon-source`, public).
- [Sessions board](../agents/sessions.md): `panelarr-mihon-source` row and ownership note.
- [mihon-source overview](../modules/mihon-source/overview.md): shims row and implementation status.
- [Questions](../questions/README.md): Q-0003 answered; Q-0010, Q-0012 and Q-0026 annotated; Q-0030 opened.
- [ADR-0021](../decisions/ADR-0021-mihon-source-standalone-admin.md) written; ADR-0005 marked superseded. GOAL-0001 widened to nine slices (auth, integrations, stores, admin SPA). Updated [contract](../contracts/mihon-source-api.md) (stores, clients, integrations services; auth), mihon-source and source-mihon overviews, source-api overview, store research, architecture overview, roadmap M1, modules index.

## Decided

- Owner (IN-0006): [ADR-0021](../decisions/ADR-0021-mihon-source-standalone-admin.md) accepted, superseding ADR-0005: mihon-source is a standalone service with a minimal React admin, scoped client API keys and one admin token, solvers, network profiles and extension stores.
- Owner (IN-0005 §2): for GOAL-0001, protos live in mihon-source until source-api exists; own Android shims with Suwayomi only as a reference (answers Q-0003); the session commits on its branches and never pushes or merges; the owner creates the GitHub repo.

## New open questions

- Q-0030: how mihon-source later picks up config from the Panelarr side, and which side wins (suggestion recorded).
- Q-0020 (JVM RPC stack) is left to a spike and a `PROPOSE:` from the session.

## Next

- Owner: create and clone `panelarr/mihon-source`, OK the brief, start the session with the paste-in prompt.
- Keeper: install the code-repo kit with the session's first slice, mark GOAL-0001 `accepted` and the board `briefed` on dispatch, run the first digest.
