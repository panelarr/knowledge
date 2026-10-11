---
title: "ADR-0025: Licences: GPL-3.0 for apps, Apache-2.0 for SDKs and protos"
status: accepted
tags: [legal, repos, licence]
related: [architecture/repo-standard.md, modules/README.md]
inputs: [IN-0014]
updated: 2026-10-11
---

# ADR-0025: GPL-3.0 apps, Apache-2.0 SDKs and protos

- **Date:** 2026-10-11
- **Deciders:** @aurimasniekis

## Context

[Q-0012](../questions/README.md) asked which licence the public code repos use. Plugin SDKs may want a permissive licence, and mihon-source no longer reuses Suwayomi code (Q-0003), so nothing upstream constrains it. The owner chose GPL-3.0 for the apps and Apache-2.0 for the SDKs (IN-0014 §2).

## Decision

| Code | Licence |
|---|---|
| **Apps and services:** server, web, meta (service), mihon-source (service), source-mihon, source-local, deploy, and Panelarr's own plugins (e.g. meta-mangabaka) | **GPL-3.0** |
| **Contracts and SDKs:** the protos (`panelarr.source.v1`, `panelarr.metadata.v1`, `panelarr.meta.v1`, `panelarr.mihon.v1`), generated code, source-api, and the meta plugin SDK | **Apache-2.0** |

- So third parties can write plugins under any licence they like.
- Where one repo holds both kinds (e.g. `meta`: service + protos + SDK; `mihon-source`: service + its protos), the repo's `LICENSE` is GPL-3.0, and the proto/SDK directories carry their own Apache-2.0 `LICENSE` and SPDX headers. Each file says which applies.
- *Suggestion, not decided:* SPDX `GPL-3.0-or-later` for the apps. If the owner wants `-only`, it changes nowhere else.
- The KB keeps its template licences (MIT tooling, CC BY 4.0 docs).

## Consequences

- Every repo adds `LICENSE` now. The READMEs drop "licence to be decided".
- Mihon extensions (Apache-2.0 in EXTREPO) are loaded at runtime, never shipped. This is compatible.
- MangaBaka's CC BY-NC-SA data is unaffected: it is downloaded by the hoster and never shipped.

## Alternatives considered

| Option | Why not |
|---|---|
| AGPL-3.0 apps | Offered; not chosen |
| Apache-2.0 or MIT everywhere | Offered; not chosen |
