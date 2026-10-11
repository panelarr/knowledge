---
title: "{{ID}}: {{TITLE}}"
status: draft
tags: [goal, agents]
related: []
repos: []
session: ""
features: []
updated: {{TODAY}}
---

# {{ID}}: {{TITLE}}

The brief a coding session works from. A short paste-in version points here: *"Work on {{ID}} in the knowledge base at `<path>`; read it first and follow it."* Change this file to change the goal.

## Status

<!-- draft → proposed (owner reviews the brief) → accepted (dispatched) → done/superseded. Keep a dated history below. -->

## Context

- Code: `<repo path>` · worktree `<path>` · branch prefix `<feat/...>`
- Read first: <!-- vision/principles, the features, the ADRs and design docs this touches -->
- **Accepted decisions are law.** If code and KB disagree, the KB wins, or send `CONFLICT:`.

## Objective

<!-- What to build and why, in a few sentences. -->

## How to work

1. Build in **slices**. Each slice works end to end (logic, interface, tests, docs).
2. One branch per slice. Follow the code repo's commit convention.
3. After each slice: `make check` (or the repo's equivalent) passes → `REPORT:` to the keeper with what you built, what you assumed and how to test it.
4. Keep a progress file in the code repo (e.g. `PROGRESS.md`): this checklist ticked off, plus the next slice. **Re-read it whenever you lose context.**
5. Don't stop after each slice to ask. Go on to the next one unless blocked on the owner's decision.

## When something isn't decided

- `ASK:` the keeper first.
- Still open? `PROPOSE:` a concrete working assumption that fits the accepted decisions, then build it **cheap to change** (config/data, not hard-coded).
- Never present an assumption as decided, and never change an accepted decision yourself.

## Constraints

<!-- Authority for this session: may it commit? merge to main? push? (see meta/authority.md). Performance, security, privacy rules. -->

## Definition of Done

- [ ] 
- [ ] Tests pass; `make check` passes
- [ ] Docs updated in the code repo
- [ ] `DONE:` sent with evidence (commits, how to verify)

## History
