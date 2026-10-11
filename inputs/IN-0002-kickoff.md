# IN-0002: Kickoff: Panelarr idea and module split

- **Received:** 2026-10-11
- **From:** @aurimasniekis
- **Distilled into:** product/vision.md, architecture/overview.md, ADR-0002, ADR-0005, ADR-0006, research/
- **Redacted on migration (IN-0004):** confidential terms replaced by their `[ALIAS]`; links to where extensions can be obtained removed.

---

Your a new project "Panelarr" knowledge base agent. My goal is to develop a `arr` styled project for reading/curating/managing/downloading panel style manga/manwha/manhua/comics like suwayomi/tachiyomi
  and etc. You will be working with other sessions to provide/record knowledge like other code folders and etc. There will be several modules for this project, one is library manager/reader so it would be `vite, react, tanstack/{router,query,virtual,pacer,store}` SPA compatible to run on web and mobile (with purpose to be added as pwa or icon where app would be browser). One project will provide an mihon extensions as api like using [EXTREPO] extensions as a service so to interact with providers for acuiring downloading and etc. with supportive tools like flaresolver/proxies/vpn support for each source individually if required and etc. main library/downloader/meta info gathered will be written in golang, and mihon service probably java/kotlin u will decide which better. The whole service is targering to be self hosted app like via docker, or apps for like unraid and etc like other `arr` projects like sonarr/radarr (but we dont follow their design or anything just idea for media management gathered and etc) For now lets define a full architecture. I wish this mihon wrapper to be able to work standalone outside the whole library, metadata gathered too like for metadata we can consume multiple sources like mangabaka dumps, also provide ability to integrate any kind of trackers to library/ready and etc

some sources for mihon extension running and etc suwayomi is good source of reference as this whole idea came from suwayomi but their limited ability to support multiple users and share same content if added to their own lib imagien u have to run now 3 instances for 3 different people.

(link removed: [EXTREPO] repository)
https://github.com/Suwayomi/Suwayomi-Server
https://mangabaka.org/data/database
