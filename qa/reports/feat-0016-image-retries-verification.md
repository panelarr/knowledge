---
title: "Test report: FEAT-0016 image retries verification"
status: draft
tags: [qa, report, web, server]
related: [planning/features/FEAT-0016-automatic-retries-for-failed-page-images.md, agents/goals/GOAL-0023-web-image-retry-settings-in-the-extension-admin.md, qa/reports/goal-0022-server-image-retries-done-verification.md]
updated: 2026-10-18
---

# Test report: FEAT-0016 image retries

- **Build under test:** web@3f73d90 (local `main`, not pushed), against server `6ff0878` (verified in [the GOAL-0022 report](goal-0022-server-image-retries-done-verification.md))
- **Plan:** GOAL-0023's Definition of Done and FEAT-0016 AC2 (the admin side)
- **Tester:** panelarr-knowledge
- **Verdict:** **pass**

## Results

| Case | Result | Notes / evidence |
|---|---|---|
| web `make setup && make check`, clean clone | pass | 392 unit tests (5 new in image-retries.test.tsx) |
| web `make e2e`, clean clone | pass | 65 passed, 4 opt-in WebKit skipped; image-retries.spec.ts on desktop and phone |
| AC2 extension value for all its sources, a source override, reset | pass | the e2e journey (set the extension, a source inherits it, off on the source, reset both) and unit tests; server side in the GOAL-0022 report |
| Inherit, Off and own waits read differently | pass | unit tests; the "In effect: … (set here / from its extension / the default)" line |
| Layout and axe | pass | layout.spec.ts with the editor open (phone, desktop); axe on the open editor |
| leak-check | pass (as reported) | |

## Risks and untested areas

- The UI was tested against the mock only; the server API answered live with the default (redeploy #33). The owner's real check is reading on SITE_A.
- A console error "<li> cannot be a descendant of <li>" shows in e2e runs (older than this slice); fixed in web `2271320` (an attached series rendered as an `<li>` inside its source row's `<li>`, on a work's Sources tab); unit tests now fail on invalid nesting.
