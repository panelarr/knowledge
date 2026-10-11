---
title: "ADR-0028: One library entry per work, sources matched to it, unified chapters"
status: accepted
tags: [library, server, sources, meta, chapters]
related: [architecture/domain-model.md, modules/server/overview.md, modules/meta/overview.md, contracts/source-plugin.md, decisions/ADR-0003-shared-store-per-user-libraries.md]
inputs: [IN-0037]
updated: 2026-10-11
---

# ADR-0028: One library entry per work, sources matched to it, unified chapters

- **Date:** 2026-10-11
- **Deciders:** @aurimasniekis

## Context

Mihon, Suwayomi and similar apps keep **one library entry per source series**: the same manga from three sources is three entries. The owner wants the opposite (IN-0037 §2):

> "the idea u search by name and it uses meta to find actual item, then it should search based on configured sources, like all apps do entry per source not per actual item, so my goal is to have an entry per actual meta library item and try to match all source items by names like item name can be different in every source so if it doesnt find by main name it can try look it up by alternative names, so item page would show tabs of all sources chapters and try to make on unified chapters, where gaps would be filled up from other sources if missing or better quality or health"

## Decision

- **One library entry (Work) per actual work**, anchored on **meta's Entry** (the meta-first add flow). Searching by name goes to meta to find the actual item.
- **Sources are matched to the Work** by searching the configured sources with the **main title**, then **alternative titles** (all languages and romanizations from meta's entry), since every source names it differently. Each match is a SourceSeries attached to the Work.
- **The item page shows a tab per source** with that source's own chapter list.
- **A unified chapter list** is built across sources. Each canonical chapter picks a variant, and **gaps are filled from other sources** when a chapter is missing. A variant can also win on **better quality or source health**.
- Adding directly from a source while browsing still lands on the same model: the source series is matched to a meta entry, and the Work is that entry.

## Consequences

- The domain model's Work / SourceSeries / Chapter (variants) / MetaLink fit this. The **Work is created from a meta Entry** rather than from the first source series.
- **Matching becomes core:** source search by title and alternatives, scoring against meta's entry (titles, people, year, type), and user confirmation. It shares logic with meta's duplicate candidates (GOAL-0004).
- **Open:**
  - meta is optional by principle, so how does a Work exist without meta or without a match ([Q-0038](../questions/README.md))?
  - What counts as "quality" and how health is weighed ([Q-0039](../questions/README.md)).
  - Match confidence and the confirm/fix UX ([Q-0040](../questions/README.md)).
- Downloads use the chosen variant per chapter ([ADR-0003](ADR-0003-shared-store-per-user-libraries.md): one shared copy).
