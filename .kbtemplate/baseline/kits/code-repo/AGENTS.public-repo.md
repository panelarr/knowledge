# Agent instructions

<!-- Privacy mode: this file is public. It must not name or describe any private design repository. -->

## Before you work

1. Your task brief was given to you by your operator, including where to read its full context. Read the brief and the documents it lists before changing code.
2. Read this repo's own docs: `README.md`, `docs/`, `CONTRIBUTING.md`.
3. Treat the decisions referenced in your brief as requirements. If the code can't satisfy one, stop and report the conflict to your operator. Don't diverge silently.

## Rules for public artifacts

Everything in this repo is public: code, comments, docs, commit messages, branch names, PR and issue text.

- Explain the *why* in your own words. Don't paste text from private notes, and don't use internal document identifiers or paths.
- If design reasoning is worth keeping publicly, write it as a doc in `docs/` (or `docs/adr/`) of this repo.

## Confidential terms

Your operator gives you a list of aliases for confidential names (a local file, never committed). Write **only the alias** in code, comments, docs, commits, branches and PR text. If unsure whether a name is confidential, ask.

## Working here

- Everything runs through `make` (`make help`). Before reporting, run `make check` and `make test`.
- Branch per slice: `<type>/<scope>-<slug>`. Conventional Commits.
- Commit / merge / push rights come from your brief. If unsure: commit on your branch only, never push.
- After each slice, report to your operator: what you built, what you assumed, how to test it.
- Text you post on the forge from a human's account starts with: `> ⚠️ **AI agent:** written by an AI agent, posted from <owner>'s account.`
