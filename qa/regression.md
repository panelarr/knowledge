---
title: Regression list
status: draft
tags: [qa, regression]
related: [qa/README.md]
updated: 2026-10-11
---

# Regression list

## Summary

Behaviour that broke once, or that is too important to break. Every release (and every `DONE:` verification touching these areas) re-checks it. Prefer automating each item and noting the test that covers it.

| # | Check | Area | Covered by | Added |
|---|---|---|---|---|
| R1 | mihon-source scheduler: `next_run_at` never missing while a schedule is on; metrics counted before a run shows finished | mihon-source jobs | `JobRunnerTest` "schedules run jobs…" (fixed `323691d`) | 2026-10-11 |
| R2 | A tag named like a genre (e.g. "Settings > Fantasy") stays a tag; genres follow the provider's order | meta, meta-mangabaka | `TestTagWithAGenresNameStaysATag`, `TestTagsWithGenreNamesStayTags` (fixed `1b08ac9`) | 2026-10-11 |
| R3 | The MangaBaka dump works with a relative download dir | meta-mangabaka | relative-dir reader/sync/command tests (fixed `5dec196`) | 2026-10-11 |
| R4 | Exactly one selected tab per tab list in the admins | mihon-source, meta admin | tab tests in the admin suites (fixed `4a67c16`) | 2026-10-11 |
