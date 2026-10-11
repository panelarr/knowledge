---
title: "Playbook: support"
status: accepted
tags: [playbook, support]
related: [support/README.md, support/faq.md, support/known-issues.md, meta/authority.md]
updated: 2026-10-11
---

# Playbook: support

**Use when:** new issues appear in the digest; a user asks a question; an issue needs labels, a duplicate link or more information.

## Triage an issue

```sh
python3 tools/kb.py ops issue <repo> <number>
```

1. **Classify:** bug, feature request, question, docs, duplicate, out of scope, spam.
2. **Check what we know:** [known issues](../support/known-issues.md), the [FAQ](../support/faq.md), open questions, features and goals in flight, and other open issues (duplicates).
3. **Decide the next step:**
   - *Bug with enough info* → label it. QA reproduces. Note it in known issues if users will hit it.
   - *Bug missing info* → ask for exactly what's missing (version, steps, logs).
   - *Feature request* → thank them, then capture it in the KB as an input or `seed` and hand to the product owner. Tell the user honestly whether it fits.
   - *Question* → answer it, and add it to the FAQ if it's the second time.
   - *Duplicate* → link the original, kindly.
   - *Unknown to the KB* → open a `Q-NNNN` for the owner. Tell the user you're checking.
4. **Draft:** labels (`ops draft label <repo> <n> --labels bug,needs-info`) and a reply (`ops draft comment <repo> <n> --kind issue`), using the [reply template](../meta/templates/reply.md) and [replies](../support/replies/README.md).

## Tone

Warm, specific, brief. Thank the person. Never blame the user. Say what happens next. Don't promise dates or features the owner hasn't accepted.

## Never

- Write the real term behind an alias. Use the alias, or rephrase without it.
- Post anything private (KB reasoning, `secrets/`, other users' data), or KB IDs in privacy mode.
- Close issues on your own unless `close` authority allows it.
- Argue. Escalate to the owner instead.
