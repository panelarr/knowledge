# Modules

One folder per code repo ([ADR-0002](../decisions/ADR-0002-split-repositories.md)). All code repos are **public**, like this KB ([ADR-0020](../decisions/ADR-0020-public-kb-with-aliases.md)). Code repos may cite KB IDs and link KB docs (Q-0028, IN-0014). Each module's `overview.md` has an **Implementation status** section that the keeper updates from REPORTs.

| Module | Lang | Role | Index |
|---|---|---|---|
| server | Go | Core *arr* app, plugin host, REST API | [server/](server/README.md) |
| web | TS | SPA/PWA reader and admin | [web/](web/README.md) |
| source-api | Go | Source contract, SDK, conformance, plugin kit | [source-api/](source-api/README.md) |
| meta | Go | Metadata service (Seerr-style browse/search) + plugin contract and SDK | [meta/](meta/README.md) |
| source-mihon | Go | Mihon stores, trust, orchestration | [source-mihon/](source-mihon/README.md) |
| mihon-source | Kotlin | Mihon extensions over source-api, minimal admin, stores | [mihon-source/](mihon-source/README.md) |
| meta-mangabaka | Go | Metadata plugin: MangaBaka dump + API | [meta-mangabaka/](meta-mangabaka/README.md) |
| source-local | Go | User's own files as a source | [source-local/](source-local/README.md) |
| deploy | YAML | Compose, Unraid, AIO | [deploy/](deploy/README.md) |

Metadata plugins get one repo each (Q-0017, IN-0009). [meta-mangabaka](meta-mangabaka/README.md) is the first; the others are listed under [meta](meta/overview.md) until they start.
