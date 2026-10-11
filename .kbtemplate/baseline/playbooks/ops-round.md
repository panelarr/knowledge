---
title: "Playbook: ops round (scheduled loop)"
status: accepted
tags: [playbook, ops, schedule]
related: [ops/README.md, meta/authority.md, playbooks/agent-manager.md, playbooks/support.md, playbooks/reviewer.md]
updated: 2026-10-11
---

# Playbook: ops round

**Use when:** the operator says "do a round", "check issues and PRs", "what's new?", or a schedule fires.

One round is a complete pass over everything that may need attention. It ends with a short summary for the operator. It must be **safe to run unattended**: with default [authority](../meta/authority.md) it only reads, writes KB files and drafts. Nothing is posted.

## Steps

1. **Pull in:**
   - `python3 tools/kb.py ops digest` (all registered repos; new items are flagged 🆕).
   - Read `agents/inbox/` and any native session messages.
   - `python3 tools/kb.py ops sessions` (worktree table).
2. **Sessions first** (they're blocked when waiting): answer `ASK`s, record `REPORT`s, handle `PROPOSE`/`CONFLICT`/`DONE` per the [agent manager](agent-manager.md).
3. **PRs/MRs:** for each 🆕 non-draft PR in the digest's to-do list, review it ([reviewer](reviewer.md)) → outbox draft. Failing checks: look at why, then draft a helpful comment.
4. **Issues:** triage each 🆕 issue ([support](support.md)) → label/reply drafts. Bugs go to QA. Ideas become inputs/seeds.
5. **QA:** verify any `DONE:` or testable `REPORT:` ([QA](qa.md)).
6. **KB upkeep:** journal entry for the round, update the board, the question register and known issues. Run `kb.py check`. Commit per `kb_commit`.
7. **Report** to the operator in chat, in at most ~10 lines:
   - **Needs you:** decisions (Q IDs), outbox drafts to approve (`kb.py ops outbox`), conflicts.
   - **Done this round:** reviews drafted, issues triaged, reports recorded.
   - **Watch:** risks, stale sessions, failing CI.

   For a longer period, the [project manager](project-manager.md) writes a status report.

## Scheduling it

Pick what your setup supports. The prompt is always the same: *"Run an ops round per playbooks/ops-round.md."*

| How | Example |
|---|---|
| Claude Code, in session | `/loop 30m Run an ops round per playbooks/ops-round.md` |
| Claude Code, cloud schedule | `/schedule` → weekdays 09:00 → same prompt |
| Headless + cron/launchd | `0 9 * * 1-5 cd /path/to/kb && claude -p "Run an ops round per playbooks/ops-round.md" >> ops/cron.log 2>&1` |
| Codex CLI headless | `codex exec "Run an ops round per playbooks/ops-round.md"` from cron |
| CI (optional) | the scheduled jobs in [ci/agent](../ci/agent/README.md) (GitHub Actions, GitLab CI, Forgejo Actions) |

Unattended runs inherit the authority settings. Keep `comment`/`review`/`label` at `draft` unless you really want the agent to post on its own.
