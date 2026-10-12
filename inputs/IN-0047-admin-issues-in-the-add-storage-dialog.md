# IN-0047: admin issues in the add storage dialog

- **Received:** 2026-10-12
- **From:** @aurimasniekis
- **Distilled into:** a fix for `panelarr-web` (web, after GOAL-0011); modules/web/overview.md

---

<!-- Paste the owner's words below, verbatim and unedited. Number sections (§1, §2, ...) if it's long,
     so docs can cite "IN-0047 §2". Never edit this file after it is committed. Corrections become a new input. -->

"i see some admin issues https://imgur.com/2XOEeCQ"

Screenshot (described by the keeper): Panelarr web, Admin → Storage, the "Add storage" dialog. The ID field (label, input, hint "Lowercase; it can't change.") and the Kind field (label, select "Directory on the server") sit side by side but don't line up: the Kind label and select are a few pixels lower than the ID label and input. Below: Name, Directory (placeholder `/data/library`, hint "An absolute path the server can write to."), Cancel and Add.
