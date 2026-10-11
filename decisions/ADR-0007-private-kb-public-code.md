---
title: "ADR-0007: Public code repos never reference the private KB"
status: superseded
tags: [privacy, repos, git]
related: [meta/session-protocol.md, architecture/repo-standard.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# ADR-0007: Public code, private KB

- **Date:** 2026-10-11 · **Deciders:** author
- **Superseded by:** [ADR-0020](ADR-0020-public-kb-with-aliases.md) on 2026-10-11 (the KB became public; IN-0004).

## Context
"The main code libs will be hosted on github open source … this knowledge is private for me to keep and will not be public on github, so each other repo should not be mentioning this KB anywhere" (IN-0003 §3.2).

## Decision
- Every code repo is **public on GitHub**.
- This KB is **private**.
- No public artifact (code, comments, docs, commits, branches, PRs, issues, CI) mentions the KB, its path or its identifiers (`ADR-`, `Q-`, `IN-`), and no KB text is copied verbatim.
- Traceability runs **one way**: the KB records which commits and PRs implement what.

## Consequences
- Each repo writes self-contained public docs, including fresh public design notes where useful.
- `tools/kb.py leak-check` scans the sibling repos' tracked files and commit messages.
- KB-style `KB:`/`Refs:` footers are **not** used in code commits.
