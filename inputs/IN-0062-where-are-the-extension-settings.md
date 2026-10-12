# IN-0062: where are the extension settings

- **Received:** 2026-10-12
- **From:** @aurimasniekis
- **Distilled into:** per-source settings UI pulled forward from GOAL-0017 (after FEAT-0012 R2)

---

<!-- Paste the owner's words below, verbatim and unedited. Number sections (§1, §2, ...) if it's long,
     so docs can cite "IN-0062 §2". Never edit this file after it is committed. Corrections become a new input. -->

"i dont see any extension settings? did the source-mihon not rexport settings from mihon-source?"

Keeper's finding: source-mihon does export them; both live sources declare the `settings` capability, and mihon-source returns a schema with x-order. The server's settings API (GOAL-0015 S4, `55cf9ed`) wasn't deployed yet (the running server was `d409c60`), and the web page for it was planned in GOAL-0017.
