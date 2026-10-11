---
title: "ADR-0020: Public KB, sensitive terms only as aliases"
status: accepted
tags: [privacy, kb, legal]
related: [decisions/ADR-0007-private-kb-public-code.md, decisions/ADR-0009-plugins-not-bundled.md, meta/conventions.md, meta/glossary.md]
inputs: [IN-0004]
updated: 2026-10-11
---

# ADR-0020: Public KB, sensitive terms only as aliases

- **Date:** 2026-10-11
- **Deciders:** @aurimasniekis
- **Supersedes:** [ADR-0007](ADR-0007-private-kb-public-code.md)

## Context

"Add all bit more sensetivie topics (copyright and etc) into aliases like `[EXTREPO]` but keep mihon but dont mention where u can get extension. We will make it public too not like now private only" (IN-0004 §1). The owner also asked that no other project of theirs is mentioned anywhere (IN-0004 §2).

## Decision

- **This KB is public** on GitHub (`panelarr/knowledge`), like the code repos.
- **Sensitive terms appear only as aliases.** That means copyright-adjacent names (extension collections, sites) and anything else the owner flags. The real terms live in the git-ignored `.kb-aliases.env`, shared by hand. `kb.py check`, the pre-commit hook, `ops post` and `leak-check` block them ([conventions](../meta/conventions.md#confidential-terms-aliases)).
- **Mihon may be named.** It is the app and API Panelarr is compatible with.
- **The KB never says where extensions or content can be obtained.** That means no store URLs, no repo links, no site lists. This matches [ADR-0009](ADR-0009-plugins-not-bundled.md): hosters add stores themselves.
- **Verbatim inputs are redacted** the same way: aliases in `[brackets]`, removed links noted, and `[redacted]` for things that must not appear at all.
- **No other projects of the owner are referenced** in the KB.

## Consequences

- ADR-0007's reason (a private KB) is gone. Whether public code repos may now cite KB IDs or link the KB is open ([Q-0028](../questions/README.md)). Until it is answered, code repos keep standing on their own and cite no KB IDs.
- Git history of the earlier private KB still holds real terms. It must not be published as-is ([Q-0029](../questions/README.md)).
- Research about extension ecosystems stays technical (formats, APIs, runtime needs) and avoids naming sources or sites.

## Alternatives considered

| Option | Why not |
|---|---|
| Keep the KB private | The owner wants it public |
| Public KB with real names | Draws copyright attention to the project and points readers to infringing content |
