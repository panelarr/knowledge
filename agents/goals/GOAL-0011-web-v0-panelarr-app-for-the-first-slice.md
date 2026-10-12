---
title: "GOAL-0011: web v0: Panelarr app for the first slice"
status: accepted
tags: [goal, agents]
related: []
repos: [web]
session: "panelarr-web"
features: [FEAT-0003, FEAT-0004, FEAT-0005, FEAT-0006, FEAT-0007]
updated: 2026-10-12
---

# GOAL-0011: web v0: Panelarr app for the first slice

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0011 in the knowledge base at `<path>`; read it first and follow it."* Change this file to change the goal.

## Status

`accepted`, **Done 2026-10-12** (verified, pass; [test report](../../qa/reports/goal-0011-web-v0-done-verification.md)). Planned 2026-10-11: `panelarr-web` planned this goal from the accepted features and sent it as a PROPOSE (slices 0–10: scaffold, setup and login, users and plugins admin, catalogue, jobs and events, library and matching, work page, reader, downloads and storage, themes, PWA). The keeper reviewed it and gave the go; the plan lives in the session's message and its `PROGRESS.md`.

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

- [x] Slices 0–10 of the accepted plan, ticked in `PROGRESS.md`
- [x] Tests pass; `make check` passes (263 unit/component, 29 Playwright)
- [x] Docs updated in the code repo (README, docs/api.md, docs/architecture.md, docs/embedding.md)
- [x] `DONE:` sent with evidence (commits, how to verify)

## History
- 2026-10-11: plan PROPOSEd by `panelarr-web` and accepted by the keeper; its open items answered as working assumptions.
- 2026-10-12: real-server check in the compose stack passed; smoke-test findings fixed (`8154eb1`).
- 2026-10-12: DONE received (`8154eb1`) and verified on a clean clone (`make check`, `make e2e`). Goal closed.
