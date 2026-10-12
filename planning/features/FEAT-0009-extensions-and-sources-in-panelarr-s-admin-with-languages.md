---
title: "FEAT-0009: Extensions and sources in Panelarr's admin, with languages"
status: accepted
tags: [feature, admin, sources, source-mihon, mihon-source, web, server]
related: [modules/source-mihon/overview.md, contracts/mihon-source-api.md, contracts/source-plugin.md, research/mihon-extension-store.md, modules/web/overview.md]
inputs: [IN-0052, IN-0053, IN-0054, IN-0055, IN-0039]
milestone: ""
priority: P2
updated: 2026-10-12
---

# FEAT-0009: Extensions and sources in Panelarr's admin, with languages

## Problem

"so i see now we can add extension store, but where from server admin i can install select extensions? also would be good to have languages assigned to the extensions/sources?" (IN-0052).

In v0, Panelarr's admin can add extension stores (source-mihon's settings, IN-0051), but installing extensions means typing package names into a text list or using mihon-source's own admin. The connected-service admin inside Panelarr was left out of v0 (IN-0039). Sources carry a language (`lang` in `ListSources`, and per extension and source in the store index, [research](../../research/mihon-extension-store.md)), but Panelarr doesn't use it.

Placement (IN-0053, the owner): "extension list page should be on mihon plugin not in general app, some source can be only one site, and some multi like mihon."

Capability, languages and who controls sources (IN-0054, the owner): "q43 yeah if plugin does support/provide it. q43 the source plugin can have configurable and extension level configurable languages so it would influence what sources are available. Also sources should be admin only controllable so simple user would only see sources in the library item or etc"

## Outcome

On the Mihon plugin's own page, an admin browses the extensions the configured stores offer, sees each one's language and content warning, and installs, updates or removes them from Panelarr's admin. Languages are set on the plugin and per extension, and they decide which sources exist. Sources are an admin concern: regular users see sources only where they're attached to a library item.

## Scope

- **In (suggested):**
  - an **Extensions** tab on the **source-mihon plugin's page** (Admin → Plugins → source-mihon), not a page of the general app (IN-0053). Plugins that are a single site have no such list; plugins that host many sites (like Mihon) do. The tab lists available extensions from all stores (name, language, version, installed version, update available, content warning, store), with search and a language filter; install, update and uninstall;
  - **languages** (IN-0054): a plugin-level language setting (which languages the plugin offers at all) and a per-extension override; together they decide **which sources are available**. A multi-language extension exposes only the sources in its enabled languages. Languages show on extensions and sources, with filters;
  - the admin **Sources** page shows each source's language and extension, with a language filter, and lets the admin enable or disable single sources;
  - **sources are admin-only** (IN-0054): only admins manage and browse sources directly. Regular users see sources only in context, on a library item (a work's source tabs and the like). The source browsing that v0 offers every user becomes admin-only.
- **Out:**
  - the rest of mihon-source's admin inside Panelarr (clients, integrations, health checks; IN-0039 stays a later feature);
  - other source plugins' install flows (the shape should allow them, per Q-0043).

## Acceptance criteria

- [ ] AC1: With a store added, the source-mihon plugin page's Extensions tab lists its extensions with language, version and content warning; a language filter and search narrow the list.
- [ ] AC2a: The plugin's language setting and an extension's language override change which of its sources are listed; a source in a language that's turned off isn't available for search, browse or matching.
- [ ] AC2: Install puts the extension on mihon-source (signing key and checksum verified as today), and its sources appear in Admin → Sources within seconds, each with its language.
- [ ] AC3: An installed extension with a newer version in its store shows "Update"; update and uninstall work; an uninstalled extension's sources are marked absent, and works matched to them keep their history.
- [ ] AC4: A single source can be disabled; disabled sources aren't searched, browsed or matched.
- [ ] AC5: Language shows on every source in the admin and on a work's source tabs.
- [ ] AC8: A regular user has no Sources page or direct source browsing; they see a work's sources on the work. The API enforces it (admin scope for source listing and browsing outside a work).
- [ ] AC7: A single-site source plugin's page has no Extensions tab.
- [ ] AC6: Only admins can install, update, uninstall or disable; everything is a plain API call (the web app has no Mihon-specific backdoor).

## Design notes

- mihon-source already has the API: `ListAvailable`, `InstallFromStore`, `UninstallExtension`, `ListExtensions` ([contracts/mihon-source-api.md](../../contracts/mihon-source-api.md)).
- Where it lives: the plugin's page (IN-0053). How: shown **when the plugin supports and provides it** (Q-0043, IN-0054), i.e. an optional, generic **package capability** in `source.v1` (list available packages, install, update, uninstall, with language and content-warning fields) that source-mihon implements by calling mihon-source. Panelarr's server and web then stay plugin-neutral, which fits [principles](../../product/principles.md). Per-extension languages travel with the capability (a package's settings); plugin-level languages are part of the plugin's config schema.
- source-mihon's `extensions` setting stays as the declarative list (installed when missing) for people who configure by file.

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| source-api, source-mihon, mihon-source | [GOAL-0012](../../agents/goals/GOAL-0012-source-plugins-extension-packages-and-languages.md) | — | planning |
| server | [GOAL-0013](../../agents/goals/GOAL-0013-server-extensions-source-languages-admin-only-sources.md) | — | planning |
| web | [GOAL-0014](../../agents/goals/GOAL-0014-web-extensions-tab-admin-sources-no-user-source-browsing.md) | — | planning |

## Open questions

- Answered: [Q-0043](../../questions/README.md), [Q-0044](../../questions/README.md) (IN-0054).
- Answered (IN-0055): admins keep a "browse a source" view for testing, in Admin → Sources.
