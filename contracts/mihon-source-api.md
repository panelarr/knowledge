---
title: mihon-source API
status: draft
tags: [contract, mihon]
related: [decisions/ADR-0021-mihon-source-standalone-admin.md, contracts/source-plugin.md, modules/mihon-source/overview.md, modules/source-mihon/overview.md]
inputs: [IN-0003, IN-0006]
updated: 2026-10-11
---

# mihon-source API

## Summary

mihon-source is a **standalone service** that exposes Mihon extensions over an API (IN-0003 §3.4). It implements **`panelarr.source.v1`** directly, so it is usable alone and as a remote source plugin (IN-0003 §6). Its **`panelarr.mihon.v1`** admin API covers extensions, extension stores, clients and API keys, and integrations (solvers, network profiles), and it backs a minimal admin SPA ([ADR-0021](../decisions/ADR-0021-mihon-source-standalone-admin.md)). Everything is served over gRPC and HTTP/JSON with OpenAPI.

## `panelarr.mihon.v1` (admin) sketch
```proto
service MihonAdmin {
  rpc ListExtensions(Empty) returns (ExtensionList);           // pkg, name, version, lib version, sources, signing fingerprint, load errors
  rpc InstallExtension(InstallRequest) returns (Extension);    // from URL (jar preferred, apk → dex2jar) or uploaded bytes; optional expected sha256/fingerprint
  rpc UninstallExtension(ExtensionRef) returns (Empty);
  rpc ReloadExtension(ExtensionRef) returns (Extension);
}

service MihonStores {                                          // extension stores (repositories)
  rpc ListStores(Empty) returns (StoreList);                   // url, name, pinned signing-key fingerprint, last refresh, errors
  rpc AddStore(AddStoreRequest) returns (Store);               // fetches repo.json, pins its signingKey
  rpc RemoveStore(StoreRef) returns (Empty);
  rpc RefreshStore(StoreRef) returns (Store);
  rpc ListAvailable(ListAvailableRequest) returns (AvailableList); // extensions offered, installed version, update available, content warning
  rpc InstallFromStore(StoreInstallRequest) returns (Extension);   // jarUrl else apkUrl; signing key and sha256 verified
}

service MihonClients {                                         // admin scope only
  rpc ListClients(Empty) returns (ClientList);                 // name, scopes, created, last used; never the key
  rpc CreateClient(CreateClientRequest) returns (ClientWithKey); // key shown once
  rpc RotateClientKey(ClientRef) returns (ClientWithKey);
  rpc DeleteClient(ClientRef) returns (Empty);
}

service MihonIntegrations {
  rpc ListSolvers / PutSolver / DeleteSolver;                  // FlareSolverr / Byparr endpoints
  rpc ListProfiles / PutProfile / DeleteProfile;               // network profiles (architecture/networking.md)
  rpc AssignProfile(AssignProfileRequest) returns (Empty);     // source → profile; a pushed SetNetworkProfile overrides it (Q-0030)
}
```

## As built (mihon-source slice 2)
- Services follow buf STANDARD naming: `MihonAdminService`, `MihonStoresService`, `MihonClientsService` (+ `WhoAmI`, `UpdateClient`), `MihonIntegrationsService` (+ `SetDefaultProfile`, `ListAssignments` reporting pushed / assigned / default / none). Each RPC has its own Request/Response.
- Client keys look like `msk_…`. Scopes as built: `sources:read`, `sources:write` (SetSettings, SetNetworkProfile; implies read), `admin`. Unknown RPCs need admin.

## Auth
- **Admin token:** one secret from an env var, or generated on first start and shown once. Full access, and the admin SPA logs in with it.
- **Clients:** each caller (a Panelarr server, a script) gets an **API key** with scopes: `sources:read` for `panelarr.source.v1`, `admin` for `panelarr.mihon.v1` (suggested scope names). Sent as `Authorization: Bearer` / gRPC metadata ([contracts and transport](../architecture/contracts-and-transport.md)).
- Keys are stored hashed and never returned after creation.

## Boundaries
- **Two ways to configure.** Standalone users configure mihon-source through its admin ([ADR-0021](../decisions/ADR-0021-mihon-source-standalone-admin.md)). In the Panelarr stack the main app owns the config: source-mihon declares it (repos/stores, settings, common services) and passes it to mihon-source (Q-0026, Q-0030 answered, IN-0007 §1). source-mihon calls `MihonStores` rather than parsing stores itself (Q-0031, IN-0015). An install request may still carry an expected fingerprint and SHA-256, which mihon-source enforces.
- **No database.** Jars, prefs, cookies, stores, clients and integrations are files under `/data`.
- **No library, no users, no downloads.** Those belong to server.
- **Without Panelarr:** `docker run panelarr/mihon-source`, open the admin with the admin token, add a store or install a jar by URL, create a client key, then `curl -H 'Authorization: Bearer …' /v1/sources/{id}/popular`.
