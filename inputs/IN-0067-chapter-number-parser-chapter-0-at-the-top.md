# IN-0067: chapter number parser, chapter 0 at the top

- **Received:** 2026-10-12
- **From:** @aurimasniekis
- **Distilled into:** a server parsing fix (volumes); the owner's saved order reset to newest first

---

<!-- Paste the owner's words below, verbatim and unedited. Number sections (§1, §2, ...) if it's long,
     so docs can cite "IN-0067 §2". Never edit this file after it is committed. Corrections become a new input. -->

"we should also implement better chapter number parser because now it shows 0 chapters at the top look at the solo leveling library item"

Keeper's finding (live stack): the numbers are parsed correctly (0, 0.1, 1, 1.1, 1.2 … 194.1 … 202; 261 chapters, all distinct), and the API's newest-first order is right. Chapter 0 was at the top because the owner's saved preference was `chapters.order: asc` (most likely set during the keeper's live tests). The keeper reset it to `desc`, keeping the rest of the preferences. Separately, volumes aren't parsed: every chapter has `volume: null` although titles say "Vol. 1 …", and titles keep noise such as "Vol. 1 Volume 1 Chapter 1: …" and "OFFICIAL TRANSLATION".
