---
name: kb-template-sync
description: Sync this knowledge base with newer versions of its upstream template: plan, explain each change, apply only what the operator approves (3-way merge for locally changed files).
---

Read `playbooks/template-sync.md` in the knowledge base root and follow it exactly. Also obey `AGENTS.md`: the owner alone accepts, cite KB paths, respect `meta/authority.md`, and run `python3 tools/kb.py check` before committing.
