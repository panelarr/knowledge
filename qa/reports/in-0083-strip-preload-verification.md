---
title: "Test report: IN-0083 long-strip preload verification"
status: draft
tags: [qa, report, web, reader]
related: [planning/features/FEAT-0012-reader-series-page-and-library-polish.md, modules/web/overview.md]
updated: 2026-10-22
---

# Test report: the long strip loads "Pages to load ahead"

- **Build under test:** web@4bcf68a (local `main`, not pushed), live as redeploy #38
- **Plan:** the owner's report IN-0083; the strip-stability specs; the new WebKit gate
- **Tester:** panelarr-knowledge
- **Verdict:** **pass**

## Results

| Case | Result | Notes / evidence |
|---|---|---|
| `make setup && make check`, clean clone | pass | 396 unit tests (4 new in page-loader.test.ts) |
| `make e2e`, clean clone | pass | 67 passed, 4 skipped (the WebKit project, run separately below). A first run failed to connect: it reused the web session's test server on the same port while that was running; re-run with `CI=1` and separate ports |
| `make e2e-webkit`, clean clone | pass | 6 passed (reader, reader-stability, strip-preload on iOS Safari's engine) |
| Preload honours the setting, in order, ≤3 in flight | pass (as reported) | page-loader unit tests; e2e/strip-preload.spec.ts with preload 12 on desktop, phone and phone-webkit |
| Smooth scrolling on iOS | pass (as reported) | iOS Simulator, preload 16: 11 pages of chapter 1 and 7 of chapter 2 loaded before the first fling; no spinners while scrolling; frame times unchanged |
| Live stack (#38) | pass (as reported) | new shell served; server log 0 WARN/ERROR |

## Risks and untested areas

- The owner's stall (nothing in flight for up to 11 s) didn't reproduce on the mock; the new loader no longer depends on what's rendered, but the owner's reading is the real check.
- Clean-clone e2e runs on this machine must use their own ports (`E2E_PORT`, `E2E_PREVIEW_PORT`) and `CI=1`, so they don't reuse a coding session's running test server.
