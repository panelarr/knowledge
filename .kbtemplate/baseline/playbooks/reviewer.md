---
title: "Playbook: reviewer"
status: accepted
tags: [playbook, review]
related: [meta/authority.md, meta/templates/review.md, playbooks/qa.md]
updated: 2026-10-11
---

# Playbook: reviewer

**Use when:** a PR/MR needs review, from a coding session or a human contributor, in a code repo or in this KB.

## Gather

```sh
python3 tools/kb.py ops pr <repo> <number> --diff
```

The bundle has the description, files, commits, checks, conversation and the **KB context**: the docs registered for that repo, accepted ADRs and goals touching it. Read the linked docs before judging.

## Check, in this order

1. **Intent:** does it do what its goal/feature/issue asks? Is there scope creep, or a missing part?
2. **Decisions:** does it respect accepted ADRs and docs? A deviation is a `CONFLICT`, not a style nit.
3. **Correctness:** logic errors, edge cases, error handling, concurrency, data loss, security (input validation, secrets, auth).
4. **Tests:** do new behaviours have tests? Are the acceptance criteria covered? Checks green?
5. **Operability:** config instead of hard-coded values, migrations, logging, backwards compatibility.
6. **Docs:** README/docs/changelog updated where users or developers would need it.
7. **Hygiene:** commit/PR title convention, focused diff, no generated junk.
8. **Confidential terms:** no real term behind an alias (`kb.py leak-check <repo path>` checks the whole repo).
9. **Privacy mode:** no KB IDs, paths or verbatim KB text in the public repo (`kb.py leak-check <repo path>`).

## Write the review

```sh
python3 tools/kb.py ops draft review <repo> <number> --event comment|approve|request_changes
```

Fill the body from the [review template](../meta/templates/review.md): **Must fix / Should consider / Nits / Verified**. Be specific (file:line), explain *why*, and suggest a fix. For contributors: be welcoming, especially first-timers, and thank them.

- `approve` only if there are no must-fix items **and** the checks pass.
- Put your reasoning for the operator in an HTML comment at the top. It is not posted.
- At `draft` authority: tell the operator the draft is ready and summarise it in two lines. Post after approval (`ops approve`, `ops post`).

## For KB PRs (team mode)

Also check: frontmatter and status are right, nothing became `accepted` without the owner, indexes are updated, inputs are cited, `kb.py check` passes, and the commit/PR title follows the [knowledge convention](../meta/commit-convention.md).
