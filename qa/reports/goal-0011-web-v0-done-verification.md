---
title: "Test report: GOAL-0011 web v0 DONE verification"
status: draft
tags: [qa, report, web]
related: [agents/goals/GOAL-0011-web-v0-panelarr-app-for-the-first-slice.md, modules/web/overview.md, modules/deploy/overview.md]
updated: 2026-10-12
---

# Test report: GOAL-0011 web v0 DONE verification

- **Build under test:** web@8154eb1 (local `main`, not pushed; 331ae2e → 8154eb1)
- **Plan:** FEAT-0003 to FEAT-0007 (web side), via the session's accepted plan
- **Tester:** panelarr-knowledge
- **Verdict:** **pass** (the flows that need catalogue entries and sources weren't run on the real stack; see the risks)

## Results

| Case | Result | Notes / evidence |
|---|---|---|
| `make setup && make check`, clean clone | pass | Exit 0; lint, gen-check, build with the CSP check, typecheck; 32 files, 263 tests passed, none skipped |
| `make e2e`, clean clone | pass | 29 passed, 4 skipped on purpose (desktop-only cases skipped on the phone project: double page, the sidebar version, two accessibility checks) |
| Embedded serving contract on the real server (session's check) | pass (as reported) | Cache headers, CSP and security headers, SPA fallback, plain 404s; matches `docs/embedding.md` |
| Every page on the real server, signed in as owner (session's check) | pass (as reported) | 0 console errors, 0 failed requests, 0 CSP violations; real writes: preferences, an API key, an invite, a plugin-sync job over SSE, source-mihon's schema-driven settings |
| Compose smoke test findings | fixed | No `/me` probe before sign-in or setup; versions shown as "dev", not "vdev"; an empty catalogue now has its own message |
| leak-check | pass | 7 repos clean |

## Risks and untested areas

- The running compose image embeds the older build; the fixes in 8154eb1 reach the image at the next server image build.
- Add and match, chapters, the reader and downloads have not been run against the real server: the stack has no catalogue entries and no sources. They are covered by spec-validated mock tests and Playwright.
- Out of v0 by plan: backups (FEAT-0008), the meta and mihon-source admin pages inside Panelarr (IN-0039), OIDC, OPDS.
