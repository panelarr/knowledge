# 2026-10-11: mihon-source goal brief

- **Participants:** @aurimasniekis, panelarr-knowledge
- **Inputs:** IN-0005

## Discussed

- The owner wants to start the Mihon extension service (mihon-source, M1) with a coding session (IN-0005 §1).
- Blockers found in the KB: source-api (M0) isn't started, so the `panelarr.source.v1` protos don't exist; Q-0003 (AndroidCompat reuse) and Q-0012 (licence) are open; Q-0010 (code-session git autonomy) is open; the repo doesn't exist. The keeper asked four questions (IN-0005 §2).

## Changed in the KB

- [GOAL-0001](../agents/goals/GOAL-0001-mihon-source-v0-run-mihon-extensions-over-the-source-api.md) written (`proposed`): seven slices from scaffold to Docker image, in-repo test extensions only, DoD.
- `mihon-source` registered in `kb.config.json` → `repos[]` (`../mihon-source`, `panelarr/mihon-source`, public).
- [Sessions board](../agents/sessions.md): `panelarr-mihon-source` row and ownership note.
- [mihon-source overview](../modules/mihon-source/overview.md): shims row and implementation status.
- [Questions](../questions/README.md): Q-0003 answered; Q-0010 and Q-0012 annotated.

## Decided

- Owner (IN-0005 §2): for GOAL-0001, protos live in mihon-source until source-api exists; own Android shims with Suwayomi only as a reference (answers Q-0003); the session commits on its branches and never pushes or merges; the owner creates the GitHub repo.

## New open questions

- None. Q-0020 (JVM RPC stack) is left to a spike and a `PROPOSE:` from the session.

## Next

- Owner: create and clone `panelarr/mihon-source`, OK the brief, start the session with the paste-in prompt.
- Keeper: install the code-repo kit with the session's first slice, mark GOAL-0001 `accepted` and the board `briefed` on dispatch, run the first digest.
