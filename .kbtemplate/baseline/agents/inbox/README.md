# Inbox

The **only** place where consumer sessions may write in this KB. Use it when your agent platform can't message the keeper directly ([session protocol](../../meta/session-protocol.md)).

**File name:** `YYYY-MM-DD-HHMM-<session>-<kind>.md`, e.g. `2026-10-12-1430-api-report.md`.

**Content:**

```markdown
REPORT: <one-line summary>

Session: <session name> · Repo: <repo> · Branch: <branch> · Commit: <sha>
Goal: GOAL-NNNN (if any)

<details: what was built or decided, what was assumed, how to test it>
```

Kinds: `ASK` · `REPORT` · `PROPOSE` · `CONFLICT` · `DONE`.

The keeper processes every file during its next [ops round](../../playbooks/ops-round.md): it records what matters in the right docs, replies through the same channel, and then deletes the file. The record lives in the journal and the commit. Files here are not knowledge docs and need no index rows.
