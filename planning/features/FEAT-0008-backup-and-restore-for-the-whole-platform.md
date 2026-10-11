---
title: "FEAT-0008: Backup and restore for the whole platform"
status: proposed
tags: [feature, ops, backup, server, meta, mihon-source]
related: [architecture/storage-layout.md, decisions/ADR-0029-meta-required.md, planning/features/FEAT-0002-jobs-page-in-every-admin.md]
inputs: [IN-0042]
milestone: ""
priority: P2
updated: 2026-10-11
---

# FEAT-0008: Backup and restore for the whole platform

## Problem

"the whole platform should have ability to make backups, not like db backups but something which would be able to restore everything" (IN-0042). A Postgres dump of one service doesn't restore a working platform: there are several services (server, meta, mihon-source, plugins), secrets and keys, plugin installs, stores and extensions, matches and settings.

## Outcome

An admin makes a backup (on demand or scheduled) that captures the whole platform's state. On a fresh install, restoring it brings back users, libraries, progress, Works and their source matches, settings, integrations, connected services and plugins, so everything works again (downloaded files re-linked or re-downloaded).

## Scope

- **In:**
  - an app-level, versioned **backup format** (a single archive with a manifest per service);
  - the server orchestrates the backup across connected services (meta, mihon-source via source-mihon, plugins), each service exporting its own state through its admin API;
  - scheduled backups as jobs (FEAT-0002) with retention;
  - written to any configured storage endpoint (FEAT-0007, Q-0041);
  - **restore** on a fresh install (the first-run wizard offers "restore from backup") and into an existing install with a dry run;
  - encryption with a passphrase ([Q-0042](../../questions/README.md)).
- **What a backup holds (suggestion, [Q-0042](../../questions/README.md)):**
  - **server:** users, grants, API keys (hashed), libraries, categories, progress and history, Works, source matches and priorities, chapter state, rules, settings, network profiles, trackers, a ChapterFile manifest;
  - **meta:** config, clients, integrations, provider settings and schedules, field locks, dismissed duplicates (not the catalogue: it re-syncs from providers);
  - **mihon-source:** stores (with pinned keys), installed extensions (list, or the files), source settings and prefs, cookies (optional), profiles, solvers, clients;
  - secrets and encryption keys (inside the encrypted archive);
  - downloaded files: optional, otherwise listed in the manifest to re-link or re-download.
- **Out:** live replication, point-in-time recovery (database tooling covers that), backing up third-party services (solvers, VPN containers).

## Acceptance criteria

- [ ] AC1: "Back up now" and a schedule produce one archive with a manifest (format version, Panelarr and service versions, contents, checksums), written to a chosen storage endpoint, with retention.
- [ ] AC2: Each service exposes export/import of its own state through its admin API; the server collects them into the archive. A service that is down is reported, and the backup is marked partial.
- [ ] AC3: Archives can be encrypted with a passphrase; secrets are never stored unencrypted.
- [ ] AC4: Restore on a fresh install (from the first-run wizard) brings back a working platform: users can sign in, libraries and progress are there, Works keep their matches, services and plugins are configured again, and downloaded files are re-linked when present at the restored storage path or queued for re-download.
- [ ] AC5: Restore into an existing install shows a dry run (what would change) and needs confirmation.
- [ ] AC6: Backups and restores are jobs (history, progress, errors); newer backups restore on newer versions (migrations), and an older Panelarr refuses a newer format with a clear message.

## Design notes

- Built on the storage interface (FEAT-0007) and the jobs model (FEAT-0002).
- Each service owns its export/import; the server is the orchestrator.
- **Open:** whether meta and mihon-source also offer stand-alone backups in their own admins (suggestion: yes, same export, for standalone users).

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| server, meta, mihon-source, web | — | — | — |

## Open questions

- [Q-0042](../../questions/README.md): contents, files or not, encryption, location.
