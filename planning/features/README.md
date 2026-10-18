# Features

Scoped units of product value, each with **acceptance criteria** that QA tests against. Create one with `python3 tools/kb.py new feature "…"` ([template](../../meta/templates/feature.md)). A feature is `accepted` when the owner agrees its scope and criteria. It is then ready to be built through a [goal](../../agents/goals/README.md).

| ID | Feature | Milestone | Status |
|---|---|---|---|
| [FEAT-0001](FEAT-0001-meta-search-engine-integrations.md) | meta search engine integrations (Typesense, then Meilisearch; optional) | M3 | accepted |
| [FEAT-0002](FEAT-0002-jobs-page-in-every-admin.md) | Jobs page in every admin (runs, statuses, Run now) | — | accepted |
| [FEAT-0003](FEAT-0003-accounts-roles-and-first-run-setup.md) | Accounts, roles and first-run setup (wizard incl. meta) | M2 | accepted |
| [FEAT-0004](FEAT-0004-add-a-work-from-meta-and-match-sources.md) | Add a work from meta and match sources | M2 | accepted |
| [FEAT-0005](FEAT-0005-unified-chapters-and-update-checks.md) | Unified chapters and update checks | M2 | accepted |
| [FEAT-0006](FEAT-0006-mobile-first-reader.md) | Mobile-first reader (per-source settings) | M2 | accepted |
| [FEAT-0007](FEAT-0007-downloads-to-the-shared-library.md) | Downloads to the shared library (CBZ) | M2 | accepted |
| [FEAT-0008](FEAT-0008-backup-and-restore-for-the-whole-platform.md) | Backup and restore for the whole platform (all services, encrypted, to any storage) | — | accepted |
| [FEAT-0009](FEAT-0009-extensions-and-sources-in-panelarr-s-admin-with-languages.md) | Extensions and sources in Panelarr's admin, with languages (install from stores, language filters) | — | accepted |
| [FEAT-0010](FEAT-0010-shared-network-services-and-plugin-admin-settings-in-panelar.md) | Shared network services and plugin admin settings in Panelarr (solvers, proxies, profiles once for every plugin) | — | accepted |
| [FEAT-0011](FEAT-0011-better-chapter-copies-and-configurable-matching.md) | Better chapter copies and configurable matching (rate down bad copies, match rules, storage per source) | — | proposed |
| [FEAT-0012](FEAT-0012-reader-series-page-and-library-polish.md) | Reader, series page and library polish (calmer reader, plain chapter rows, icon menus, bookmarks) | — | accepted |
| [FEAT-0013](FEAT-0013-connected-services-admin-inside-panelarr.md) | Connected services' admin inside Panelarr (mihon-source and meta admin pages; network chosen from Panelarr) | — | accepted |
| [FEAT-0014](FEAT-0014-reading-history.md) | Reading history (a History tab, resume, remove, clear) | — | accepted |
| [FEAT-0015](FEAT-0015-updates-feed.md) | Updates feed (new chapters across the library, grouped by day and series) | — | accepted |
| [FEAT-0016](FEAT-0016-automatic-retries-for-failed-page-images.md) | Automatic retries for failed page images (in the server; per extension, overridable per source) | — | accepted |
