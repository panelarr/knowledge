---
title: "Test report: GOAL-0004 meta duplicates DONE verification"
status: draft
tags: [qa, report, meta, duplicates]
related: [agents/goals/GOAL-0004-meta-duplicates-find-similar-entries-optional-model-review.md]
updated: 2026-10-11
---

# Test report: GOAL-0004 meta duplicates DONE verification

- **Build under test:** meta@324acd6 (local `main`, not pushed), meta-mangabaka `main` beside it
- **Plan:** the [GOAL-0004 Definition of Done](../../agents/goals/GOAL-0004-meta-duplicates-find-similar-entries-optional-model-review.md#definition-of-done)
- **Tester:** panelarr-knowledge
- **Verdict:** **pass**, with a quality risk noted below

## Results

| Case | Result | Notes / evidence |
|---|---|---|
| `make check`, clean clone of meta | pass | Exit 0; lint 0 issues; no vulnerabilities; 21 Go packages `ok`; Vitest 56 passed |
| `make check`, clean clone of meta-mangabaka | pass | Exit 0; 5 packages `ok` |
| DoD evidence | pass (as reported) | Tests named per box: find/confirm/dismiss, dismissed pairs stay dismissed, incremental runs, judge adapters on mock servers (OpenAI Decisions, TypeSafe, Clef) with back-off, caching and caps, secret storage, merge with redirects |
| `~/Projects/Panelarr/meta` back on `main` | pass | The session now uses worktrees for branches |
| leak-check | pass | 7 repos clean |

## Risks and untested areas

- **Candidate quality at full scale isn't proven.** On synthetic data: 100% precision at 30k entries, 67% recall on full runs (misses are "Special Edition"-style variants); precision at 300k was 41% before the people-mismatch penalty and wasn't re-measured. The first run on the owner's real catalogue is the real test, and its results should be reviewed before trusting many confirms.
- The decision-model adapters are tested only against mock servers (by design); a real call happens only when the owner enables one.
