---
title: "GOAL-0013: server: extensions, source languages, admin-only sources"
status: accepted
tags: [goal, agents, server]
related: [planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md, contracts/server-api.md, agents/goals/GOAL-0012-source-plugins-extension-packages-and-languages.md]
inputs: [IN-0052, IN-0053, IN-0054, IN-0055]
repos: [server]
session: "panelarr-server"
features: [FEAT-0009]
updated: 2026-10-12
---

# GOAL-0013: server: extensions, source languages, admin-only sources

The brief a coding session works from. A short paste-in version points here: *"Work on GOAL-0013 in the knowledge base at `~/Projects/Panelarr/knowledge`; read it first and follow it."* Change this file to change the goal.

## Status

`accepted` (2026-10-12): the owner accepted [FEAT-0009](../../planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md) (IN-0055). Depends on GOAL-0012's `source.v1` shape: wait for the keeper to forward `panelarr-mihon-source`'s PROPOSE, comment on it, then PROPOSE your own plan. Slices that don't need the new protos (admin-only sources, source enable/disable, languages on sources) can start right away.

## Context

- Code: `~/Projects/Panelarr/server`; worktrees; builds against `../source-api`.
- **Read first:** [FEAT-0009](../../planning/features/FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md), [contracts/server-api.md](../../contracts/server-api.md), GOAL-0012.
- **Accepted decisions are law** (IN-0053..IN-0055):
  - the Extensions tab lives on the plugin's page and appears only if the plugin declares the package capability;
  - languages are set on the plugin and per extension and decide which sources are available;
  - **sources are admin-only**: only admins list, manage and browse sources directly; regular users see sources only on a library item (a work's sources); admins keep a "browse a source" view for testing.

## Objective

1. **Packages API** (admin scope): for a plugin that declares the capability, list available packages (with languages, versions, update available, content warning), install, update, uninstall, and per-package language settings. Long operations report progress (jobs or events, consistent with the rest of `/api/v1`).
2. **Sources:** store and return each source's language and providing package; admin enable/disable per source; disabled sources and sources in disabled languages aren't searched, browsed or matched; re-sync the plugin after package changes so sources appear within seconds.
3. **Admin-only sources:** source listing and direct source browsing/search outside a work require admin; a work's own sources stay visible to users who can see the work. Update the spec, and tell `panelarr-web` what changed.
4. Uninstall: a source that disappears is marked absent; works matched to it keep their history (FEAT-0009 AC3).

## How to work

As in your earlier goals: slices, gated `make check`, `REPORT:` per slice, `PROGRESS.md`, keep going unless blocked.

## Constraints

- Merge to local main yourself; never push; don't touch the running stack. API changes additive where possible; the admin-only change is a deliberate break for non-admins, so document it in the spec and changelog.

## Definition of Done

- [ ] Packages API for capable plugins; per-package languages
- [ ] Source language, package, enable/disable; filtering in search, browse and matching
- [ ] Admin-only source listing and browsing, enforced in the API, with tests for both roles
- [ ] Spec and docs updated; `make check` green; leak-check clean
- [ ] `DONE:` with evidence per box

## History

- 2026-10-12: brief written and dispatched on the owner's go (IN-0055).
- 2026-10-12: plan PROPOSEd and accepted by the keeper. S1 admin-only sources (`feat(api)!:`; source listing, popular, latest, search, filters, series, chapters move to admin; work-bound calls, attach/match, reader pages and signed images stay user). S2 source filters (`plugin_id`, `enabled`, `present`), proof that disabled/absent sources are skipped everywhere, and AC3 (an absent source keeps a work's links, history and downloads). S3 packages after GOAL-0012 (capability flag on Plugin, `/plugins/{id}/packages` list/install/update/uninstall as queue tasks, per-package settings, `package` on sources). Answers: `addFromSource` stays `user` (grants and may_add still apply; working assumption, cheap to change); no server language setting (languages live in plugin config and package settings, IN-0054); admin read-only keys lose source browsing (admin scope required, consistent with admin-only sources).
- 2026-10-12: REPORT: **S1 done** (`4a51c86`, merge `611c0e6`): listSources, sourcePopular, sourceLatest, sourceSearch, sourceFilters, sourceSeries, sourceChapters are admin-only (`feat(api)!:`, BREAKING CHANGE footer, docs/api.md "Changes within v1"); signed source images, addFromSource and work-scoped calls stay user. Tests: every role on all seven endpoints, read-only admin keys refused, users still see a work's sources with lang, chapters and covers. web told. Next: S2.
- 2026-10-12: added to S2: a work-scoped source search for match fixers (`POST /works/{id}/sources/{source_id}/search`, may_manage_matches, usable and allowed sources only), so users search sources only on a library item (IN-0054).
