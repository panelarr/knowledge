---
title: "Test report: GOAL-0007 mihon-source jobs DONE verification"
status: draft
tags: [qa, report, mihon-source, jobs]
related: [agents/goals/GOAL-0007-mihon-source-jobs-page.md, planning/features/FEAT-0002-jobs-page-in-every-admin.md]
updated: 2026-10-11
---

# Test report: GOAL-0007 mihon-source jobs DONE verification

- **Build under test:** mihon-source@898723f (local `main`, not pushed)
- **Plan:** [FEAT-0002](../../planning/features/FEAT-0002-jobs-page-in-every-admin.md) AC1–AC7 via the [GOAL-0007](../../agents/goals/GOAL-0007-mihon-source-jobs-page.md) DoD
- **Tester:** panelarr-knowledge
- **Verdict:** **pass**

## Results

| Case | Result | Notes / evidence |
|---|---|---|
| `make check`, clean clone of `main` @ `898723f` | pass | Exit 0; JUnit 152, 0 failures, 0 skipped; Vitest 81 passed |
| AC evidence | pass (as reported) | Tests named per AC (list, history and trimming, 409 + params, cancel, admin-only, interrupted runs, metrics) |
| Contract parity with meta | pass | Implements contracts/jobs.md incl. Changes; adds `JobParam.choices` and an ErrorInfo on 409, which meta should copy |
| leak-check | pass | 3 repos clean |

## Bugs found

None. Fixed along the way: a cancelled health check no longer records the source as failing.

## Risks and untested areas

- The scheduled self-check now runs in **rounds** each interval (two sources at a time, random order, short random pause) instead of spread across the interval, so Run now isn't always busy. Same off-by-default and rate-limit rules.
- Armeria routes `:` in IDs differently from vanguard (it doesn't 404); the ID rule is still enforced at startup.
