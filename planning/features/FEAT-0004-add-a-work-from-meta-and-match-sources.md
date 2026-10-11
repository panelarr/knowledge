---
title: "FEAT-0004: Add a work from meta and match sources"
status: accepted
tags: [feature, server, web, m2]
related: [decisions/ADR-0028-library-entry-per-work.md, modules/meta/overview.md, contracts/source-plugin.md]
inputs: [IN-0009, IN-0037, IN-0042]
milestone: "M2"
priority: P1
updated: 2026-10-11
---

# FEAT-0004: Add a work from meta and match sources

## Problem

"search by name and it uses meta to find actual item, then it should search based on configured sources … match all source items by names … if it doesnt find by main name it can try look it up by alternative names" (IN-0037 §2; [ADR-0028](../../decisions/ADR-0028-library-entry-per-work.md)).

## Outcome

A user searches a title, sees meta's catalogue results (Seerr-style), opens one and adds it. Panelarr finds that work on the configured sources, using every known title, and attaches the matches. The user sees which sources matched and can fix them.

## Scope

- **In:**
  - search and browse meta's catalogue from Panelarr (through the server);
  - "Add to library" creates or reuses the shared Work for that meta Entry and the user's LibraryEntry;
  - background source matching: search each allowed source with the main title, then alternative titles (all languages and romanizations); score candidates against the entry (titles, people, year, type); auto-attach strong matches; queue weaker ones for confirmation;
  - "Fix match": attach, detach, choose between candidates, paste a source URL (`ResolveUrl`);
  - adding from a source while browsing (matched back to a meta entry).
- **Out:** automatic re-matching on schedule (later), cross-user curation queue (later).

## Acceptance criteria

- [ ] AC1: Searching in Panelarr returns meta entries (titles in the user's language, cover, type, year, status) filtered by the user's content-rating ceiling.
- [ ] AC2: Adding an entry creates one Work per meta Entry (shared by all users) and a LibraryEntry for the user; adding it again, or by another user, reuses the same Work.
- [ ] AC3: Matching searches every source the user's library can use, tries the main title then alternatives until it finds candidates, and records per source: attached, candidates or no match. It respects each source's rate limits and runs as a job (FEAT-0002 model).
- [ ] AC4: Strong matches attach automatically ([Q-0040](../../questions/README.md) sets the threshold); others appear as candidates to confirm, with the evidence (matched title, people, year, chapter count).
- [ ] AC5: "Fix match" lets a user (with permission) attach a candidate, detach a source, re-run matching, or paste a source URL that resolves to a series.
- [ ] AC6: Adding from a source's browse page finds the corresponding meta entry (by external IDs or title matching) and lands on the same Work; if none is found, the user picks the entry from meta search.

## Design notes

- Matching logic overlaps meta's duplicate candidates (GOAL-0004); share the scoring approach.
- Source search quality matters, and mihon-source's cache keeps repeated searches cheap.
- Mihon sources return **one title per series** (no alternative titles in the extension model, [research](../../research/mihon-extensions.md)): the alternatives always come from meta. Native plugins may fill `Series.alt_titles` when they have them.

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| server | [GOAL-0010](../../agents/goals/GOAL-0010-server-v0-accounts-add-and-match-chapters-reader-api-downloa.md) slice 5 | — | server side done (`a4b98e9`) |
| web | [GOAL-0011](../../agents/goals/GOAL-0011-web-v0-panelarr-app-for-the-first-slice.md) | — | pending |

## Open questions

- [Q-0040](../../questions/README.md): auto-attach threshold and confirm UX.
