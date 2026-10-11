---
title: "Playbook: docs writer"
status: accepted
tags: [playbook, docs]
related: [planning/releases/README.md, support/README.md, meta/session-protocol.md]
updated: 2026-10-11
---

# Playbook: docs writer

**Use when:** a feature ships and users need to know; a repo's README or docs are out of date; release notes are due; support keeps answering the same question.

## Principles

- **Audience first.** Users (how to install and use), operators (configure, deploy, upgrade) or contributors (build, test, conventions). Write each page for one audience.
- **The KB is the source, public docs are the product.** Distil from accepted docs, in plain language. Don't link users to the KB.
- **Privacy mode:** public docs never mention the KB, its IDs or its paths, and never copy KB text verbatim. Explain the *why* in your own words.
- **Aliases:** public docs never contain the real term behind an alias. Use the alias, or a neutral description agreed with the owner.
- Show, then explain: a working example before the reference table.
- Only document what exists. Planned behaviour is labelled as planned, or left out.

## Workflow

1. Find what changed: merged PRs (digest), completed features, the release list from the project manager.
2. For each change, decide where users would look: README, docs page, changelog, CLI help, error message.
3. Write the docs **in the code repo** on a branch. That is code-repo work, so it goes through the agent manager as a small goal, or as a PR the owner opens. Drafts can sit in an outbox file or a KB scratch note until then.
4. Release notes: `kb.py new doc "vX.Y.Z" --area planning/releases --template release-notes.md`. Write Highlights first, user-visible changes only, upgrade notes when anything breaks.
5. When support answers the same question twice, add it to the [FAQ](../support/faq.md). When the FAQ answer is stable, move it into the public docs.

## Quality bar

Accurate (tested commands), current (version noted), scannable (headings, short paragraphs, tables), and complete for the task the reader came to do.
