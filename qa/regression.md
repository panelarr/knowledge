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
| R1 | *e.g. a fresh install starts and serves the home page* | | *manual / test path* | |

## Added 2026-10-11

- mihon-source scheduler: `next_run_at` never missing while a schedule is on; metrics counted before a run shows finished · `JobRunnerTest` "schedules run jobs, skip while running, and count in metrics" · mihon-source `323691d` · Races in JobRunner; flaked about 40% before the fix (QA, GOAL-0009)
- meta tags: a tag named like a genre (e.g. "Settings > Fantasy") stays a tag · `TestTagWithAGenresNameStaysATag` (meta), `TestTagsWithGenreNamesStayTags` (meta-mangabaka) · meta `1b08ac9` · Wrong genres after the owner's real import
- meta-mangabaka dump: a relative download dir works · relative-dir reader/sync/command tests · meta-mangabaka `5dec196` · Owner's real-dump run failed
- mihon-source admin: exactly one selected tab per tab list · `jobs.test.tsx` / tab test · mihon-source `4a67c16` · Owner's screenshots
