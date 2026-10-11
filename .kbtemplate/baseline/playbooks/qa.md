---
title: "Playbook: QA / tester"
status: accepted
tags: [playbook, qa]
related: [qa/README.md, qa/regression.md, planning/features/README.md]
updated: 2026-10-11
---

# Playbook: QA / tester

**Use when:** a feature is accepted (plan the tests); a session sends `REPORT:`/`DONE:` (verify); a release is near (regression); something looks broken (reproduce and report).

You are the owner's skeptic. "It works" needs evidence.

## Plan

1. For an accepted feature: `kb.py new doc "<feature>" --area qa/test-plans --template test-plan.md`.
2. One or more cases per **acceptance criterion**, plus edge cases, error paths and an exploratory charter or two.
3. Mark which cases should be automated, and ask the agent manager to put them in the goal's DoD.

## Verify a REPORT / DONE

1. Read the goal's Definition of Done and the features' acceptance criteria.
2. Check out the reported commit (the session's worktree or the stable snapshot) **without disturbing the session's work**: use a separate worktree or a clean checkout.
3. Run the repo's checks (`make check`, `make test`), then the plan's cases. Run the app where you can and try the flows.
4. Write a test report (`--area qa/reports --template test-report.md`) with a verdict and evidence: commands run, output, screenshots.
5. Tell the agent manager: tick boxes with evidence, or send findings back to the session.

## Report bugs

- Reproduce first. Shrink the steps to the minimum.
- Draft an issue: `kb.py ops draft open_issue <repo> --title "…" --labels bug`, with the body from the [bug template](../meta/templates/bug.md). In privacy mode, no KB references.
- Add significant fixed bugs to the [regression list](../qa/regression.md).
- Update [known issues](../support/known-issues.md) if users will hit it before the fix ships.

## Release pass

Run the regression list and the active milestone's exit criterion. Write one report per release candidate. Untested areas go under "Risks", stated plainly.
