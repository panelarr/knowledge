---
title: "Test report: GOAL-0022 server image retries DONE verification"
status: draft
tags: [qa, report, server]
related: [agents/goals/GOAL-0022-server-automatic-retries-for-failed-page-images.md, planning/features/FEAT-0016-automatic-retries-for-failed-page-images.md]
updated: 2026-10-18
---

# Test report: GOAL-0022 server image retries

- **Build under test:** server@6ff0878 (local `main`, not pushed; S1 `0913f34`, S2 `1217f9d`), clean clone with clean sibling clones of meta and source-api
- **Plan:** GOAL-0022's Definition of Done and FEAT-0016 AC1–AC5 (server side)
- **Tester:** panelarr-knowledge
- **Verdict:** **pass**

## Results

| Case | Result | Notes / evidence |
|---|---|---|
| `make setup && make check`, clean clone | pass | fmt, vet, golangci-lint 0 issues, govulncheck 0 affecting, tests with race detector (22 packages ok) |
| `make gen-check` | pass | generated API and SQL up to date |
| `make api-breaking` | pass | additive only |
| Retry tests run on their own (`-count=1 -v`) | pass | TestPageImageRetries, TestPageImagesRetried (reader page and download with the real 1 s default), TestImageRetrySettings |
| AC1 fail once, then shown | pass | TestPageImageRetries, TestPageImagesRetried |
| AC2 extension value for all its sources, source override wins, default otherwise | pass | TestImageRetrySettings, TestPageImageRetries (package [] = 1 call; source override = 3 calls; clear falls back at once) |
| AC3 not found not retried | pass | one call each for not found, rejected key, challenge, login |
| AC4 rate limit and retry-after | pass | retry_after waited out; over 30 s fails at once; the pacer runs before every attempt |
| AC5 downloads get the same retries | pass | TestPageImagesRetried |
| Live stack (redeploys #32, #33) | pass (as reported) | migration 00018 applied; two sources answer level `default`, [1000, 3000] |
| leak-check | pass | 7 repos clean |

## Risks and untested areas

- The retry path hasn't been seen on a real flaky site yet; the owner's reading on SITE_A is the real check.
- No admin UI yet (GOAL-0023, `panelarr-web`); FEAT-0016 isn't delivered until it lands.
