# IN-0049: meta shown unavailable when the provider is down

- **Received:** 2026-10-12
- **From:** @aurimasniekis
- **Distilled into:** a fix for `panelarr-server` (error mapping); modules/deploy/overview.md

---

<!-- Paste the owner's words below, verbatim and unedited. Number sections (§1, §2, ...) if it's long,
     so docs can cite "IN-0049 §2". Never edit this file after it is committed. Corrections become a new input. -->

"it seams the meta is not accessible but 8901 works? https://i.imgur.com/SiN9PLI.png"

Screenshot (described by the keeper): Panelarr web, the metadata checklist. "A metadata provider has entries" failed; "What to do: No metadata provider has entries yet. Run a sync of a provider; a first full import can take a while." Provider row: `mangabaka`, badge **down**, 0 entries, "Start sync". Error box: "The sync didn't start / the metadata service didn't answer: unavailable / meta_unavailable · HTTP 503 · Request ID: 8c61fa1359294552".

Keeper's finding: meta was up and healthy. The `meta-mangabaka` plugin container was stopped on purpose in this stack (disk), and meta logged "plugin not reachable … no such host". The server reported meta's answer about its plugin as meta itself being unavailable.
