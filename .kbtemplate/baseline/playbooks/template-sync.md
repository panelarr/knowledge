---
title: "Playbook: template sync"
status: accepted
tags: [playbook, template, meta]
related: [playbooks/template-feedback.md, meta/conventions.md]
updated: 2026-10-11
---

# Playbook: template sync

**Use when:** the operator asks "is there a newer template?", "update from the template", or a periodic check (e.g. monthly) is due.

This KB was created from an upstream template, and has since **diverged on purpose**: names were rendered in, roles were removed, conventions were tuned, playbooks were edited. So **never pull or merge upstream blindly.** Bring over what fits, explain what doesn't, and let the operator decide.

## Steps

1. **Status.** `python3 tools/kb.py template status`: upstream URL, the version this KB is based on, last sync.
2. **Plan.** `python3 tools/kb.py template plan` fetches upstream into `.kbtemplate/upstream/` (git-ignored) and writes `.kbtemplate/sync-plan.md`:
   - **safe**: upstream changed, the KB didn't;
   - **merge**: both changed;
   - **new**: new upstream files;
   - **removed**: upstream deleted them;
   - **local-only**: removed here on purpose.
3. **Read the upstream changelog** (in the plan) for every version after ours. Note anything flagged as needing action.
4. **Explain, then ask.** Give the operator a short summary in plain words, grouped: what each change does and whether it fits this KB.
   - Recommend **skip** for changes that conflict with decisions recorded here (ADRs, edited conventions), and say which decision.
   - Recommend **take** for fixes (tool bugs, broken checks) and for clear improvements.
   - New playbooks/templates for **disabled roles**: mention them, don't install them.

   Wait for the operator's choice. Approval is per file or per group.
5. **Apply what was approved:**
   - safe: `python3 tools/kb.py template apply <file>…` re-renders the new version with this KB's values.
   - merge: `python3 tools/kb.py template apply <file>` tries a 3-way merge (`git merge-file`). Clean merges still get a quick review. On conflict, open the file, use `python3 tools/kb.py template diff <file>` to see what upstream intended, and resolve with the operator. Keep the KB's deliberate local changes and add upstream's intent. Then `python3 tools/kb.py template resolve <file>`.
   - new: `python3 tools/kb.py template apply --new <file>`. Then add index rows and links (e.g. playbook README, AGENTS.md routing).
   - Declined changes: leave them. Note them in the journal so they aren't re-offered as surprises.
6. **Config changes.** If upstream added keys to `kb.config.json`, add them by hand with their documented defaults. `kb.config.json` is never overwritten.
7. **Finish.** `python3 tools/kb.py check` must pass. Then `python3 tools/kb.py template finish` adopts the upstream version and clears the fetched copy. Write a journal entry ("synced to template X: took A, B; skipped C because ADR-…"). Commit `meta(template): sync with template <version>` per `kb_commit` authority.

## No baseline?

KBs made before sync support (or copied by hand) have no `.kbtemplate/manifest.json`. Then:
1. `git clone --depth 1 <upstream> .kbtemplate/upstream`.
2. Compare the managed areas by hand: `tools/`, `.githooks/`, `meta/templates/`, `playbooks/`, `meta/*.md`, agent files and forge files. Use `git diff --no-index`.
3. Prefer taking `tools/` wholesale if not edited locally. Port playbook and convention changes by hand.

## Found a problem in the template itself?

If the sync (or anything else) shows a bug or gap that **every** KB would have, propose it upstream: [template feedback](template-feedback.md).
