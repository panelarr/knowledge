# Meta

How this knowledge base works.

| Doc | What it holds | Status |
|---|---|---|
| [conventions.md](conventions.md) | Areas, frontmatter, status lifecycle, IDs, style, diagrams, indexes | accepted |
| [commit-convention.md](commit-convention.md) | Knowledge commit types, `!` for accepted changes, footers | accepted |
| [session-protocol.md](session-protocol.md) | Keeper and consumers, message kinds, channels, privacy mode | accepted |
| [authority.md](authority.md) | What the agent may do on its own; the outbox flow | accepted |
| [glossary.md](glossary.md) | Terms with specific meanings | draft |

## templates/

Used by `python3 tools/kb.py new <kind> "title"`. You can also copy them by hand and replace the `{{…}}` fields.

| Knowledge | Operations |
|---|---|
| [concept](templates/concept.md) · [decision](templates/decision.md) · [question](templates/question.md) · [input](templates/input.md) · [journal](templates/journal.md) · [research](templates/research.md) · [kb-aliases.env](templates/kb-aliases.env) | [feature](templates/feature.md) · [goal](templates/goal.md) · [test-plan](templates/test-plan.md) · [test-report](templates/test-report.md) · [bug](templates/bug.md) · [review](templates/review.md) · [reply](templates/reply.md) · [status-report](templates/status-report.md) · [release-notes](templates/release-notes.md) |

## Tooling

| Command | Does |
|---|---|
| `python3 tools/kb.py check` | Frontmatter, statuses, links, indexes, IDs, duplicates, placeholders, outbox |
| `python3 tools/kb.py new adr\|question\|input\|feature\|goal\|journal\|doc "title"` | Next free ID, template, index row |
| `python3 tools/kb.py commit-msg <file>` / `--title "…"` | Commit convention (git hook and CI) |
| `python3 tools/kb.py leak-check` | Privacy mode and aliases: public repos never reference the KB or a confidential term |
| `python3 tools/kb.py aliases` | Lists the aliases defined in `.kb-aliases.env` (values hidden unless `--show`) |
| `python3 tools/kb.py ops …` | Forge digest, PR/issue context, outbox, worktree board ([ops](../ops/README.md)) |

The git hooks in `.githooks/` run `check` and `commit-msg`. Enable them once per clone: `git config core.hooksPath .githooks`.
