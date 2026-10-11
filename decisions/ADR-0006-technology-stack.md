---
title: "ADR-0006: Go services, Kotlin/JVM for Mihon, React + TanStack SPA"
status: accepted
tags: [stack]
related: [architecture/overview.md]
inputs: [IN-0002, IN-0003]
updated: 2026-10-11
---

# ADR-0006: Technology stack

- **Date:** 2026-10-11 · **Deciders:** author

## Decision
| Module | Stack |
|---|---|
| server, meta, source-api, source-mihon, source-local, meta plugins | **Go** |
| mihon-source | **Kotlin/JVM** (Mihon extensions are Kotlin compiled to dex; they need a JVM, coroutines, OkHttp 5, kotlinx.serialization) |
| web | **Vite + React + TanStack Router, Query, Virtual, Pacer, Store**, SPA installable as a PWA (web + mobile) |

## Alternatives considered
| Option | Why not |
|---|---|
| Java for mihon-source | More friction with Kotlin-centric extension APIs (coroutines, serialization) |
