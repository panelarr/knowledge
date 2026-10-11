---
title: "Playbook: project manager"
status: accepted
tags: [playbook, planning]
related: [planning/roadmap.md, planning/status/README.md, agents/sessions.md]
updated: 2026-10-11
---

# Playbook: project manager

**Use when:** the owner asks "where are we?", a milestone needs planning or closing, a status report is due, risks or dependencies need tracking, a release is coming.

## Milestones

- Each milestone in the [roadmap](../planning/roadmap.md) has a **goal**, an **exit criterion** and its **features**. Keep it short. A milestone that can't be described in one line is two milestones.
- When a milestone becomes active: check every feature in it is `accepted` with acceptance criteria. Ask the agent manager for goals covering them.
- When a milestone closes: QA has verified the exit criterion. The release notes are drafted. The roadmap state becomes `done`.

## Status report

Sources: the latest digest (`ops/digests/`), the [sessions board](../agents/sessions.md), goal docs, the question register, the outbox.

1. `kb.py new doc "YYYY-MM-DD" --area planning/status --template status-report.md`.
2. **Headline first**: on track / at risk / off track, and why, in one sentence.
3. Done, in progress (per goal/session), **blocked or needing the owner** (decisions, approvals waiting in the outbox, conflicts), risks, next.
4. Keep it scannable: tables and short bullets, links instead of repetition.
5. Give the owner the headline and the "needs you" list in chat as well.

## Risks and dependencies

- Write each risk down with likelihood, impact and a mitigation or owner. Put them in the status report or roadmap.
- Cross-repo dependencies: record which goal waits on which, and tell the agent manager so sessions are sequenced.

## Release planning

- Collect merged PRs since the last release (digest, forge history) and map them to features.
- Hand the list to the [docs writer](docs-writer.md) for release notes. QA runs the [regression list](../qa/regression.md).
- Tagging, publishing and pushing are the owner's call unless [authority](../meta/authority.md) says otherwise.

## Outputs

Roadmap updates (proposed), status reports, risk notes, release checklists. Commit type `plan`.
