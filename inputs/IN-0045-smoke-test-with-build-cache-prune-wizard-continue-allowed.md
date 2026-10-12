# IN-0045: Smoke test with build-cache prune; wizard continue allowed

- **Received:** 2026-10-12
- **From:** @aurimasniekis
- **Distilled into:** agents/sessions.md, modules/web/overview.md

---

## §1 Answers

1. *panelarr-meta wants to build and smoke-test the full compose stack once (~4–6 GB of Docker disk, 9.3 GB free, 3.3 GB reclaimable build cache).* Options: yes; yes and prune build cache first; not now.
   → **"Yes, and prune build cache first"**
2. *In the web setup wizard, can the admin continue once meta is connected even if its provider has no data yet?* Options: allow continue with warning; block until meta has data.
   → **"Allow continue with warning"**
