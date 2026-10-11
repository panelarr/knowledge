---
title: "ADR-0001: Keep project knowledge in an agent-curated Markdown KB"
status: accepted
tags: [meta, decision]
related: [meta/conventions.md, meta/session-protocol.md, meta/authority.md]
inputs: [IN-0001, IN-0003, IN-0004]
updated: 2026-10-11
---

# ADR-0001: Keep project knowledge in an agent-curated Markdown KB

- **Date:** 2026-10-11
- **Deciders:** @aurimasniekis
- **Supersedes / superseded by:** —

## Context

Panelarr: A self-hosted, arr-style app for curating, downloading, managing and reading manga, manhwa, manhua and comics, with real multi-user support and opt-in plugins for sources and metadata.

Several agent sessions and people will work on it over time. Agents forget between sessions, and decisions scattered across chats get lost or re-argued. The project needs one trustworthy, versioned place that every session can read, and an agent that keeps it current and runs the day-to-day product, delivery and quality work. The setup answers are recorded in IN-0001.

## Decision

- All product, design, technical and delivery knowledge lives in this git repo as **Markdown**, with **Mermaid** for diagrams. Areas and rules are in [conventions](../meta/conventions.md).
- Docs carry frontmatter with a **status lifecycle** (seed → draft → proposed → accepted …). **Only the owner accepts.**
- One keeper session, **`panelarr-knowledge`**, writes the KB and performs the enabled roles in [playbooks](../playbooks/README.md). Other sessions read it and message the keeper ([session protocol](../meta/session-protocol.md)).
- What the agent may do on its own is set in [authority](../meta/authority.md). Commits in this KB: **the keeper commits on its own after each discussion**. Pushes: **never by the agent**.
- `tools/kb.py check` and the git hooks keep the KB consistent.
- The KB is built from the owner's [llm-knowledge-base-template](https://github.com/aurimasniekis/llm-knowledge-base-template) (preset `platform`, all roles on; IN-0004). The first, hand-built version of this KB (same day) was migrated into it in full: inputs renumbered `IN-0002`/`IN-0003`, ADR-0002…0019 and Q-0001…0027 kept their numbers. Template updates arrive through [template sync](../playbooks/template-sync.md).
- The KB is **public** ([ADR-0020](ADR-0020-public-kb-with-aliases.md)).

## Consequences

- Ideas are traceable from the owner's words (inputs) to docs, decisions and code.
- Consumers can rely on `accepted` docs as requirements.
- There is some upkeep overhead (frontmatter, indexes). The checker and `kb.py new` keep it cheap.

## Alternatives considered

| Option | Why not |
|---|---|
| Wiki / Notion / shared docs | Hard for local agent sessions to read and write; weak history and review |
| Docs only inside each code repo | No home for cross-repo planning or private reasoning; scattered decisions |
| Chat history as memory | Lost between sessions; not reviewable; no single source of truth |
