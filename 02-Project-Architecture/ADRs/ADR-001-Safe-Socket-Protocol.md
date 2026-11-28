---
microservice: ecosystem-wide
type: adr
status: accepted
date: 2026-04-15
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#service/obsidian-brain'
- '#state/accepted'
- '#type/adr'
- '#domain/networking'
- '#domain/architecture'
---
# 📜 ADR-001: Safe-Socket Custom TCP Protocol

## 1. Context and Problem Statement
The Bastien-Antigravity microservice ecosystem requires high-throughput, low-latency, and strictly partitioned communication between internal processes (like the `config-server` and `log-server`). Standard HTTP/REST introduces unacceptable parsing overhead and connection-tear-down delays.

## 2. Decision Drivers
- Extreme low latency.
- Persistent internal connections.
- Native identity verification (Handshakes) without TLS overhead internally.

## 3. Considered Options
- **Option 1:** Standard HTTP/REST.
- **Option 2:** gRPC / HTTP2.
- **Option 3:** Custom framed TCP wrapper (`safe-socket`).

## 4. Decision Outcome
Chosen option: **Option 3 (Custom framed TCP wrapper)**, because it allows us to build extremely resilient, long-lived connections optimized for our custom message framing, and natively support "profile" based handshakes upon connection.

### Current Hardened Implementation (2026-11 Update)
- **Single-Syscall & Zero-Alloc Framing**: `FramedTCPSocket.Write` combines the 4-byte BigEndian length prefix and payload into one write — using a stack `[512]byte` buffer (`0 allocs/op`) for frames `<= 508B` (including 0-byte heartbeats), `net.Buffers` (`writev`) scatter-gather for large cleartext TCP frames, and a coalesced write buffer for TLS records — closing the socket immediately if a partial write fails. `ReadMessage()` reads the 4-byte header into a stack `[4]byte` array.
- **Role-Segregated Public Facade**: `CreateClient` / `CreateClientWithConfig` (`ClientSocket`) and `CreateServer` / `CreateServerWithConfig` (`ServerSocket`) segregate client and server contracts cleanly while keeping `Create` backward compatible.
- **Unified TLS & TCP Optimizations**: `FramedTCPSocket.underlyingTCPConn()` unwraps `*tls.Conn` to apply `TCP_NODELAY`, `SO_KEEPALIVE`, and 4MB socket buffers uniformly across cleartext TCP and TLS connections.
- **Timeout Isolation & Reconnection Boundary**: See [[ADR-003-Safe-Socket-Handshake-Isolation-And-Hybrid-Timeouts]].

### Positive Consequences
- Zero dependencies on massive remote web frameworks.
- Immediate failure detection on broken pipes.
- Custom payload framing strictly controls payload sizes.

### Negative Consequences
- We must manually maintain the TCP transport layer library across Go, Rust, and Python.
- Lacks native load balancing out-of-the-box compared to HTTP.

---
*Linked Nodes:* [[safe-socket/README.md]], [[config-server/README.md]], [[log-server/README.md]]
