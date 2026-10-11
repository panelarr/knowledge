---
title: "Playbook: onboarding a code repo"
status: accepted
tags: [playbook, agents, repos]
related: [agents/sessions.md, meta/session-protocol.md, playbooks/agent-manager.md]
updated: 2026-10-11
---

# Playbook: onboarding a code repo

**Use when:** a new code repo joins the project, or an existing repo should start working with this KB.

## Steps

1. **Register it** in `kb.config.json` → `repos[]`:
   ```json
   {"name": "api", "path": "../api", "forge": "github", "slug": "acme/api",
    "visibility": "public", "session": "acme-api", "default_branch": "main",
    "module": "architecture/api.md", "docs": ["architecture/overview.md"]}
   ```
   - `path` is relative to this KB (for worktrees and `ops sessions`). `slug` is the forge path (for digests and reviews).
   - `module`/`docs` are the KB docs a reviewer must read for this repo.
   - `visibility: public` + privacy mode → `leak-check` scans it.
2. **Check access:** `python3 tools/kb.py ops repos`. Install and log in to the forge CLI if it says so.
3. **Install the kit** (with the owner's OK; it is a change in the code repo): copy the files from [kits/code-repo](../kits/code-repo/README.md):
   - the agent instructions snippet into the repo's `AGENTS.md`. Pick the **public** variant in privacy mode, because it never names the KB;
   - the PR/MR template and contributing snippet;
   - the Makefile help skeleton, if the repo has no task runner yet.
4. **Add the session** to the [sessions board](../agents/sessions.md), and a module/architecture doc for the repo if the domain preset has one.
5. **First digest:** `python3 tools/kb.py ops digest --repo <name>`.
6. Journal entry. Commit type `struct` or `goal`.
