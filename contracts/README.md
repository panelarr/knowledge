# Contracts

The **reasoning and sketches** behind Panelarr's interfaces. The authoritative specs (protos, OpenAPI, JSON Schema) live in the **public repos** ([contracts and transport](../architecture/contracts-and-transport.md)). Once a public spec exists, these docs point to it and keep only the *why*.

| Doc | Contract | Public home | Status |
|---|---|---|---|
| [source-plugin.md](source-plugin.md) | `panelarr.source.v1`: every source plugin | `source-api` | draft |
| [mihon-source-api.md](mihon-source-api.md) | mihon-source: source v1 + `panelarr.mihon.v1` admin | `mihon-source` | draft |
| [metadata-plugin.md](metadata-plugin.md) | `panelarr.metadata.v1` plugins + `panelarr.meta.v1` service | `meta` | draft |
| [metadata-schema.md](metadata-schema.md) | Metadata entry schema: ProviderEntry, merged Entry, Person/Company/Tag, enums | `meta` | proposed |
| [jobs.md](jobs.md) | Shared jobs API shape for every admin (FEAT-0002) | each service's admin package | draft |
| [plugin-index.md](plugin-index.md) | Plugin index JSON | plugin kit ([Q-0017](../questions/README.md)) | draft |
| [server-api.md](server-api.md) | Browser REST API + SSE events | `server` | draft |
