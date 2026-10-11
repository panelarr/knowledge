---
title: "FEAT-0005: Unified chapters and update checks"
status: proposed
tags: [feature, server, web, m2]
related: [decisions/ADR-0028-library-entry-per-work.md, architecture/domain-model.md]
inputs: [IN-0037]
milestone: "M2"
priority: P1
updated: 2026-10-11
---

# FEAT-0005: Unified chapters and update checks

## Problem

"item page would show tabs of all sources chapters and try to make on unified chapters, where gaps would be filled up from other sources if missing or better quality or health" (IN-0037 §2).

## Outcome

A Work's page shows a **Unified** chapter list (one row per chapter, the chosen source and variant visible) and a **tab per source** with that source's raw list. New chapters from any source show up after an update check.

## Scope

- **In:**
  - group source chapters into canonical chapters by number (and volume);
  - choose a preferred variant per chapter: present at all (gap filling), user source priority, source health, scanlator preference, quality signals ([Q-0039](../../questions/README.md));
  - per-source tabs;
  - manual override per chapter;
  - scheduled and manual update checks per Work (jobs);
  - new-chapter badges per user.
- **Out:** chapter-level merging of partial pages across sources (no), automatic downloads (FEAT-0007 rules).

## Acceptance criteria

- [ ] AC1: Chapters from all attached sources group into canonical chapters by normalized number (and volume where given); decimals (12.5), extras and oddly numbered chapters are kept, not lost.
- [ ] AC2: Each canonical chapter shows its chosen variant and why ("only source", "priority", "healthier source", …); gaps in one source are filled from another.
- [ ] AC3: A per-source tab lists that source's chapters exactly as the source reports them.
- [ ] AC4: Users with permission can pin a variant for a chapter or set the source priority for the Work.
- [ ] AC5: Update checks run per Work on a schedule (configurable, jittered, within source limits) and on demand; new chapters raise per-user "new" badges and SSE events.
- [ ] AC6: A source that fails (health FAILING) is skipped for variant choice while healthy alternatives exist, and the Work page shows the source's status.

## Design notes

[domain model](../../architecture/domain-model.md): SourceChapter, Chapter, preferred variant.

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| server, web | — | — | — |

## Open questions

- [Q-0039](../../questions/README.md): what "better quality" means.
