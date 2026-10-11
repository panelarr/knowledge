# Modules

One folder per code repo ([ADR-0002](../decisions/ADR-0002-split-repositories.md)). All code repos are **public**, like this KB ([ADR-0020](../decisions/ADR-0020-public-kb-with-aliases.md)). Whether code repos may link KB IDs is open ([Q-0028](../questions/README.md)); until then they don't. Each module's `overview.md` has an **Implementation status** section that the keeper updates from REPORTs.

| Module | Lang | Role | Index |
|---|---|---|---|
| server | Go | Core *arr* app, plugin host, REST API | [server/](server/README.md) |
| web | TS | SPA/PWA reader and admin | [web/](web/README.md) |
| source-api | Go | Source contract, SDK, conformance, plugin kit | [source-api/](source-api/README.md) |
| meta | Go | Metadata service + plugin contract | [meta/](meta/README.md) |
| source-mihon | Go | Mihon stores, trust, orchestration | [source-mihon/](source-mihon/README.md) |
| mihon-source | Kotlin | Small tool: Mihon extensions over source-api | [mihon-source/](mihon-source/README.md) |
| source-local | Go | User's own files as a source | [source-local/](source-local/README.md) |
| deploy | YAML | Compose, Unraid, AIO | [deploy/](deploy/README.md) |

Metadata plugins (`meta-mangabaka`, `meta-anilist`, …) are documented under [meta](meta/overview.md) until their repo layout is decided ([Q-0017](../questions/README.md)).
