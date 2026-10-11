---
title: "Playbook: keeper"
status: accepted
tags: [playbook, keeper]
related: [meta/conventions.md, meta/session-protocol.md, meta/commit-convention.md]
updated: 2026-10-11
---

# Playbook: keeper

**Use when:** the owner shares ideas, answers questions, makes decisions, pastes material, or asks what the KB says. This is the default role.

## The loop (every discussion)

1. **Capture.** The owner's substantial words go **verbatim** into `inputs/IN-NNNN-slug.md` (`kb.py new input "…"`). Follow-up messages in the same discussion are appended as new `§` sections of the current input, until it is committed.
2. **Place.** Put each idea where its question is answered ([conventions](../meta/conventions.md#areas)). Check whether an existing doc covers it first. Extend before you create.
3. **Restructure when needed.** A doc over ~300 lines or mixing topics gets split. A topic with no home gets a sub-folder. A new top-level area needs an ADR.
4. **Status.** New ideas are `seed`/`draft`. Tentative wording ("maybe", "what if") is never `accepted`. Changing accepted content needs the owner's explicit word plus an ADR or a `!` commit.
5. **Questions.** Every unknown becomes a `Q-NNNN` row (`kb.py new question`). Answered questions move to the Answered table with a link.
6. **Decisions.** Settled choices become ADRs (`kb.py new adr`) plus their index row. The owner's explicit decision makes them `accepted`.
7. **Indexes.** Area README rows (with status), glossary terms, `inputs/README.md` (distilled into), root README if areas changed.
8. **Journal.** `kb.py new journal "topic"`: discussed, changed, decided, new questions, next.
9. **Check.** `python3 tools/kb.py check` must pass.
10. **Commit** per [authority](../meta/authority.md) `kb_commit`, using the [commit convention](../meta/commit-convention.md). Never push unless `kb_push` allows it.

## Answering questions

- Answer from the KB and **cite paths**. Quote the status ("draft, so not binding yet").
- If the KB doesn't know: say so, open a question, and offer a clearly labelled **suggestion**.
- Never invent decisions, numbers or names and present them as settled.

## Confidential terms

When the owner uses a name that should stay private (a client, partner, codename, person), ask whether to alias it. On yes, add `ALIAS=real term` to `.kb-aliases.env`, use the alias in the input and every doc, and add the alias to the glossary. Inputs are verbatim, **except** for aliased terms, which are replaced with the alias in `[brackets]`, e.g. "we're pitching to [CLIENT_A]".

## Keeping the owner's voice

- Keep the owner's terms and intent. Don't sand ideas down into generic language.
- Don't quietly make an optional thing mandatory, or the other way round.
- When you disagree, say so once, with reasons, in the doc's open questions. The owner decides.

## Housekeeping (when asked, or every few sessions)

- Find stale `draft`/`proposed` docs and list them for the owner.
- Look for duplicated content across docs. Merge it (`refine`).
- Check the question register for questions answered elsewhere.
- Re-read accepted ADRs against recent REPORTs for drift.
