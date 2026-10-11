---
title: "ADR-0021: mihon-source is a standalone service with a minimal admin, clients and extension stores"
status: accepted
tags: [sources, plugins, mihon, admin, security]
related: [decisions/ADR-0005-layered-source-architecture.md, modules/mihon-source/overview.md, modules/source-mihon/overview.md, contracts/mihon-source-api.md, architecture/networking.md, research/mihon-extension-store.md]
inputs: [IN-0003, IN-0006]
updated: 2026-10-11
---

# ADR-0021: mihon-source as a standalone service with a minimal admin

- **Date:** 2026-10-11
- **Deciders:** @aurimasniekis
- **Supersedes:** [ADR-0005](ADR-0005-layered-source-architecture.md)

## Context

ADR-0005 layered the sources: `source-api` as the general contract, `source-mihon` (Go) with store logic, trust and orchestration, and `mihon-source` as a "small tool to interact with mihon extensions directly via api" (IN-0003 §3.4) with no store logic. Then the owner asked for more on mihon-source: "minimal admin with like intereaction with sources, like client and integration management like api keys and etc" (IN-0006 §1). Asked which integrations, they picked solvers, proxies/network profiles **and extension stores**, adding "extension repositories, also let source pickup configs from sources-api later on". The admin is a small React SPA, and the admin logs in with one admin token (IN-0006 §2).

## Decision

- **The layering stays.** `source-api` (Go) is the general source contract and SDK that every source kind implements. `source-mihon` (Go) is the Mihon implementation on the Panelarr side. `mihon-source` (Kotlin/JVM) loads Mihon extensions and serves them over the API. Other source kinds (local files, OPDS, native scrapers, other ecosystems) plug into source-api.
- **mihon-source is a self-sufficient standalone service** with a **minimal admin**:
  - **sources:** browse and test them (popular, latest, search with filters, details, chapters, pages) and edit their settings;
  - **clients:** callers such as a Panelarr server or scripts, each with its own **API key** and scope;
  - **integrations:** solvers (FlareSolverr/Byparr) and proxies / network profiles, assigned per source;
  - **extension stores (repositories):** add store URLs, list what they offer, install and update from them, and pin and verify each store's signing key.
- **Admin UI:** a small **React SPA** on the [ADR-0006](ADR-0006-technology-stack.md) stack, built into the image and served by mihon-source.
- **Admin auth:** **one admin token** (from an env var, or generated on first start and shown once). Clients get **scoped API keys** (e.g. read sources vs admin).
- **Still out of mihon-source:** no library, no users beyond the admin token and clients, no downloads. State stays in files under `/data`, not a database.
- **Later:** mihon-source can **pick up its config (stores, profiles, solvers) from the Panelarr side** over the source-api contracts. The local admin stays for standalone use. How it works and which side wins: [Q-0030](../questions/README.md).

## Consequences

- source-mihon and mihon-source now both know about stores. Whether source-mihon keeps its own store logic, pushes config to mihon-source, or shrinks to a pass-through is [Q-0026](../questions/README.md), now more pressing.
- Store parsing and signing-key verification are built in Kotlin first ([store format](../research/mihon-extension-store.md)).
- mihon-source exposes an admin surface, so auth is in from the first slice. Secrets (admin token, API keys, proxy credentials) are hashed or encrypted at rest and never returned once set ([security](../architecture/security.md)).
- The mihon-source repo gains a Node toolchain for the SPA. The image build is multi-stage, and the runtime image stays JVM-only.
- The KB and the public repo still never say where extensions can be obtained ([ADR-0020](ADR-0020-public-kb-with-aliases.md)), and Panelarr ships with no store configured ([ADR-0009](ADR-0009-plugins-not-bundled.md)).

## Alternatives considered

| Option | Why not |
|---|---|
| Keep ADR-0005: stores only in source-mihon | mihon-source alone couldn't install from a store, which weakens the standalone mode the owner wants |
| Server-rendered admin (htmx), no Node build | Offered; the owner picked a React SPA |
| Admin user and password | Offered; one admin token is enough for a small service |
