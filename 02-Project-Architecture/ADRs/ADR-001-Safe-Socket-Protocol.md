---
type: adr
status: accepted
date: 2026-04-15
tags:
  - domain/networking
  - domain/architecture
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

### Positive Consequences
- Zero dependencies on massive remote web frameworks.
- Immediate failure detection on broken pipes.
- Custom payload framing strictly controls payload sizes.

### Negative Consequences
- We must manually maintain the TCP transport layer library across Go, Rust, and Python.
- Lacks native load balancing out-of-the-box compared to HTTP.

---
*Linked Nodes:* [[safe-socket/README.md]], [[config-server/README.md]], [[log-server/README.md]]
