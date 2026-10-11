# Ops

The agent's working area for forges (GitHub, GitLab, Gitea/Forgejo, Bitbucket) and local worktrees. Everything here is written by `python3 tools/kb.py ops …` or by the agent following the [ops round](../playbooks/ops-round.md).

| Folder | What it holds |
|---|---|
| [digests/](digests/README.md) | Snapshots of open issues and PRs/MRs across registered repos, with an agent to-do list |
| [outbox/](outbox/README.md) | Drafted comments, reviews, labels and issues waiting for the operator's approval |

`ops/.state.json` remembers when each repo was last digested. It is git-ignored.

## Commands

| Command | Does |
|---|---|
| `ops repos` | Lists registered repos and whether their forge CLI is installed and logged in |
| `ops digest [--since last\|24h\|7d] [--repo R]` | Writes a digest to `digests/` |
| `ops pr <repo> <n> [--diff]` | Prints a review bundle: description, files, checks, thread, relevant KB docs |
| `ops issue <repo> <n>` | Prints a triage bundle |
| `ops draft <action> <repo> [n]` | Creates an outbox draft (`comment`, `review`, `label`, `assign`, `open_issue`, `close`, `merge`) |
| `ops outbox` | Lists drafts and their states |
| `ops approve <file>` | Marks a draft approved. **Only on the operator's word** |
| `ops post <file> [--dry-run]` | Posts an approved draft and records the URL |
| `ops sessions` | Refreshes the worktree table in [agents/sessions.md](../agents/sessions.md) |

**Forge access is CLI-first:** `gh` for GitHub, `glab` for GitLab, `tea` for Gitea/Forgejo. If a CLI is missing, `ops` tells you how to install and log in. A raw HTTPS + token fallback exists, but only as an explicit opt-in (`"transport": "http"` under `forges.<name>` in `kb.config.json`). Bitbucket has no official CLI, so it always needs that opt-in. Whether drafts can be posted at all is set in [authority](../meta/authority.md).
