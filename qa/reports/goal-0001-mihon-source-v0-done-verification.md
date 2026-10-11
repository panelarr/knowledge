---
title: "Test report: GOAL-0001 mihon-source v0 DONE verification"
status: draft
tags: [qa, report, mihon-source]
related: [agents/goals/GOAL-0001-mihon-source-v0-run-mihon-extensions-over-the-source-api.md, modules/mihon-source/overview.md]
updated: 2026-10-11
---

# Test report: GOAL-0001 mihon-source v0 DONE verification

- **Build under test:** mihon-source@3977e41 (local `main`, not pushed)
- **Plan:** the [GOAL-0001 Definition of Done](../../agents/goals/GOAL-0001-mihon-source-v0-run-mihon-extensions-over-the-source-api.md#definition-of-done) (no feature test plan yet)
- **Tester:** panelarr-knowledge, plus the owner's hand test
- **Verdict:** **pass with issues**. Automated checks pass on a clean clone. The owner's real use found a solver usability gap, and a fix is requested before the goal closes.

## Results

| Case | Result | Notes / evidence |
|---|---|---|
| `make check` on a clean clone of `main` @ `3977e41` (outside the session's worktree) | pass | `BUILD SUCCESSFUL in 1m 17s`; JUnit 100 tests, 0 failures, 0 errors, 0 skipped; Vitest 7 files, 67 tests passed. Some Gradle tasks came from the local build cache |
| No extension binaries or real store data in the repo | pass | `git ls-tree` on `main`: only `gradle/wrapper/gradle-wrapper.jar` matches `*.jar/*.apk/*.dex` |
| leak-check (aliases, KB references) | pass | `kb.py leak-check`: 3 repos clean |
| DoD evidence per box | pass (as reported) | The session's DONE gives a test class or commit for each box (auth, install paths, shims, source API, networking, stores, SPA, Docker). The keeper did not re-run the Docker image or the quick start |
| Owner hand test against a real store and extension (earlier, run by the session) | pass | Store add, install, browse, search, details, chapters, pages and a WebP image worked. The one bug found (query-parameter casing) was fixed |
| Owner hand test: FlareSolverr on a Cloudflare-protected source | **fail (usability)** | Solver configured, still 403, solver never called. Cause: a solver is used only through a network profile; the owner's config had a solver but no profiles and no default. The UI doesn't explain this. Also, detection requires a 403/503 with `Server: cloudflare` |

## Bugs found

- **Solver unused without a profile, and nothing says so.** Follow-up requested from `panelarr-mihon-source`: default-profile flow or a warning, docs.
- **Narrow challenge detection** (`Server` header only). Follow-up requested: `cf-mitigated: challenge`, challenge-page markers, logging when a 403/503 isn't treated as a challenge, tests.

## Risks and untested areas

- `docker.yml` (multi-arch build and push) has never run, because nothing is pushed. It needs the Docker Hub secrets.
- The keeper did not build or run the 485 MB image; the session reports it ran the quick start against the container.
- WebView-only sources are unsupported (Q-0002).
