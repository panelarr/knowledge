# Code repo kit

Drop-in files that connect a code repo to this KB. Installed by the agent manager with the owner's OK ([onboarding playbook](../../playbooks/onboarding-a-code-repo.md)). Replace the `<…>` fields when copying.

| File | Copy to | Notes |
|---|---|---|
| [AGENTS.private-kb.md](AGENTS.private-kb.md) | `AGENTS.md` (or append) | When the code repo is **private**, or the KB is public. Names the KB and the protocol |
| [AGENTS.public-repo.md](AGENTS.public-repo.md) | `AGENTS.md` (or append) | **Privacy mode.** Never names the KB. Points to a local path the agent learns from its goal brief |
| [pull_request_template.md](pull_request_template.md) | `.github/pull_request_template.md` · `.gitlab/merge_request_templates/Default.md` · `.forgejo/pull_request_template.md` | Neutral; no KB IDs |
| [CONTRIBUTING.snippet.md](CONTRIBUTING.snippet.md) | merge into `CONTRIBUTING.md` | Commit convention, branches, `make` targets, AI disclosure |
| [Makefile.help](Makefile.help) | top of `Makefile` | Self-documenting `make help` + the standard target names briefs refer to |

For Claude Code, add a one-line `CLAUDE.md` containing `@AGENTS.md` to the code repo as well.
