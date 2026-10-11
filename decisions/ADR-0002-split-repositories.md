---
title: "ADR-0002: One repository per module"
status: accepted
tags: [repos, architecture]
related: [architecture/overview.md, modules/README.md]
inputs: [IN-0002, IN-0003]
updated: 2026-10-11
---

# ADR-0002: One repository per module

- **Date:** 2026-10-11 · **Deciders:** author

## Context
The Mihon wrapper and the metadata service must also work **standalone** (IN-0002). The author chose "fully split, meta separate too" (IN-0003 §2).

## Decision
Each module is its own git repo under `~/Projects/Panelarr/`, with its own session and its own release cycle:

| Repo | Role |
|---|---|
| `knowledge` | private KB (this) |
| `server` | Go core *arr* app; plugin host; embeds web |
| `web` | SPA/PWA |
| `source-api` | Go source-plugin contract, SDK, conformance tests |
| `meta` | Go metadata service + metadata-plugin contract/SDK |
| `source-mihon` | Go source plugin for Mihon extensions |
| `mihon-source` | Kotlin/JVM small tool running Mihon extensions |
| `source-local` | Go source plugin for the user's own files (*proposed* as its own repo) |
| `meta-<provider>` | metadata plugins (*layout open*, [Q-0017](../questions/README.md)) |
| `deploy` | compose, Unraid templates, AIO image |

## Consequences
- Contracts must be versioned and published as artifacts (Go modules, protobuf, OpenAPI), because there is no monorepo refactor safety.
- Each repo carries its own CI, docs and releases ([ADR-0008](ADR-0008-public-repo-standard-and-images.md)).

## Alternatives considered
| Option | Why not |
|---|---|
| One monorepo | Author preferred split; standalone tools want independent releases |
| Split with meta inside server | Author chose meta separate |
