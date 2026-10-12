---
title: "GOAL-0010: server v0: accounts, add and match, chapters, reader API, downloads"
status: accepted
tags: [goal, agents]
related: []
repos: [server]
session: "panelarr-server"
features: []
updated: 2026-10-11
---

# GOAL-0010: server v0: accounts, add and match, chapters, reader API, downloads

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0010 in the knowledge base at `<path>`; read it first and follow it."* Change this file to change the goal.

## Status

**Done 2026-10-12.** The session planned this goal itself and the keeper accepted the plan; its slices and evidence are in its REPORTs and its `PROGRESS.md`. Verified on a clean clone: see the [test report](../../qa/reports/goal-0010-server-v0-done-verification.md).

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
- 2026-10-12: DONE received (`41418a9`) and verified on a clean clone.
