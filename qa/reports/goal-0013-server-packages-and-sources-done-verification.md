---
title: "Test report: GOAL-0013 server extensions, source languages, admin-only sources DONE verification"
status: draft
tags: [qa, report, server]
related: [agents/goals/GOAL-0013-server-extensions-source-languages-admin-only-sources.md, planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md]
updated: 2026-10-12
---

# Test report: GOAL-0013 DONE verification

- **Build under test:** server@79cbf1c (local `main`, not pushed), with source-api@2ac5461 and meta@805d263 beside it (clean clones)
- **Plan:** FEAT-0009 (server side), via the session's accepted plan (S1–S3)
- **Tester:** panelarr-knowledge
- **Verdict:** **pass**

## Results

| Case | Result | Notes / evidence |
|---|---|---|
| `make setup && make check`, clean clones | pass | Exit 0; lint 0 issues; govulncheck: no called vulnerabilities (1 in a required module, not reachable); all Go packages `ok` |
| Key tests re-run (`-count=1`) | pass | TestPackagesAPI, TestSingleSitePluginHasNoPackages, TestSourcesBrowse, TestWorkSourceSearch, TestCopiesFollowSourceAvailability, TestListSourcesFilters |
| Admin-only sources (AC6, AC8) | pass (as reported) | `4a51c86`: seven operations admin-only, both roles tested, authorization matrix; the one deliberate break documented |
| Languages and availability (AC2a, AC4) | pass (as reported) | `5afb3f2`, `1d732f6`: copies follow usable sources; language-off sources marked `unavailable_reason: language` |
| Packages API (AC1–AC3, AC7) | pass (as reported) | `1d732f6`: list, get, install, update, uninstall as `plugin.package` tasks; per-package languages; 422 for single-site plugins |
| leak-check | pass | 7 repos clean |

## Risks and untested areas

- Store-failure mappings (`store_fetch_failed`, `store_invalid`) have no test: the fake can't simulate store failures yet (follow-up).
- Package icons aren't served (needs an admin proxy route; follow-up).
- Not run against the real source-mihon: its packages capability is GOAL-0012 slice 3, still in progress.
