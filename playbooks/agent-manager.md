---
title: "Playbook: agent manager"
status: accepted
tags: [playbook, agents]
related: [agents/sessions.md, agents/goals/README.md, meta/session-protocol.md, meta/authority.md]
updated: 2026-10-11
---

# Playbook: agent manager

**Use when:** work needs to be handed to a coding session; sessions report back; several sessions run in parallel; a session's PR needs judging; the owner asks "who is doing what?".

You manage agent sessions the way a lead manages a team: clear briefs, clean boundaries, quick unblocking, honest verification.

## 1. Brief: write the goal

1. `kb.py new goal "…"`. Fill in the [template](../meta/templates/goal.md):
   - **Objective** and the **features** it delivers (`features:` frontmatter).
   - **Context to read first**: the exact docs and accepted ADRs. Don't make the session hunt.
   - **Where**: repo path, worktree, branch prefix (`repos:` and `session:` frontmatter).
   - **Constraints**: what it may commit, merge or push ([authority](../meta/authority.md) and the code repo's rules), performance, security and privacy rules.
   - **Definition of Done**: checkable boxes, including tests, docs and a `DONE:` with evidence.
2. Status `proposed`. Show the owner the brief and ask for a go-ahead (`dispatch_session` level).
3. Write a **short paste-in prompt** for the session, which points to the goal file:
   > You are `<session>`. Work on GOAL-NNNN in the knowledge base at `<kb path>`: read `agents/goals/GOAL-NNNN-….md` and the docs it lists, then follow it. Message the keeper with ASK/REPORT/PROPOSE/CONFLICT/DONE ([session protocol](../meta/session-protocol.md)).

## 2. Dispatch: worktrees and sessions

- **One worktree per parallel session.** Sessions never edit files in another session's worktree.
  ```sh
  git -C <repo> worktree add ../<repo>-<session> -b <prefix>/<slug> main
  ```
  Creating it follows `create_worktree` authority. At `draft`, give the owner the command to run.
- **Ownership:** record in the [sessions board](../agents/sessions.md) which paths each parallel session owns. A cross-cutting change gets asked for, or kept as a tiny, clearly labelled commit.
- **Stable snapshot (optional):** if the owner tests builds by hand, keep a `stable` branch/worktree that only moves to verified commits (`make stable`), so the session's ongoing work never disturbs testing.
- **Everything through `make`** (or the repo's task runner): `make help`, `setup`, `build`, `test`, `check`, `run`. Briefs refer to targets, not raw commands.
- Update the board: session, repo, worktree, branch prefix, goal, state `briefed`. Goal status `accepted` once dispatched.

## 3. Run: handle messages

Process native messages, `agents/inbox/` files and forge threads ([session protocol](../meta/session-protocol.md)):

| Message | Do |
|---|---|
| `ASK:` | Answer from the KB with paths. If unknown, open a Q and give a labelled suggestion |
| `REPORT:` | Record it (tech/module doc, goal history, board), commit with `Session:`. If testable, hand to QA |
| `PROPOSE:` | Record as draft + Q for the owner. If it unblocks work, agree it as a **working assumption** built cheap to change |
| `CONFLICT:` | Open a Q, flag it to the owner now, tell the session how to proceed meanwhile (pause that part, or assume X) |
| `DONE:` | Run the [QA](qa.md) verification against the Definition of Done before ticking anything |

Keep sessions moving. A session waiting on an answer is the most expensive state.

## 4. Review: judge the work

- For each PR/MR from a session: `kb.py ops pr <repo> <n> --diff`, then the [reviewer playbook](reviewer.md). Check the change against the goal's DoD and the accepted ADRs, not just code quality.
- Merging follows `merge` authority (default `never`: the owner merges). Recommend clearly: "ready to merge" or "needs X".

## 5. Close

- Tick DoD boxes only with evidence (QA report, commits). Goal status: `accepted` → note **Done** with date in its history. Start a follow-up goal for leftovers, and `superseded` links point to it.
- Board state `done` or `idle`. Remove worktrees when the owner agrees (`git worktree remove`).
- Tell the project manager: features completed, for status and release notes.

## Board hygiene (every ops round)

- `kb.py ops sessions` refreshes the generated worktree table: branch, ahead/behind, uncommitted changes, last commit.
- Flag: sessions with no report for a long time, worktrees far behind main, uncommitted work piling up, two sessions touching the same paths.
