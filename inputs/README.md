# Inputs

The owner's raw words: messages, answers, idea dumps, transcripts, pasted conversations. They are kept **verbatim and immutable**. Distilled knowledge cites them as `IN-NNNN §section`. Corrections become a new input. Add one with `python3 tools/kb.py new input "…"` ([template](../meta/templates/input.md)).

| ID | Input | Received | Distilled into |
|---|---|---|---|
| [IN-0001](IN-0001-setup.md) | Setup interview: project, roles, agents, authority, forge, privacy | 2026-10-11 | kb.config.json, ADR-0001, README.md |
| [IN-0002](IN-0002-kickoff.md) | Kickoff: Panelarr idea, modules, Suwayomi's multi-user pain, references (redacted) | 2026-10-11 | product/, architecture/, research/, ADR-0002/0005/0006 |
| [IN-0003](IN-0003-architecture-round-1.md) | Round 1 answers: DBs, shared store, Kotlin, split repos, public code, source-api layering, local files, plugins, optional search, gRPC, mDNS, GoReleaser (redacted) | 2026-10-11 | ADR-0001…0019, architecture/, modules/, contracts/ |
| [IN-0004](IN-0004-template-migration-public-kb.md) | Move to the KB template, migrate everything, aliases for sensitive terms, make the KB public, never mention other projects | 2026-10-11 | ADR-0001, ADR-0020, Q-0028, Q-0029, meta/glossary.md |
| [IN-0005](IN-0005-start-mihon-source-with-a-coding-session.md) | Start mihon-source with a coding session: local protos, own Android shims, commit-no-push, owner creates the GitHub repo | 2026-10-11 | GOAL-0001, Q-0003, agents/sessions.md, kb.config.json |
