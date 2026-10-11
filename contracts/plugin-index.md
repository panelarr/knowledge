---
title: Plugin index format
status: draft
tags: [contract, plugins, index]
related: [decisions/ADR-0014-plugin-index-and-signing.md, research/mihon-extension-store.md, architecture/plugins.md]
inputs: [IN-0003]
updated: 2026-10-11
---

# Plugin index format

## Summary

This is a JSON document a hoster adds by URL, modelled loosely on Mihon's Extension Store ([research](../research/mihon-extension-store.md)). **Public home:** a JSON Schema in the shared plugin kit ([Q-0017](../questions/README.md)).

## Sketch
```json
{
  "schema": 1,
  "name": "Panelarr Official",
  "signingKeys": [{"id": "panelarr-2026", "alg": "minisign", "pub": "RWT..."}],
  "plugins": [{
    "id": "source-mihon",
    "kind": "source",
    "name": "Mihon extensions",
    "description": "Use Mihon extension stores through mihon-source",
    "homepage": "https://github.com/panelarr/source-mihon",
    "contentWarning": "MIXED",
    "versions": [{
      "version": "0.3.0",
      "contracts": {"panelarr.source": "v1"},
      "minHost": "0.5.0",
      "artifacts": [
        {"os": "linux", "arch": "amd64", "url": ".../source-mihon_linux_amd64.tar.gz", "sha256": "...", "sig": "..."},
        {"os": "linux", "arch": "arm64", "url": "...", "sha256": "...", "sig": "..."}
      ],
      "image": "panelarr/source-mihon:0.3.0",
      "requires": [{"service": "mihon-source", "contract": "panelarr.source/v1"}]
    }]
  }]
}
```

## Notes
- `requires` lets the UI say "this plugin needs a mihon-source endpoint" and offer the compose profile.
- The release workflow generates index entries ([repo standard](../architecture/repo-standard.md)).
- Signature algorithm and key rotation are open ([Q-0024](../questions/README.md)).
