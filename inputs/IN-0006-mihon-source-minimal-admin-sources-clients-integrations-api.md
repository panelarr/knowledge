# IN-0006: mihon-source minimal admin: sources, clients, integrations, API keys

- **Received:** 2026-10-11
- **From:** @aurimasniekis
- **Distilled into:** ADR-0021 (supersedes ADR-0005), Q-0030, Q-0026 note, agents/goals/GOAL-0001-mihon-source-v0-run-mihon-extensions-over-the-source-api.md, contracts/mihon-source-api.md, modules/mihon-source/overview.md, modules/source-mihon/overview.md

---

## §1 Request

also on mihon source i want minimal admin with like intereaction with sources, like client and integration management like api keys and etc

## §2 Answers to the keeper's questions

1. *Which "integrations" should the mihon-source admin manage? (Clients = callers like Panelarr server or scripts, each with its own API key.)* Options offered: Solvers; Proxies / network profiles; Extension stores (noted as crossing ADR-0005).
   → Picked **Solvers**, **Proxies / network profiles**, **Extension stores**, and wrote: "extension repositories, also let source pickup configs from sources-api later on"
2. *How should the admin UI be built?* Options: server-rendered + htmx (recommended); small React SPA.
   → **"Small React SPA"**
3. *How does the admin itself log in?* Options: one admin token (recommended); admin user + password.
   → **"One admin token (Recommended)"**: a single admin secret from an env var, or generated on first start and printed once; clients get scoped API keys (read sources vs admin).
