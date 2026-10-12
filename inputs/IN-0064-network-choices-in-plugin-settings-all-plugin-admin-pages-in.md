# IN-0064: network choices in plugin settings; all plugin admin pages in Panelarr

- **Received:** 2026-10-12
- **From:** @aurimasniekis
- **Distilled into:** [FEAT-0013](../planning/features/FEAT-0013-connected-services-admin-inside-panelarr.md) (accepted); FEAT-0010 / GOAL-0017

---

<!-- Paste the owner's words below, verbatim and unedited. Number sections (§1, §2, ...) if it's long,
     so docs can cite "IN-0064 §2". Never edit this file after it is committed. Corrections become a new input. -->

Answers to the keeper's two questions (2026-10-12):

1. Network settings for mihon-source and meta: "like Panelarr's Network page it defines profiles/proxies/resolvers and in plugin it becomes available for its settings so like on mihon-source setting i can choose resolver from Panelarr itself"
2. Should the rest of mihon-source's and meta's admin pages also live inside Panelarr's admin (IN-0039)? "Yes, all of it" (the keeper's option: mihon-source stores, extensions, sources and health checks, jobs; meta providers and syncs, jobs, duplicates review, search engine; each a section of that plugin's page; their API keys and clients stay in their own admin).
