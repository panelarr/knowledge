# IN-0027: Gluetun VPN-as-proxy example in mihon-source docs

- **Received:** 2026-10-11
- **From:** @aurimasniekis
- **Distilled into:** GOAL-0005 (item 3), architecture/networking.md

---

## §1 Question

what about using something like vpn like openvpn or wireguard instead of proxy for mihon-source?

## §2 After the keeper's answer

The keeper answered from architecture/networking.md (a VPN is a container such as gluetun that exposes a proxy) and listed options: a proxy per source (current design), `network_mode: service:gluetun`, a userspace WireGuard-to-proxy tool, or mihon-source running the VPN itself (advised against).

u should record as example the glueton to use openvpn/wireguard for proxy as container in the docs of mihon-source
