# IN-0079: Retry failed page images per source

- **Received:** 2026-10-18
- **From:** @aurimasniekis
- **Distilled into:** [FEAT-0016](../planning/features/FEAT-0016-automatic-retries-for-failed-page-images.md) (proposed)

---

<!-- Paste the owner's words below, verbatim and unedited. Number sections (§1, §2, ...) if it's long,
     so docs can cite "IN-0079 §2". Never edit this file after it is committed. Corrections become a new input. -->

"one thing i can think for source like SITE_A to try reload the failed image in extension settings or etc"

Context: right after the mobile batch and History/Updates were verified. SITE_A is a single-site extension (alias). In the reader today, a page that fails shows "Page N didn't load" with a manual "Try again" (web `page-image.tsx`); nothing retries a failed image automatically.
