---
title: mihon-source API
status: draft
tags: [contract, mihon]
related: [contracts/source-plugin.md, modules/mihon-source/overview.md, modules/source-mihon/overview.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# mihon-source API

## Summary

mihon-source is a **small standalone tool** that exposes Mihon extensions over an API (IN-0003 §3.4). It implements **`panelarr.source.v1`** directly, so it is usable alone and as a remote source plugin (IN-0003 §6). It adds a tiny **`panelarr.mihon.v1`** admin service for installing extensions and managing their prefs. Both are served over gRPC and HTTP/JSON with OpenAPI.

## `panelarr.mihon.v1` (admin) sketch
```proto
service MihonAdmin {
  rpc ListExtensions(Empty) returns (ExtensionList);           // pkg, name, version, lib version, sources, signing fingerprint, load errors
  rpc InstallExtension(InstallRequest) returns (Extension);    // from URL (jar preferred, apk → dex2jar) or uploaded bytes; optional expected sha256/fingerprint
  rpc UninstallExtension(ExtensionRef) returns (Empty);
  rpc ReloadExtension(ExtensionRef) returns (Extension);
}
```

## Boundaries
- **No store logic.** Index parsing, update checks and signing **trust decisions** live in source-mihon ([module](../modules/source-mihon/overview.md)). mihon-source only *reports* the fingerprint and *enforces* an expected one if it is given one.
- **No database.** Jars, prefs and cookies are files under `/data`.
- **Without Panelarr:** `docker run panelarr/mihon-source`, then install a jar by URL, then `curl /v1/sources/{id}/popular`.
