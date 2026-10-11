# 2026-10-11: Kickoff and architecture v0

- **Participants:** author, keeper
- **Inputs:** IN-0002, IN-0003

## Discussed
- The Panelarr idea: an *arr*-style manga/comics manager and reader. Suwayomi's one-instance-per-person problem.
- Research: Suwayomi-Server internals; EXTREPO extensions and the Mihon Extension Store; MangaBaka; metadata providers; Mihon trackers.
- Repos fully split; code public, KB private.
- Source layering: source-api (Go) ← source-mihon (Go) → mihon-source (small Kotlin tool).
- Local files as a source.
- Plugins (not bundled); an optional search engine (Typesense-class); gRPC between services; mDNS plugin discovery idea; GoReleaser.

## Changed in the KB
- Bootstrapped every area: product, architecture, modules (8), contracts, research (8 docs), decisions, questions, inputs, journal and meta, plus `tools/kb_check.py`, `tools/leak_check.sh` and the git hooks.

## Decided
- **Accepted (author):** ADR-0001 to ADR-0011. These cover the KB, split repos, shared store with per-user libraries, multi-DB, layered sources, the stack, the private KB, the GitHub standard and images, plugins not bundled, optional search, and composable deployment.
- **Proposed (keeper, awaiting the author):**

| ADR | Topic | Origin |
|---|---|---|
| ADR-0012 | Protobuf + gRPC between services; mihon-source speaks source-api | Author's "maybe" |
| ADR-0013 | Out-of-process plugins | Keeper |
| ADR-0014 | Plugin index and signing | Keeper |
| ADR-0015 | CBZ + ComicInfo | Keeper |
| ADR-0016 | Network profiles | Keeper |
| ADR-0017 | Search interface, DB full-text default, Typesense first | Keeper |
| ADR-0018 | ent + Atlas | Keeper |
| ADR-0019 | release-please + GoReleaser | Author's "maybe" |

## New open questions
Q-0001 to Q-0027. **P1:**
- Q-0001: ORM
- Q-0003: AndroidCompat licence
- Q-0010: code-session git autonomy
- Q-0012: licences
- Q-0013: GitHub org
- Q-0020: RPC stack
- Q-0026: source-mihon vs mihon-source role split

## Next
- The author reviews the proposed ADRs and answers the P1 questions.
- M0: create the `source-api` repo (protos + SDK + conformance), and a repo template with workflows.
