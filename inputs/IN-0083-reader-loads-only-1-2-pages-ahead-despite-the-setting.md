# IN-0083: Reader loads only 1-2 pages ahead despite the setting

- **Received:** 2026-10-22
- **From:** @aurimasniekis
- **Distilled into:** a reader fix for `panelarr-web` ([FEAT-0012](../planning/features/FEAT-0012-reader-series-page-and-library-polish.md))

---

<!-- Paste the owner's words below, verbatim and unedited. Number sections (§1, §2, ...) if it's long,
     so docs can cite "IN-0083 §2". Never edit this file after it is committed. Corrections become a new input. -->

"i think web reader doesnt preload images like set in the settings i discovered that it only preloads like 1 maybe 2 images forward even when my settings is 16"

Context (keeper, checked in web `2271320`): the paged reader honours "Pages to load ahead" (`reader-screen.tsx`), but the long strip skips it ("a long strip loads its own") and uses a fixed `AHEAD = 2` past the first page not yet loaded (`strip-viewer.tsx`, since `647cb99`). So in a long strip the setting has no effect.
