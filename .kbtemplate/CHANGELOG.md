# Template changelog

Changes to the template itself, newest first. When you sync a knowledge base made from this template, read the entries after the version in your `.kbtemplate/VERSION` ([template-sync playbook](../playbooks/template-sync.md)). Each entry says what changed and whether existing KBs should act.

## 0.1.0 (2026-10-11)

First public version.

- Core: conventions, status lifecycle, ADRs, question register, verbatim inputs, journal, commit convention, `kb.py check`/`new`/`commit-msg`.
- Operations layer: planning, agents (goals, sessions board, inbox), QA, support, ops (digests, outbox) with role playbooks.
- Authority model with draft-first outbox and automatic AI-agent disclosure on everything posted.
- Forge adapters (GitHub, GitLab, Gitea/Forgejo, Bitbucket), CLI-first.
- Presets: software, platform, game, research, minimal. Examples for the first four.
- Team mode for GitHub, GitLab, Forgejo/Gitea and Bitbucket; optional scheduled CI agent rounds.
- Template sync (`kb.py template`) and upstream feedback playbooks.
- Aliases for confidential terms (`.kb-aliases.env`, git-ignored), enforced by check, ops post and leak-check.
