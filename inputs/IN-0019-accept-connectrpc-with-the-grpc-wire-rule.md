# IN-0019: Accept ConnectRPC with the gRPC wire rule

- **Received:** 2026-10-11
- **From:** @aurimasniekis
- **Distilled into:** ADR-0026, Q-0020, architecture/contracts-and-transport.md, contracts/metadata-plugin.md, GOAL-0001, GOAL-0002

---

## §1 Question

why should i not accept ConnectRPC Q20 ?

## §2 Decision

The keeper listed the costs (two Go stacks because go-plugin needs grpc-go; vanguard less proven than grpc-gateway; Connect being a Buf project; raw speed) and suggested accepting ConnectRPC with a wire rule: standard gRPC is the canonical wire for remote plugins; REST/JSON follows the google.api.http paths; the Connect protocol is optional.

okay lets do it
