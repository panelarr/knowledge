---
title: "Test report: FEAT-0012 reader, series page and library polish verification"
status: draft
tags: [qa, report, web]
related: [planning/features/FEAT-0012-reader-series-page-and-library-polish.md]
updated: 2026-10-12
---

# Test report: FEAT-0012 verification

- **Build under test:** web@645caa3 (local `main`, not pushed), with server bookmarks (`781ed85`), image limits (`4e16d93`), chapter parser (`f28a50e`, `ae9666f`) and library stats (`ac8875e`)
- **Plan:** FEAT-0012 (accepted plan: quick fix, R1–R4) plus IN-0061 and IN-0066
- **Tester:** panelarr-knowledge
- **Verdict:** **pass**

## Results

| Case | Result | Notes / evidence |
|---|---|---|
| `make setup && make check`, clean clone | pass | 318 unit tests |
| `make e2e`, clean clone | pass | 49 passed, 4 opt-in WebKit skipped (WebKit reader specs run separately by the session) |
| Reader on the live stack | pass (as reported) | Pages p50 1.5 s after image limits; the page being read moves 0 px while pages load (throttled phone runs); one page-list fetch per chapter |
| Series page, bookmarks, reader bars, chapter titles, library on the live stack | pass (as reported) | Redeploys #8–#16 |
| leak-check | pass | 7 repos clean |

## Risks and untested areas

- The owner's own trial on a phone is the real acceptance; custom image filters are a later goal.
