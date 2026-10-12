---
title: "Test report: GOAL-0017 web Network admin and plugin settings DONE verification"
status: draft
tags: [qa, report, web]
related: [agents/goals/GOAL-0017-web-network-admin-and-plugin-settings-pages.md, planning/features/FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md]
updated: 2026-10-12
---

# Test report: GOAL-0017 DONE verification

- **Build under test:** web@dd2e2a5 (local `main`, not pushed)
- **Plan:** FEAT-0010 (web side) via the session's accepted plan (N1–N4); per-source settings pulled forward (IN-0062)
- **Tester:** panelarr-knowledge
- **Verdict:** **pass with issues** (tests flaky under heavy machine load)

## Results

| Case | Result | Notes / evidence |
|---|---|---|
| `make setup && make check`, clean clone, run 1 | fail | 5 of 314 unit tests failed, 4 by the 5 s test timeout; machine load average about 380 at the time (several sessions and a Docker build) |
| `make check`, run 2 | pass | 314 passed |
| `make e2e`, run 1 | fail | 2 failed (extensions specs), 46 passed |
| `make e2e`, run 2 | fail | 2 failed (axe specs, different ones), 47 passed; load average about 460 |
| Live on the stack (redeploy #13) | pass (as reported) | Network tab with "Only for …", links, docs; no non-GET requests |
| leak-check | pass | 7 repos clean |

## Risks and untested areas

- Different tests fail on each loaded run, all timeouts: the suite depends on timing. Sent to `panelarr-web` to harden (longer or condition-based waits, traces on retry) before the next goal closes.
