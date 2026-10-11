# IN-0003: Architecture round 1: answers and follow-ups

- **Received:** 2026-10-11
- **From:** @aurimasniekis (answers to the keeper's questions, plus messages sent during planning)
- **Distilled into:** ADR-0001…ADR-0011, meta/, architecture/plugins.md, architecture/search.md, architecture/repo-standard.md, modules/source-local/
- **Redacted on migration (IN-0004):** confidential terms replaced by their `[ALIAS]` or `[redacted]`; links to where extensions can be obtained removed.

---

## §1 Answers to keeper questions (round A)

- **KB format?** "[redacted: pointed to another knowledge base as a reference], how it uses special cases of `/cc` command for commits and etc"
- **Default database for the Go core?** "would be great to have options like sqlite/postgres/mysql(optional but if possible and not too difficult)"
- **Multi-user content sharing?** "Shared store, per-user libraries (Recommended)"
- **Mihon extension service language?** "Kotlin/JVM (Recommended)"

## §2 Answers to keeper questions (round B)

- **Keeper commits like the reference KB?** "Yes, same as [redacted] (Recommended)"
- **Code layout?** "Fully split (meta separate too)"
- **Name of the Mihon extension service?** "we will have more than just mihon extensions, so lets do general api of sources and one implemention as mihon"

## §3 Follow-up messages

1. "also not differect copy of [redacted] knowledge-base but just reference of what we can do too"
2. "The main code libs will be hosted on github open source, so full github workflows/pr/code quality/tests/builds/releases be defined for each repo, docker registry will be panelarr/x and each repo should have docs and etc, this knowledge is private for me to keep and will not be public on github, so each other repo should not be mentioning this KB anywhere"
3. "also source api will be `golang` and `source-mihon` will be golang lib but `mihon-soure` will be external api based on kotlin/jvm"
4. "like mihon source is just small tool to interact with mihon extensions directly via api"
5. "also another source could be users own manga and etc files i forgot name of file extenson"

## §4 Plan review feedback

"i think sources could be like plugins, like by default they dont come and u need to add it urself, same for metadata search api. Oh I also forgot that i would like to use some kind of proper search engine not opensearch but something lighter to search by different titles, descriptions, character info if available and etc. i do remember something like typesense. also this should be optional and possible to configure if u want to use it (like each own hoster can decide what they want to run)"

## §5 Approval

The author approved the keeper's architecture v0 plan (2026-10-11).

## §6 During execution

"maybe for inter service we an use grpc or etc? also the mihon one could be standalone tool with our source api grpc or openapi options"

## §7 During execution (idea)

"maybe good idea is some kind of plugin detection with mdns when running on same docker compose project? (thinking ideas)"

## §8 During execution (idea)

"maybe for go we can use something like GoReleaser"
