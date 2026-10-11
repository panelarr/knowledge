# IN-0001: Setup interview

- **Received:** 2026-10-11
- **From:** @aurimasniekis
- **Distilled into:** kb.config.json, [ADR-0001](../decisions/ADR-0001-knowledge-base.md), README.md

---

The owner's answers to the setup questionnaire (SETUP.md), recorded as given.

```json
{
  "project": {
    "name": "Panelarr",
    "pitch": "A self-hosted, arr-style app for curating, downloading, managing and reading manga, manhwa, manhua and comics, with real multi-user support and opt-in plugins for sources and metadata.",
    "owner": "@aurimasniekis",
    "keeper_session": "panelarr-knowledge",
    "slug": "panelarr",
    "language": "en"
  },
  "preset": "platform",
  "mode": "agents",
  "roles": {
    "product_owner": true,
    "project_manager": true,
    "agent_manager": true,
    "qa": true,
    "docs_writer": true,
    "support": true
  },
  "agents": [
    "claude"
  ],
  "repos": [],
  "authority": {
    "kb_commit": "auto",
    "kb_push": "never",
    "comment": "draft",
    "review": "draft",
    "label": "draft",
    "assign": "draft",
    "open_issue": "draft",
    "close": "never",
    "merge": "never",
    "push_code": "never",
    "dispatch_session": "draft",
    "create_worktree": "draft"
  },
  "forge": "github",
  "collaboration": {
    "templates": false,
    "ci_check": true,
    "ci_agent": false,
    "codeowners": ""
  },
  "kb": {
    "visibility": "public",
    "url": "https://github.com/panelarr/knowledge"
  },
  "privacy": {
    "enabled": false,
    "extra_patterns": [],
    "aliases": [
      "EXTREPO"
    ]
  },
  "secrets": false,
  "license": "own-open",
  "areas": {
    "add": [],
    "remove": []
  },
  "git": {
    "init": true,
    "hooks": true
  },
  "seed": {}
}
```

The seed text, if any, is IN-0002.
