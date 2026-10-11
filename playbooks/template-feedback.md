---
title: "Playbook: template feedback"
status: accepted
tags: [playbook, template, upstream]
related: [playbooks/template-sync.md, meta/authority.md]
updated: 2026-10-11
---

# Playbook: template feedback

**Use when:** you find a bug or gap in a template-managed part (`tools/kb.py`, hooks, a check that misfires, a playbook step that doesn't work, a confusing convention, a missing forge feature), and it is **generic**: every KB made from the template would hit it. Or the operator says "report this to the template".

## 1. Is it upstream's problem?

- **Yes:** a crash or wrong result in `kb.py`; a playbook that contradicts the tool; a template field everyone needs; docs that mislead.
- **No:** things this KB changed on purpose, project-specific conventions, taste. Those stay local.
- Check the latest upstream first: `python3 tools/kb.py template plan` (maybe it's already fixed), and search existing issues:
  `gh issue list -R <template slug> --search "<keywords>" --state all` (slug in `kb.config.json` → `template.slug`).

## 2. Strip everything private

Upstream is public. Before writing anything, remove:
- project names, people, paths, repo names, URLs of private repos;
- KB content: decisions, inputs, questions, the domain;
- tokens, hostnames, logs that reveal any of the above.

Reproduce with a **minimal, made-up example** instead (`kb.py init --preset minimal --yes` in a scratch folder is a clean test bed).

## 3. Issue (default)

Draft it to the outbox. The template repo isn't in `repos[]`, so pass its slug directly:

```sh
python3 tools/kb.py ops draft open_issue <template slug> --title "kb.py check: <short summary>" --labels bug
```

Body: what you did, what happened, what you expected, template version (`.kbtemplate/VERSION`), Python version, OS, and the minimal reproduction. Suggest a fix if you have one. The disclosure line is added when posted. Post only after the operator approves (`open_issue` authority).

## 4. Pull request (when the fix is clear and small)

Only with the operator's explicit OK for this PR. It publishes code under their account.

1. Work in a **fresh clone of upstream**, never in this KB:
   `gh repo fork <template slug> --clone --remote` into the scratch folder (or `git clone` if the operator has write access).
2. Branch `fix/<slug>`, make the minimal change, and add a test in `tools/tests/` if it's tool code. Run `python3 -m unittest discover -s tools/tests` and `python3 tools/kb.py check`.
3. Commit with Conventional Commits (`fix(check): …`). Update `.kbtemplate/CHANGELOG.md` under "Unreleased".
4. Show the operator the diff and the PR text. On yes:
   `gh pr create -R <template slug> --title "fix(check): …" --body-file <file>`. The body starts with the disclosure line: `> ⚠️ **AI agent:** written by an AI agent, posted from <owner>'s account.`
5. Record it in the journal, with a link to the PR. When it's merged upstream, the next [template sync](template-sync.md) brings it back as a normal update.
