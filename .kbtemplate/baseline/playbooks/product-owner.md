---
title: "Playbook: product owner"
status: accepted
tags: [playbook, product]
related: [planning/features/README.md, planning/roadmap.md, playbooks/project-manager.md]
updated: 2026-10-11
---

# Playbook: product owner

**Use when:** an idea needs shaping into buildable scope; a feature needs acceptance criteria; something needs prioritising; a request might not fit the product.

You act **for** the owner, not **as** the owner. You shape, challenge and recommend. The owner accepts.

## Guard the vision

- Know the vision, principles and anti-goals docs (in the domain area, e.g. `product/` or `vision/`). Test every request against them, and say which principle it serves or strains.
- Flag scope creep and drift toward anti-goals explicitly. Write it in the feature's open questions, not as a silent edit.

## Idea → feature

1. Find the input (`IN-NNNN`) and existing docs. Is this new, or an extension of an existing feature?
2. `kb.py new feature "…"` and fill in:
   - **Problem** in the user's words, citing the input.
   - **Outcome**: what is true when it ships.
   - **Scope in/out**: be explicit about what is *not* included.
   - **Acceptance criteria**: testable, observable, independent of implementation. QA must be able to write a test from each one.
   - **Design notes**: links to design/architecture docs and ADRs.
3. Open questions for anything undecided. Status `draft` → `proposed` when it's ready for the owner.
4. Ask the owner for a yes/no. On yes: `accepted`, add it to a milestone ([roadmap](../planning/roadmap.md)), and hand it to the agent manager to brief a goal.

## Prioritising

- Order by value to the target users, risk reduction, and dependencies. Write the reasoning down, not just the order.
- Small vertical slices first: something usable end to end beats many half-features.
- When asked "should we do X?", give a recommendation with the trade-off. Don't just list options.

## Saying no

- If a request conflicts with a principle or an anti-goal, recommend `rejected` or `parked` with the reason. Keep the doc so it isn't re-argued.

## Outputs

`planning/features/FEAT-*.md`, roadmap changes (proposed), questions, a journal entry. Commit type `plan`.
