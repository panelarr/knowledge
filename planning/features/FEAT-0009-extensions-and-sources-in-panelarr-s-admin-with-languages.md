---
title: "FEAT-0009: Extensions and sources in Panelarr's admin, with languages"
status: proposed
tags: [feature, admin, sources, source-mihon, mihon-source, web, server]
related: [modules/source-mihon/overview.md, contracts/mihon-source-api.md, contracts/source-plugin.md, research/mihon-extension-store.md, modules/web/overview.md]
inputs: [IN-0052, IN-0039]
milestone: ""
priority: P2
updated: 2026-10-12
---

# FEAT-0009: Extensions and sources in Panelarr's admin, with languages

## Problem

"so i see now we can add extension store, but where from server admin i can install select extensions? also would be good to have languages assigned to the extensions/sources?" (IN-0052).

In v0, Panelarr's admin can add extension stores (source-mihon's settings, IN-0051), but installing extensions means typing package names into a text list or using mihon-source's own admin. The connected-service admin inside Panelarr was left out of v0 (IN-0039). Sources carry a language (`lang` in `ListSources`, and per extension and source in the store index, [research](../../research/mihon-extension-store.md)), but Panelarr doesn't use it.

## Outcome

An admin browses the extensions the configured stores offer, sees each one's language and content warning, and installs, updates or removes them from Panelarr's admin. Sources show their language everywhere, and lists can be filtered by language.

## Scope

- **In (suggested):**
  - an **Extensions** page in Panelarr's admin: available extensions from all stores (name, language, version, installed version, update available, content warning, store), with search and a language filter; install, update and uninstall;
  - the **Sources** page shows each source's language and extension, with a language filter, and lets the admin enable or disable single sources (so a multi-language extension can keep only some languages);
  - language shown on sources in browse, search and a work's source tabs;
  - how languages limit browse, search and matching: open, [Q-0044](../../questions/README.md).
- **Out:**
  - the rest of mihon-source's admin inside Panelarr (clients, integrations, health checks; IN-0039 stays a later feature);
  - other source plugins' install flows (the shape should allow them, per Q-0043).

## Acceptance criteria (draft)

- [ ] AC1: With a store added, Admin → Extensions lists its extensions with language, version and content warning; a language filter and search narrow the list.
- [ ] AC2: Install puts the extension on mihon-source (signing key and checksum verified as today), and its sources appear in Admin → Sources within seconds, each with its language.
- [ ] AC3: An installed extension with a newer version in its store shows "Update"; update and uninstall work; an uninstalled extension's sources are marked absent, and works matched to them keep their history.
- [ ] AC4: A single source can be disabled; disabled sources aren't searched, browsed or matched.
- [ ] AC5: Language shows on every source in admin, browse and a work's source tabs.
- [ ] AC6: Only admins can install, update, uninstall or disable; everything is a plain API call (the web app has no Mihon-specific backdoor).

## Design notes

- mihon-source already has the API: `ListAvailable`, `InstallFromStore`, `UninstallExtension`, `ListExtensions` ([contracts/mihon-source-api.md](../../contracts/mihon-source-api.md)).
- The path from Panelarr is open ([Q-0043](../../questions/README.md)). *Suggestion:* an optional, generic **package capability** in `source.v1` (list available packages, install, update, uninstall, with language and content-warning fields) that source-mihon implements by calling mihon-source. Panelarr's server and web then stay plugin-neutral, which fits [principles](../../product/principles.md). The alternative is IN-0039's route (the server calls mihon-source's admin API with an admin key), which is Mihon-specific.
- source-mihon's `extensions` setting stays as the declarative list (installed when missing) for people who configure by file.

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| | | | |

## Open questions

- [Q-0043](../../questions/README.md): generic plugin capability or mihon-source's admin API?
- [Q-0044](../../questions/README.md): what languages drive.
