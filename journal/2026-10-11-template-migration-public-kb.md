# 2026-10-11: Template migration, public KB

- **Session:** panelarr-knowledge
- **Inputs:** IN-0004

## Discussed
- The owner made a reusable KB template and asked to rebuild this KB on it, migrate everything, alias sensitive terms, and make the KB public (IN-0004 §1). Mid-way: never mention their other projects at all (§2).

## Changed
- The old KB moved to `../knowledge.old` (its git history intact). The new KB was initialised from the template: preset `platform`, all six roles, agent `claude`, forge GitHub, `kb_commit: auto`, `kb_push: never`, KB visibility public, licence `own-open`.
- Migrated every area: product, architecture, modules (8), contracts, research, ADR-0002…0019, Q-0001…0027, both inputs, the first journal entry and the glossary terms. The roadmap moved from `product/` to `planning/roadmap.md`. The session table moved to [agents/sessions.md](../agents/sessions.md). The old `tools/kb_check.py` and `tools/leak_check.sh` are replaced by `tools/kb.py`.
- Inputs renumbered: kickoff `IN-0001` → `IN-0002`, round 1 `IN-0002` → `IN-0003`. `IN-0001` is now the setup answers. All references were rewritten.
- Aliases: `EXTREPO` for the community extension collection. the old extension research doc became [research/mihon-extensions.md](../research/mihon-extensions.md). Repo and store links and site-hinting theme names were removed. Inputs were redacted with `[ALIAS]` / `[redacted]` and say so in their header.
- References to the owner's other project were removed everywhere.
- Living docs that said "private KB" now point to ADR-0020: principles, modules index, repo standard, contracts.

## Decided
- [ADR-0020](../decisions/ADR-0020-public-kb-with-aliases.md) (accepted, owner's words): the KB is public, with aliases. It supersedes ADR-0007.

## New questions
- Q-0028: may code repos cite or link the now-public KB?
- Q-0029: replace the already-pushed private history. Answered the same day: the owner deleted the old repo, and this KB starts from a fresh initial commit (IN-0004 §3).

## Next
- Owner: the P1 questions from the kickoff.
- Register code repos (`playbooks/onboarding-a-code-repo.md`) once they exist.
