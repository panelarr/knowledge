# IN-0057: sources of unselected languages listed, all on/off, extension list reload

- **Received:** 2026-10-12
- **From:** @aurimasniekis
- **Distilled into:** fixes for `panelarr-web` (FEAT-0009 follow-up)

---

<!-- Paste the owner's words below, verbatim and unedited. Number sections (§1, §2, ...) if it's long,
     so docs can cite "IN-0057 §2". Never edit this file after it is committed. Corrections become a new input. -->

"why sources list source of languages which are not selected in the source plugin extension list. (Also language selection should have button for easy `All on/off`. Bug 2: its not bug it fine to list all extension but maybe good to cache/reload on button"

Keeper's finding (live stack): source-mihon's `languages` is `[en]`. Of 43 sources, 2 (en) are usable; the other 41 were seen in an earlier sync and are kept as "Not available" (`unavailable_reason: language`), so Admin → Sources still lists them. The filtering itself works: they aren't used for search, matching or downloads.
