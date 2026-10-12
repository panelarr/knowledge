---
title: "Test report: GOAL-0012 source plugins extension packages and languages DONE verification"
status: draft
tags: [qa, report, source-api, source-mihon, mihon-source]
related: [agents/goals/GOAL-0012-source-plugins-extension-packages-and-languages.md, planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md, contracts/source-plugin.md]
updated: 2026-10-12
---

# Test report: GOAL-0012 DONE verification

- **Build under test:** source-api@2dafabf (packages at `2ac5461`), mihon-source@17f1f2b, source-mihon@b5dbae0 (local `main`, not pushed; clean clones side by side)
- **Plan:** FEAT-0009 (plugin side), via the session's accepted plan (slices 1–4)
- **Tester:** panelarr-knowledge
- **Verdict:** **pass**

## Results

| Case | Result | Notes / evidence |
|---|---|---|
| source-api `make setup && make check`, clean clone | pass | Exit 0 |
| source-mihon `make setup && make check`, clean clone | pass | Exit 0 |
| mihon-source `./gradlew check`, clean clone | pass | Exit 0; 82 admin Vitest tests; service tests green |
| source-mihon `make e2e` against the real mihon-source and the exported fixture store | pass | TestEndToEnd and TestEndToEndPackages: the conformance package walk (install, install again, narrow languages, restore, uninstall), plugin languages, an update from the store's v2, uninstall |
| Contract (AC1–AC3, AC2a, AC7 plugin side) | pass (as reported) | `PLUGIN_CAPABILITY_PACKAGES`, six package RPCs, `Source.package_id`, `PackageSource.available`, STORE_* reasons, idempotent installs, cancel-safe installs in mihon-source |
| leak-check | pass | 7 repos clean |

## Risks and untested areas

- Not yet run against the server in a live stack (next compose rebuild; server GOAL-0013 is verified separately with the fake plugin).
- Real stores and extensions are the owner's to try; the tests use the fixture store and test extensions only.
