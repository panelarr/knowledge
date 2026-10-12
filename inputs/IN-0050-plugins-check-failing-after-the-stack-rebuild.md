# IN-0050: plugins check failing after the stack rebuild

- **Received:** 2026-10-12
- **From:** @aurimasniekis
- **Distilled into:** a fix for `panelarr-server` (recheck down plugins sooner)

---

<!-- Paste the owner's words below, verbatim and unedited. Number sections (§1, §2, ...) if it's long,
     so docs can cite "IN-0050 §2". Never edit this file after it is committed. Corrections become a new input. -->

"now

plugins
optional
0 ms
Failing
plugins down: source-mihon (listing sources failed: mihon-source at http://mihon-source:8902 can't be reached: unavailable: dial tcp 172.19.0.3:8902: connect: connection refused)"

Keeper's finding: seen during the stack rebuild. The server restarted at 05:12:50 and its first plugin sync ran at 05:13:02, one second before the recreated mihon-source was listening. source-mihon wasn't recreated, so it passed the refusal on. The server marked source-mihon down and only rechecked on its 5-minute `plugins.sync` schedule; it went back to ok at 05:18:01 by itself.
