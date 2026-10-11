# Architecture

How Panelarr's pieces fit together across repos. Start with the [overview](overview.md).

| Doc | Holds | Status |
|---|---|---|
| [overview.md](overview.md) | Containers, responsibilities, key flow | proposed |
| [contracts-and-transport.md](contracts-and-transport.md) | Protobuf + gRPC between services; REST/OpenAPI for browser; where each contract lives | proposed |
| [plugins.md](plugins.md) | Plugin kinds, managed vs remote, index, lifecycle, discovery idea | proposed |
| [networking.md](networking.md) | Network profiles: per-source proxy, solver, VPN, rate limits | proposed |
| [search.md](search.md) | SearchIndex interface; DB full-text default; Typesense/Meilisearch | proposed |
| [domain-model.md](domain-model.md) | Work, SourceSeries, Chapter, ChapterFile, users, jobs | draft |
| [multi-user.md](multi-user.md) | Shared vs per-user, roles, grants, enforcement, auth | proposed |
| [storage-layout.md](storage-layout.md) | `/config`, `/data`, CBZ + ComicInfo naming, atomic writes | proposed |
| [trackers.md](trackers.md) | Tracker interface, built-in targets, sync behaviour | draft |
| [security.md](security.md) | Plugin and extension trust, isolation, secrets, web hardening | draft |
| [deployment.md](deployment.md) | Images, compose profiles, Unraid, AIO | proposed |
| [repo-standard.md](repo-standard.md) | Public GitHub repo standard: files, workflows, releases, quality | proposed |
