# IN-0068: web app buggy on mobile, reader jumps and flickers

- **Received:** 2026-10-18
- **From:** @aurimasniekis
- **Distilled into:** fixes for `panelarr-web` (real iOS Safari testing), the compose stack (mihon-source /tmp) via `panelarr-meta`; a durable mihon-source fix

---

<!-- Paste the owner's words below, verbatim and unedited. Number sections (§1, §2, ...) if it's long,
     so docs can cite "IN-0068 §2". Never edit this file after it is committed. Corrections become a new input. -->

"The web app itself is pretty buggy and doesnt work that great on mobile, maybe u need to run in mobile emulator or etc [Image #1] [Image #2] [Image #3][Image #5]. The reader jumps arounds and flickers panels impossible to read, jumps back and forth and etc"

Screenshots (described by the keeper):
- Image #1: unrelated to Panelarr (left out).
- Images #2 and #3 (iPhone, Safari): a catalogue entry page (Solo Leveling). The top third of the screen is empty black above the app header ("Panelarr"), then Back / "Refresh from providers", the cover, title, alternative titles, type and status, author and artist; bottom navigation Library / Browse / Downloads / More.
- Image #5 (iPhone): the reader stuck on a black screen with a spinner and "Opening the chapter…".

Keeper's findings on the live stack (2026-10-18): the server logs 502s on GET /chapters/{id}/pages for some chapters; the problem is `source_failed`: mihon-source fails with "UnsatisfiedLinkError: /tmp/zstd-kmp….tmp: failed to map segment from shared object" when an extension's HTTP client loads the zstd native library: the compose stack mounts mihon-source's /tmp as tmpfs, which Docker mounts noexec. The web app shows "Opening the chapter…" forever instead of the error.
