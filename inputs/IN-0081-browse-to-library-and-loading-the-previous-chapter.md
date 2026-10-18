# IN-0081: Browse to library, and loading the previous chapter

- **Received:** 2026-10-18
- **From:** @aurimasniekis
- **Distilled into:** [FEAT-0012](../planning/features/FEAT-0012-reader-series-page-and-library-polish.md) R5 (browse → library, previous chapter)

---

<!-- Paste the owner's words below, verbatim and unedited. Number sections (§1, §2, ...) if it's long,
     so docs can cite "IN-0081 §2". Never edit this file after it is committed. Corrections become a new input. -->

"Another thing is to make transition from browse item to lirbary item if its added or on add to library move to library and etc. Another i can think of is make going from middle (lets say i am jump to 45 chapter and i scroll up) it shold be nicer way to load previous chapter"

Context (checked 2026-10-18, web `fd0b653`): a Browse card for a work already in the library opens the catalogue page, which shows an "In your library" link; after **Add to library** the page stays, with a toast and the same link. In the long strip, scrolling up within half a screen of the first loaded chapter's start loads the previous chapter above (`strip-viewer.tsx`), all at once.
