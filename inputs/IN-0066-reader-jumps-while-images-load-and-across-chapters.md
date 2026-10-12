# IN-0066: reader jumps while images load and across chapters

- **Received:** 2026-10-12
- **From:** @aurimasniekis
- **Distilled into:** a bug for `panelarr-web` (FEAT-0012 AC1); page sizes in source.v1 (a later idea) become relevant

---

<!-- Paste the owner's words below, verbatim and unedited. Number sections (§1, §2, ...) if it's long,
     so docs can cite "IN-0066 §2". Never edit this file after it is committed. Corrections become a new input. -->

"also the reader now jumps quite a lot when loading images, also not sure but looks like it jumps through chapters too"

Context: on the live stack with the reader that reads on into the next chapter and loads the previous one when scrolling up (web `647cb99`, live since redeploy #7).
