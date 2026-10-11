# IN-0005: Start mihon-source with a coding session

- **Received:** 2026-10-11
- **From:** @aurimasniekis
- **Distilled into:** agents/goals/GOAL-0001-mihon-source-v0-run-mihon-extensions-over-the-source-api.md, agents/sessions.md, modules/mihon-source/overview.md, questions/README.md (Q-0003 answered; Q-0010 and Q-0012 notes), kb.config.json (repo registered)

---

## §1 Request

I want to start working on mihon extension service with another agent

## §2 Answers to the keeper's questions

The keeper asked four questions (choices shown in brackets were the options offered; the owner picked one each).

1. *mihon-source must serve the `panelarr.source.v1` protos, but source-api (M0) hasn't been started. How should the first goal handle that?*
   → **"Local protos, move later (Recommended)"**: the session writes source.v1 + mihon.v1 protos from contracts/source-plugin.md inside mihon-source and builds against them; they move to source-api once it exists.
2. *Android shims: reuse Suwayomi's AndroidCompat (licence unverified, Q-0003; repo licence open, Q-0012)?*
   → **"Own shims, Suwayomi as reference (Recommended)"**: write our own shims and study Suwayomi's approach without copying code.
3. *Git autonomy for this coding session (Q-0010 open)?*
   → **"Commit on branches, no push (Recommended)"**: commits on its own feature branches; the owner pushes and merges.
4. *The repo doesn't exist yet. How should it be created?*
   → **"I create it on GitHub now"**: the keeper gives the `gh` commands to create `panelarr/mihon-source` and clone it; the session starts in that clone.
