---
title: "Test report: GOAL-0009 source-api and source-mihon DONE verification"
status: draft
tags: [qa, report, source-api, source-mihon, mihon-source]
related: [agents/goals/GOAL-0009-source-api-and-source-mihon-v0.md]
updated: 2026-10-11
---

# Test report: GOAL-0009 source-api and source-mihon DONE verification

- **Build under test:** source-api@d33d1bf, source-mihon@ada9503, mihon-source@a3906c0 (local `main`s, not pushed)
- **Plan:** the [GOAL-0009 Definition of Done](../../agents/goals/GOAL-0009-source-api-and-source-mihon-v0.md#definition-of-done)
- **Tester:** panelarr-knowledge
- **Verdict:** **pass with issues**: the goal's own work passes; a flaky test from GOAL-0007 surfaced in mihon-source.

## Results

| Case | Result | Notes / evidence |
|---|---|---|
| `make check`, clean clone of source-api | pass | Exit 0; lint 0 issues; no vulnerabilities; 6 packages `ok` |
| `make check`, clean clone of source-mihon (beside source-api) | pass | Exit 0; lint 0 issues; no vulnerabilities; 3 packages `ok` |
| `make check`, clean clone of mihon-source | **fail (flaky)** | 159 JUnit, 1 failure: `JobRunnerTest` "schedules run jobs, skip while running, and count in metrics" (line 217, a null result). Isolated reruns: 2 of 5 failed. Vitest 81 passed |
| End-to-end conformance (real mihon-source + test extension) | pass (as reported) | `make e2e`: 2 sources, every step OK, 0 problems |
| leak-check | pass | 7 repos clean |

## Bugs found

- **Flaky scheduler test in mihon-source** (from GOAL-0007): timing-dependent; fails about 40% of runs. Sent to `panelarr-mihon-source` to fix.

## Risks and untested areas

- None of the three repos' CI has run (nothing pushed); source-mihon's CI needs sibling checkouts, and releases need Docker Hub secrets.
