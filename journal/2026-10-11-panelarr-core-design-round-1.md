# 2026-10-11: Panelarr core design round 1

- **Participants:** @aurimasniekis, panelarr-knowledge
- **Inputs:** IN-0037

## Discussed

- The owner asked to start designing the main app: library, reader, downloader (IN-0037 §1). The keeper surveyed the existing drafts (domain model, multi-user, storage layout, server/web overviews, server API sketch, trackers) and asked four framing questions.
- Answers (§2): one library entry per actual work, anchored on meta, with sources matched by title and alternative titles, per-source chapter tabs, and unified chapters filled across sources by availability, quality or health; source-mihon from day one; first slice add → read → download, multi-user; shadcn/ui + Tailwind.
- Sent during the round (§3): fully responsive UI (native-app feel on mobile, good desktop) and reader settings per source.

## Changed in the KB

- [ADR-0028](../decisions/ADR-0028-library-entry-per-work.md) (accepted, the owner's words).
- [Domain model](../architecture/domain-model.md): the Work is created from a meta Entry.
- [Web](../modules/web/overview.md): UI kit, look and feel, Work page with source tabs and unified chapters, per-source reader settings.
- Q-0008 answered.

## Decided

- ADR-0028; Q-0008 (shadcn/ui + Tailwind); the first slice and source-mihon from day one (recorded here and in the next design docs).

## New open questions

- Q-0038: a Work without meta (meta is optional by principle).
- Q-0039: what makes a chapter variant better (quality, health).
- Q-0040: match confidence and the confirm/fix UX.

## Next

- Keeper: draft feature docs for the first slice (accounts, add and match, unified chapters and updates, reader, downloads), refine the server API contract, and brief source-mihon, server and web sessions.
