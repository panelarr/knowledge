# IN-0014: Answers: Armeria, licences, pre-release merging, KB refs in repos

- **Received:** 2026-10-11
- **From:** @aurimasniekis
- **Distilled into:** ADR-0024, ADR-0025, Q-0010, Q-0012, Q-0020 (JVM side), Q-0028, architecture/repo-standard.md, GOAL-0001, GOAL-0002

---

## §1 Request

what questions u have for me?

## §2 Answers to the keeper's questions

1. *Q-0020 (JVM side): mihon-source is built on Armeria. Accept it?* Options: accept Armeria (recommended); keep as assumption; switch to grpc-kotlin + Ktor.
   → **"Accept Armeria (Recommended)"**
2. *Q-0012: licence for the public code repos?* Options: GPL-3.0 apps + Apache-2.0 SDKs; AGPL-3.0 apps + Apache-2.0 SDKs; Apache-2.0 everywhere; MIT everywhere.
   → **"GPL-3.0 apps, Apache-2.0 SDKs"**
3. *Q-0010: sessions commit on their own branches, never push or merge. How do you want to merge?* Options: you merge per slice; sessions push + open PRs; merge at the end of a goal.
   → Wrote: "before initial releases the agent can merge himself"
4. *Q-0028: may the public code repos reference the KB (link docs, cite ADR/Q IDs in docs and commits)?* Options: links in docs only; yes, IDs and links; no, keep repos standalone.
   → **"Yes, IDs and links"**
