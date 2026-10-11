## Working conventions

- **Tasks:** everything runs through `make`. `make help` lists the targets (`setup`, `build`, `test`, `check`, `run`).
- **Branches:** `<type>/<scope>-<slug>`, e.g. `feat/sync-conflicts`.
- **Commits and PR titles:** [Conventional Commits](https://www.conventionalcommits.org/): `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `build`, `ci`. Add `!` for breaking changes.
- **Reviews:** at least one approval and green checks before merge.
- **AI agents:** agents may open PRs and post reviews. Anything an agent posts from a person's account starts with a **⚠️ AI agent** line. Humans stay responsible for what they merge.
