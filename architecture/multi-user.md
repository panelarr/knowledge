---
title: Multi-user model
status: proposed
tags: [architecture, multi-user, auth]
related: [decisions/ADR-0003-shared-store-per-user-libraries.md, architecture/domain-model.md, architecture/security.md]
inputs: [IN-0002, IN-0003]
updated: 2026-10-11
---

# Multi-user model

## Summary

One install serves many people. **Content is shared; everything personal is per user** ([ADR-0003](../decisions/ADR-0003-shared-store-per-user-libraries.md)). This is the main gap Panelarr closes over Suwayomi, whose new multi-user mode still shares queues and skips ownership checks on file endpoints ([research](../research/suwayomi-server.md)).

| Shared (instance) | Per user |
|---|---|
| Plugins, sources, network profiles | Library entries, categories |
| Works, chapters, files, covers | Read progress, history, bookmarks |
| Metadata links | Tracker accounts and bindings |
| Download queue (de-duplicated) | Reader settings, UI prefs |
| Search index | Content-rating ceiling, allowed sources (set by admin) |

## Roles and permissions
- **Admin:** everything, including plugins, profiles, users, storage and deletions.
- **User:** by default may browse allowed sources, add to their own library, and read.
- **Grants:** `may_download` (queue downloads), `may_add_works`, `may_manage_metadata` (fix matches), allowed plugins/sources, content-rating ceiling, quotas (max library size, downloads per day).
- **Optional request flow** (later): users without `may_download` *request*, and an admin approves.

## Enforcement
- Every API handler resolves the **visible-Works scope** for the caller. **File and page endpoints check it too**, so there is no direct-object access (Suwayomi's gap).
- Downloads are attributed to the requesting user for quotas, but are stored once.
- The SSE event stream is filtered per user.

## Auth
- Local accounts (argon2id/bcrypt), with HTTP-only cookie sessions for web and API keys for 3rd-party tools.
- **Optional OIDC** (Authelia, Authentik, Keycloak). An optional trusted reverse-proxy header mode for SSO setups.
- **Default install:** creating the first account makes it the admin.
