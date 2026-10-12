---
title: "FEAT-0011: Better chapter copies and configurable matching"
status: proposed
tags: [feature, server, web, chapters, matching, storage]
related: [decisions/ADR-0028-library-entry-per-work.md, planning/features/FEAT-0004-add-a-work-from-meta-and-match-sources.md, planning/features/FEAT-0005-unified-chapters-and-update-checks.md, planning/features/FEAT-0007-downloads-to-the-shared-library.md]
inputs: [IN-0059]
milestone: ""
priority: P3
updated: 2026-10-12
---

# FEAT-0011: Better chapter copies and configurable matching

## Problem

The owner's answers to Q-0039, Q-0040 and Q-0041 (IN-0059):
- "q39: user can rate down or mark as bad quality chapter so it would have logic to prioritise better ones and works case select worst."
- "q40 exact name, maybe some of fields matches or etc (maybe many options user can select)"
- "q41 yes per source maybe,"

v0 picks a chapter copy by pinned → preferred languages → healthier source → series priority → newest upload (server `a114382`), matches sources with a built-in rule, and stores downloads on named storages with a default.

## Outcome

Users can mark a chapter copy as bad quality; Panelarr then prefers other copies of that chapter, and falls back to the bad one only when nothing else exists. Matching attaches a source series automatically on an exact title match, and admins can choose which further fields must also match. Download storage can be chosen per source.

## Scope (suggested)

- **In:**
  - "bad quality" (rate down) on a chapter copy, from the reader and the chapter list; it lowers that copy in the choice for everyone (or per user: to settle), with a reason shown; the worst copy still serves when it's the only one;
  - match rules: exact title (main or alternative, any language) attaches automatically; optional extra conditions an admin can select (author, year, type, external ID, chapter count…) and a candidates list for the rest *("maybe", IN-0059: options to be settled)*;
  - storage rules: the default storage plus an optional choice per source *("maybe", IN-0059)*.
- **Out:** automatic image-quality detection (resolution, watermarks).

## Acceptance criteria (draft)

- [ ] AC1: Marking a copy bad makes the next pick use another copy of that chapter when one exists; the reason shows "rated down".
- [ ] AC2: With only bad copies, the least bad still serves.
- [ ] AC3: An exact title match attaches automatically; with extra conditions selected, a match also needs them; others land as candidates.
- [ ] AC4: An admin can send a source's downloads to a chosen storage.

## Open questions

- Is "bad quality" per user or shared by everyone on the instance?
- Which extra match conditions to offer first.
