# Agent instructions

This repo is part of **<project>**. Its design, decisions and plans live in the project knowledge base at `<path to KB>`, which is curated by the keeper session `<keeper session>`.

## Before you work

1. If you were given a goal (`GOAL-NNNN`), read `<path to KB>/agents/goals/GOAL-NNNN-*.md` and every doc it lists. It is your brief and Definition of Done.
2. Read the KB docs for this repo: `<module/architecture doc paths>`.
3. **Accepted docs and ADRs are requirements.** If the code can't satisfy one, send `CONFLICT:` to the keeper. Never diverge silently.

## Talking to the keeper

Prefix messages with `ASK:`, `REPORT:`, `PROPOSE:`, `CONFLICT:` or `DONE:`. Send them by session message if your tool supports it, or as a file in `<path to KB>/agents/inbox/` (the only place you may write in the KB). Never edit KB docs yourself.

- Undecided point? `ASK:` first. Still open → `PROPOSE:` a working assumption, build it cheap to change (config/data), and never present it as decided.
- After each slice: checks pass → `REPORT:` with what you built, what you assumed and how to test it.

## Confidential terms

Some names are confidential and have aliases, defined in `<path to KB>/.kb-aliases.env` (local, git-ignored). Read it, and write **only the alias** in code, comments, docs, commits, branches and PR text.

## Working here

- Everything runs through `make` (`make help`). Before reporting, run `make check` and `make test`.
- Branch per slice: `<type>/<scope>-<slug>`. Conventional Commits.
- Commit / merge / push rights: `<from the goal brief>`. If unsure: commit on your branch only, never push.
- Keep a progress file (`PROGRESS.md`) with your checklist. Re-read it whenever you lose context.
