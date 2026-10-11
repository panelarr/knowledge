---
title: "FEAT-0003: Accounts, roles and first-run setup"
status: proposed
tags: [feature, server, web, m2]
related: [architecture/multi-user.md, decisions/ADR-0003-shared-store-per-user-libraries.md, decisions/ADR-0029-meta-required.md]
inputs: [IN-0003, IN-0037, IN-0038]
milestone: "M2"
priority: P1
updated: 2026-10-11
---

# FEAT-0003: Accounts, roles and first-run setup

## Problem

Panelarr is multi-user from the first slice (IN-0037 §2; [ADR-0003](../../decisions/ADR-0003-shared-store-per-user-libraries.md)). A fresh install also needs meta connected, with a metadata provider, before anything can be added ([ADR-0029](../../decisions/ADR-0029-meta-required.md)).

## Outcome

A hoster opens Panelarr for the first time and creates the admin account. A wizard connects meta (and checks it has a provider with data) and optionally a source plugin. Then the admin invites users, who sign in and get their own libraries.

## Scope

- **In:**
  - local accounts (password, argon2id);
  - roles admin/user;
  - grants (`may_add`, `may_download`, allowed sources, content-rating ceiling);
  - sessions (cookie for web) and personal API keys;
  - the first-run wizard (admin → meta → metadata provider check → optional source plugin);
  - the users admin page.
- **Out:** OIDC and the trusted-proxy header (later), quotas (later), the request/approve flow (later).

## Acceptance criteria

- [ ] AC1: On an empty install, every route leads to the first-run wizard; the first account created is the admin; afterwards the wizard can't be reopened by anyone else.
- [ ] AC2: The wizard checks meta: reachable, admin key valid, at least one provider with entries. If not, it explains what to do (e.g. add meta-mangabaka and run a sync) and lets the admin retry; Panelarr shows "degraded" until meta is ready.
- [ ] AC3: Admins create, disable and delete users, set role and grants; users change their own password.
- [ ] AC4: Every API call enforces grants server-side: a user without `may_download` can't queue downloads; a source outside a user's allowed list is invisible to them; content above their ceiling is hidden everywhere (search, browse, library).
- [ ] AC5: Web sessions are HTTP-only, SameSite cookies with CSRF protection; personal API keys are scoped, hashed and shown once; login is rate-limited.
- [ ] AC6: Libraries are per user: two users adding the same work see their own entries and progress, and share one copy on disk.

## Design notes

[multi-user](../../architecture/multi-user.md), [security](../../architecture/security.md), [domain model](../../architecture/domain-model.md).

## Delivery

| Repo | Goal | PR/MR | State |
|---|---|---|---|
| server, web | — | — | — |

## Open questions

- Invite links vs admin-set passwords (suggestion: both).
