# IN-0037: Panelarr core design round 1: library model, sources, first slice, UI kit

- **Received:** 2026-10-11
- **From:** @aurimasniekis
- **Distilled into:** ADR-0028, Q-0008 answered, Q-0038, Q-0039, Q-0040, architecture/domain-model.md, modules/web/overview.md, journal 2026-10-11-panelarr-core-design-round-1

---

## §1 Request

maybe we can already start working on `panelarr` (library/reader/downloader) design itself?

## §2 Answers to the keeper's questions

1. *How should someone add a series to their library?* Options: both, meta-first default (recommended); meta-first only; source-first only.
   → Wrote: "the idea u search by name and it uses meta to find actual item, then it should search based on configured sources, like all apps do entry per source not per actual item, so my goal is to have an entry per actual meta library item and try to match all source items by names like item name can be different in every source so if it doesnt find by main name it can try look it up by alternative names, so item page would show tabs of all sources chapters and try to make on unified chapters, where gaps would be filled up from other sources if missing or better quality or health"
2. *How should the main app talk to Mihon sources in the first version?* Options: straight to mihon-source (recommended); via source-mihon from day one.
   → **"Via source-mihon from day one"**
3. *What should the first runnable slice be?* Options: add → read → download, multi-user (recommended); same single-user first; local files first.
   → **"Add → read → download, multi-user (Recommended)"**
4. *UI for the main web app (Q-0008)?* Options: shadcn/ui + Tailwind (recommended); Mantine; plain CSS like the admins.
   → **"shadcn/ui + Tailwind (Recommended)"**

## §3 Sent during the round

the ui should be fully responsive, like full mobile native app look on mobiles and good look on desktop, per source zoom levels and etc (in reader)
