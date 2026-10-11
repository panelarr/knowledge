# IN-0015: Answers: or-later, contact, Docker Hub, ports, store delegation, meta standalone

- **Received:** 2026-10-11
- **From:** @aurimasniekis
- **Distilled into:** ADR-0025 (annotation), Q-0005, Q-0006, Q-0013, Q-0031 answered, architecture/deployment.md, architecture/repo-standard.md, modules (meta, mihon-source, source-mihon), contracts/mihon-source-api.md, GOAL-0001, GOAL-0002

---

## §1 Answers

The keeper had listed: (1) GPL "v3 or later" (suggested) vs "v3 only"; (2) a contact address for the Code of Conduct; (3) Q-0013, is the `panelarr` Docker Hub org secured; (4) Q-0005, default ports; (5) Q-0031, should source-mihon delegate stores to mihon-source's store API; (6) Q-0006, meta as its own container or built into server.

1. yes
2. team@panelarr.app
3. yes
4. mihon-source should use like 8902, main app 8900, meta 8901
5. yes
6. yes it will be standalone service with library integration
