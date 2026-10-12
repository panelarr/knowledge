---
title: "GOAL-0012: source plugins: extension packages and languages"
status: accepted
tags: [goal, agents, source-api, source-mihon, mihon-source]
related: [planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md, contracts/source-plugin.md, contracts/mihon-source-api.md, research/mihon-extension-store.md]
inputs: [IN-0052, IN-0053, IN-0054, IN-0055]
repos: [source-api, source-mihon, mihon-source]
session: "panelarr-mihon-source"
features: [FEAT-0009]
updated: 2026-10-12
---

# GOAL-0012: source plugins: extension packages and languages

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0012 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`accepted`, **Done 2026-10-12** (verified, pass; [test report](../../qa/reports/goal-0012-source-plugins-packages-done-verification.md)). The owner accepted [FEAT-0009](../../planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md) and gave the go (IN-0055). Plan first: send a `PROPOSE:` with the proto shape and slices before building; the keeper reviews it and shares it with `panelarr-server` and `panelarr-web` (GOAL-0013, GOAL-0014 build on it).

## Context

- Code: `~/Projects/Panelarr/source-api`, `~/Projects/Panelarr/source-mihon`, `~/Projects/Panelarr/mihon-source`. Work in worktrees; keep the checkouts on main (the server builds against `../source-api`).
- **Read first:** [FEAT-0009](../../planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md) (the owner's words in IN-0052..IN-0055 are quoted there), [contracts/source-plugin.md](../../contracts/source-plugin.md), [contracts/mihon-source-api.md](../../contracts/mihon-source-api.md), [research/mihon-extension-store.md](../../research/mihon-extension-store.md).
- **Accepted decisions are law** (Q-0043, Q-0044 answered):
  - the Extensions tab appears on a plugin's page **only if the plugin supports and provides it**: an optional, generic capability in `source.v1`, not a Mihon-specific server path;
  - languages are configurable **on the plugin and per extension**, and they decide **which sources are available**.
- Licences: source-api Apache-2.0; source-mihon and mihon-source GPL-3.0 (ADR-0025).

## Objective

1. **source-api (`source.v1`, additive):** an optional **package capability**, declared in the plugin's capabilities. Suggested shape (refine in your PROPOSE):
   - list available packages: id, name, languages, version, installed version, update available, content warning, origin (store), and the sources each provides with their languages;
   - install, update, uninstall a package (long-running: return when done or give a job/run handle; your call);
   - per-package settings, at least **enabled languages** (empty = all the plugin allows).
   - a plugin-level **languages** setting is plain config (the plugin's config schema).
   - `ListSources` lists only sources whose language is enabled at both levels.
   - SDK support and conformance cases for the capability (skipped when not declared).
2. **mihon-source:** what source-mihon needs that isn't there yet, notably per-extension enabled languages (a multi-language extension exposes only those sources) and anything missing from `ListAvailable` (per-source languages). Additive admin API changes only.
3. **source-mihon:** implement the capability by calling mihon-source (`ListAvailable`, `InstallFromStore`, `UninstallExtension`, update), add the plugin-level languages setting, and filter `ListSources` accordingly. The declarative `extensions` setting stays.
4. Also finish the queued `x-order` stamping in source-api's settings if it isn't done yet.

## How to work

1. Build in **slices**. Each slice works end to end (logic, interface, tests, docs).
2. One branch per slice. Follow each code repo's commit convention.
3. After each slice: `make check` (gated: only merge when it passes) → `REPORT:` to the keeper with what you built, what you assumed and how to test it.
4. Keep a progress file (`PROGRESS.md`) in the repo you lead from. **Re-read it whenever you lose context.**
5. Don't stop after each slice to ask. Go on unless blocked on the owner's decision.

## When something isn't decided

- `ASK:` the keeper first. Still open? `PROPOSE:` a working assumption that fits the accepted decisions, built cheap to change.

## Constraints

- Merge to local main yourself; **never push**. Don't touch the running compose stack.
- Proto changes are additive; `buf breaking` passes.
- No real store, extension or site names in any repo; tests use mihon-source's test extensions and fixture store.
- Observability per ADR-0027 for new paths (installs logged, metrics with bounded labels).

## Definition of Done

- [x] source-api: package capability and language filtering in `source.v1` (additive), SDK support, conformance cases; Apache-2.0
- [x] mihon-source: per-extension enabled languages and per-source languages available through its admin API
- [x] source-mihon: implements the capability end to end against the real mihon-source and the fixture store; plugin-level languages; `ListSources` filtered
- [x] `make check` green in all three repos; leak-check clean; docs updated
- [x] `DONE:` with evidence per box

## History

- 2026-10-12: brief written and dispatched on the owner's go (IN-0055); plan to be PROPOSEd first.
- 2026-10-12: x-order done first (source-api `a3e91cd`, source-mihon `aa80905`).
- 2026-10-12: plan PROPOSEd and accepted by the keeper (server comments pending before slice 1 merges). `PLUGIN_CAPABILITY_PACKAGES`; ListPackages/GetPackage/Install/Update/Uninstall/SetPackageSettings (additive; others answer UNIMPLEMENTED); Package with langs, versions, offers per store, sources with lang and enabled, settings `enabled_langs`; plugin-level `languages` config; a source is available only if its lang passes both levels ("all"/"multi" enabled explicitly), other sources answer NOT_FOUND; install/update synchronous with a long deadline; single-source enable/disable and admin-only access stay with the host. Slices: 1 source-api proto+SDK+conformance, 2 mihon-source per-extension languages + fixture-store export, 3 source-mihon capability + languages + e2e, 4 docs.
- 2026-10-12: server comments folded in: install/update idempotent and never half-installed; `package_id` on `Source`; `PackageSource.enabled` renamed `available` (vs the server's admin enable/disable); store failures as ErrorInfo reasons STORE_FETCH_FAILED / STORE_INVALID; pagination optional. Slice 1 may merge.
- 2026-10-12: mihon-source per-source settings schemas carry per-property `x-order` (`b3550d7`). Plan for the server's guarantees: slice 1 defines idempotency in the contract (fake + conformance), slice 2 makes mihon-source's install finish even if the caller goes away, slice 3 makes source-mihon idempotent.
- 2026-10-12: REPORT: **slice 1 done** (source-api `2ac5461`): `PLUGIN_CAPABILITY_PACKAGES`, the six package RPCs, `Package`/`PackageOffer`/`PackageSource{available}`/`PackageSettings{enabled_langs}`, `Source.package_id = 9`, error reasons STORE_FETCH_FAILED (7) / STORE_INVALID (8), package IDs `^[A-Za-z0-9][A-Za-z0-9._-]*$`; idempotency documented and checked by conformance; SDK on Plugin and every Client transport; plugintest fake with packages (one multi-language, from two stores); conformance read-only by default plus a `--package` install walk; settings.Parse refuses malformed `properties`. source-mihon answers UNIMPLEMENTED until slice 3 (`e8cfe2c`). The server still builds and vets against it (keeper check). Next: slice 2 (mihon-source).
- 2026-10-12: REPORT: **slice 2 done** (mihon-source `17f1f2b`): `SetExtensionLanguages` (`PUT /v1/admin/extensions/{pkgName}/languages`), `Extension.enabled_langs`, `ExtensionSource.available`; every source path (list, browse, health checks, gauge, cache) follows it; stored with the extension (survives restart and update). Admin Languages control on multi-language extensions, with the "all"/"multi" hint. Re-installing the installed version returns at once; a cancelled install leaves the previous version installed and loaded (tested). Fixture-store export task for e2e (v1/v2, en and fr sources, test key). Next: slice 3 (source-mihon).
- 2026-10-12: REPORT: **slice 3 done** (source-mihon `b5dbae0`): PACKAGES over mihon-source (offers per store, best supported offer, idempotent install/update/uninstall, languages forwarded), plugin-level `languages`, ListSources filtered with `package_id`, NOT_FOUND outside the languages, metrics and logs; e2e against the real mihon-source and the fixture store.
- 2026-10-12: DONE received and verified on clean clones (all three `make check`/`gradlew check`, plus source-mihon `make e2e` against the real mihon-source). Goal closed.
