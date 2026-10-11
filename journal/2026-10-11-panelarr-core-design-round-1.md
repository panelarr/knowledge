# 2026-10-11: Panelarr core design round 1

- **Participants:** @aurimasniekis, panelarr-knowledge
- **Inputs:** IN-0037, IN-0038, IN-0039, IN-0040, IN-0041, IN-0042

## Discussed

- The owner asked to start designing the main app: library, reader, downloader (IN-0037 §1). The keeper surveyed the existing drafts (domain model, multi-user, storage layout, server/web overviews, server API sketch, trackers) and asked four framing questions.
- Answers (§2): one library entry per actual work, anchored on meta, with sources matched by title and alternative titles, per-source chapter tabs, and unified chapters filled across sources by availability, quality or health; source-mihon from day one; first slice add → read → download, multi-user; shadcn/ui + Tailwind.
- Sent during the round (§3): fully responsive UI (native-app feel on mobile, good desktop) and reader settings per source.

- The keeper flagged that ADR-0028 conflicts with meta being optional (Q-0038). The owner chose **meta required for the library** (IN-0038), and the mihon-source session to build source-mihon.

- Sent during the round (IN-0039): most of meta's and mihon-source's admin should be visible inside Panelarr when connected.

## Changed in the KB

- [ADR-0028](../decisions/ADR-0028-library-entry-per-work.md) (accepted, the owner's words).
- [Domain model](../architecture/domain-model.md): the Work is created from a meta Entry.
- [Web](../modules/web/overview.md): UI kit, look and feel, Work page with source tabs and unified chapters, per-source reader settings.
- Q-0008 answered.

- [ADR-0029](../decisions/ADR-0029-meta-required.md) (accepted; annotates ADR-0011); AGENTS.md, principles, deployment, meta and server docs updated; Q-0038 answered.

- [GOAL-0009](../agents/goals/GOAL-0009-source-api-and-source-mihon-v0.md) (`proposed`): source-api (protos move there, Go SDK, conformance) + source-mihon (pass-through to mihon-source) for the mihon-source session.
- Web and server docs: connected-service admin built into Panelarr (IN-0039).

- First-slice features FEAT-0003–0007 drafted. The owner (IN-0042) added multiple storage endpoints for downloads (FEAT-0007, storage layout, Q-0041) and whole-platform backup and restore ([FEAT-0008](../planning/features/FEAT-0008-backup-and-restore-for-the-whole-platform.md), Q-0042); "everything else is fine". The frontend stays a separate repo with a public, versioned server API (IN-0041).

## Decided

- ADR-0028; Q-0008 (shadcn/ui + Tailwind); the first slice and source-mihon from day one (recorded here and in the next design docs).

## New open questions

- Q-0038: a Work without meta (meta is optional by principle).
- Q-0039: what makes a chapter variant better (quality, health).
- Q-0040: match confidence and the confirm/fix UX.

## Next

- Keeper: feature docs FEAT-0003–0007 drafted (`proposed`); next, the server API contract and the server/web briefs. GOAL-0009 dispatched (IN-0040).
