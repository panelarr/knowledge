# 2026-10-11: mihon-source goal brief

- **Participants:** @aurimasniekis, panelarr-knowledge
- **Inputs:** IN-0005, IN-0006, IN-0007, IN-0008

## Discussed

- The owner wants to start the Mihon extension service (mihon-source, M1) with a coding session (IN-0005 §1).
- Then the owner asked for a minimal admin on mihon-source: interact with sources, manage clients and integrations, API keys (IN-0006 §1). Their picks: solvers, proxies/network profiles and extension stores, with config later picked up from the Panelarr side; a React SPA; one admin token (IN-0006 §2).
- Blockers found in the KB: source-api (M0) isn't started, so the `panelarr.source.v1` protos don't exist; Q-0003 (AndroidCompat reuse) and Q-0012 (licence) are open; Q-0010 (code-session git autonomy) is open; the repo doesn't exist. The keeper asked four questions (IN-0005 §2).

- The owner answered Q-0026 and Q-0030 together (IN-0007 §1), created the repo and gave the go (IN-0007 §2).
- The session started and reported in directly through session messages. The owner suggested ("maybe") a frontend sub-agent working in parallel (IN-0008).

## Changed in the KB

- [GOAL-0001](../agents/goals/GOAL-0001-mihon-source-v0-run-mihon-extensions-over-the-source-api.md) written (`proposed`): seven slices from scaffold to Docker image, in-repo test extensions only, DoD.
- `mihon-source` registered in `kb.config.json` → `repos[]` (`../mihon-source`, `panelarr/mihon-source`, public).
- [Sessions board](../agents/sessions.md): `panelarr-mihon-source` row and ownership note.
- [mihon-source overview](../modules/mihon-source/overview.md): shims row and implementation status.
- [Questions](../questions/README.md): Q-0003 answered; Q-0010, Q-0012 and Q-0026 annotated; Q-0030 opened.
- [ADR-0021](../decisions/ADR-0021-mihon-source-standalone-admin.md) written; ADR-0005 marked superseded. GOAL-0001 widened to nine slices (auth, integrations, stores, admin SPA). Updated [contract](../contracts/mihon-source-api.md) (stores, clients, integrations services; auth), mihon-source and source-mihon overviews, source-api overview, store research, architecture overview, roadmap M1, modules index.
- Q-0026 and Q-0030 answered; Q-0031 opened. [Plugins](../architecture/plugins.md) common surface: plugins declare the config they expect and the common services they can use. Contracts, both Mihon module docs and GOAL-0001 updated. GOAL-0001 `accepted` and dispatched; board `briefed`.
- GOAL-0001: optional "Parallel frontend" section (after slice 2, sub-agent owns `admin/` in its own worktree, API is the contract). Board: `working`; ownership note.
- GOAL-0001: slices 1 and 2 REPORTed and recorded; Armeria PROPOSE recorded as a working assumption on Q-0020; contracts note what was built.
- GOAL-0001 catch-up REPORT: slices 3–8 merged (`a49f0ba`); a second sub-agent was used for the shims, beyond the brief; a hand test against a real store worked.

## Decided

- Owner (IN-0006): [ADR-0021](../decisions/ADR-0021-mihon-source-standalone-admin.md) accepted, superseding ADR-0005: mihon-source is a standalone service with a minimal React admin, scoped client API keys and one admin token, solvers, network profiles and extension stores.
- Owner (IN-0005 §2): for GOAL-0001, protos live in mihon-source until source-api exists; own Android shims with Suwayomi only as a reference (answers Q-0003); the session commits on its branches and never pushes or merges; the owner creates the GitHub repo.
- Owner (IN-0007 §1): the main app gets each plugin's config (incl. source-mihon: repos/stores, settings) and the common services it can use; the mihon-source admin is for standalone users only. Answers Q-0026 and Q-0030.

## New open questions

- Q-0030: how mihon-source later picks up config from the Panelarr side, and which side wins (suggestion recorded).
- Q-0031: does source-mihon parse stores itself or delegate to mihon-source (suggestion: delegate).
- Q-0020 (JVM RPC stack) is left to a spike and a `PROPOSE:` from the session.

## Next

- Owner: start `panelarr-mihon-source` with the paste-in prompt.
- Keeper: handle the session's ASK/REPORT/PROPOSE; board to `working` on the first REPORT; first digest once the repo has commits.
