---
title: "Test report: FEAT-0014 history, FEAT-0015 updates and the mobile fixes verification"
status: draft
tags: [qa, report, web, server]
related: [planning/features/FEAT-0014-reading-history.md, planning/features/FEAT-0015-updates-feed.md, planning/features/FEAT-0012-reader-series-page-and-library-polish.md]
updated: 2026-10-18
---

# Test report: history, updates and the mobile fixes

- **Build under test:** web@fd0b653 (local `main`, not pushed), server `7743817` (updates feed) and `65872f1` (history) on the live stack
- **Plan:** FEAT-0014, FEAT-0015, and the owner's mobile reports IN-0068..IN-0078
- **Tester:** panelarr-knowledge
- **Verdict:** **pass**

## Results

| Case | Result | Notes / evidence |
|---|---|---|
| web `make setup && make check`, clean clone | pass | 386 unit tests |
| web `make e2e`, clean clone | pass | 63 passed, 4 opt-in WebKit skipped |
| Reader on real Mobile Safari (iOS Simulator, real touches) | pass (as reported) | Flicker loop gone (`c052bd1`), no seams (32 → 0), flings up glide (about 500 px → 6,300 px) (`3f7b93f`, regression fixed in `6bedb02`), errors at once (`4ce796b`) |
| Installed Home Screen app | pass (as reported) | Full-height layout on iPhone 16 Pro and 16e (`4654cc3`) |
| Live stack (redeploys #23–#30) | pass (as reported) | History and Updates APIs 200 for the owner; no warnings |
| leak-check | pass | 7 repos clean |

## Risks and untested areas

- The owner's own use on the iPhone is the real acceptance (the top band in the installed app couldn't be reproduced; the header that held it is gone).
- The Updates feed only shows chapters found after a work was added; it starts nearly empty and fills with tonight's checks.
