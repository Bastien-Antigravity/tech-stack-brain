---
microservice: ecosystem-wide
type: adr
status: accepted
date: 2026-11-27
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#service/safe-socket'
- '#service/obsidian-brain'
- '#state/accepted'
- '#type/adr'
- '#domain/networking'
- '#domain/architecture'
---
# 📜 ADR-003: Safe-Socket Two-Phase Handshake Timeout Isolation, Hybrid Timeouts & Reconnection Boundary

## 1. Context and Problem Statement
Production microservices (`config-server`, `notif-server`, `log-server`) accept persistent connections carrying a Cap'n Proto `HelloMsg` identity handshake (`tcp-hello` / `tls-hello`), while keeping healthy streams alive for long idle windows (`10m` local, `3m` Docker). Two failure modes emerged when a single timeout and bidirectional heartbeat model was shared across handshake and runtime phases:

1. **Slow-Loris Handshake Stall**: Go servers (`config-server`, `notif-server`, and raw `safe-socket` servers) execute `proto.WaitInitiation(conn)` synchronously inside `SocketServer.Accept()` before spawning `go handleConnection(conn)`. Applying the `10m` runtime `IdleTimeout` before `WaitInitiation` allowed any peer that sent a partial header (or 0 bytes without closing) to stall the accept loop for 10 minutes instead of failing fast. By contrast, `log-server` (Rust) already enforces a tight handshake timeout (`5s`) inside its per-connection task and drops invalid/incomplete handshakes immediately so clients reconnect cleanly.
2. **Bidirectional Heartbeat Buffer Stalls & Nested Reconnects**: Earlier defaults (`200ms`/`500ms` deadlines + bidirectional heartbeats + an internal backoff loop inside `SocketClient.Open()`) caused spurious timeouts, server-to-client heartbeat frames filling kernel buffers on unidirectional producer clients, and multi-minute nested retry loops competing with `microservice-toolbox/conn_manager`.

## 2. Decision Drivers
- Protect `SocketServer.Accept()` against Slow-Loris and stalled handshake peers (`<= 200ms`/`500ms`), failing fast and closing the socket so legitimate peers reconnect cleanly.
- Maintain long-lived idle connections (`10m` local / `3m` Docker) once peer identity is verified.
- Prevent server-outbound heartbeat traffic storms on unidirectional producer streams.
- Keep `SocketClient.Open()` single-attempt and fail-fast so `conn_manager` remains the single owner of backoff and `AppConfig` live-sync self-healing.
- Eliminate hot-path heap allocations for small frames (`<= 508B`, including heartbeats) and avoid extra payload copies for large TCP frames.

## 3. Decision Outcome

### A. Two-Phase Server Connection Timeout Lifecycle
In `SocketServer.Accept()` (`safe-socket/src/facade/socket_server.go`):
1. **Phase 1 (Pre-Handshake)**: Immediately enforce `handshakeTimeout` (`200ms` local, `500ms` remote, `100ms` SHM, or explicit `Config.HandshakeTimeout`) on `conn` before calling `proto.WaitInitiation(conn)`.
   - If the peer disconnects cleanly (`io.EOF` / `io.ErrUnexpectedEOF`), log at `DEBUG`, close the socket, and continue `Accept()`.
   - If the peer stalls past `handshakeTimeout`, sends an incomplete frame, or sends an invalid/corrupted Cap'n Proto payload, close the socket immediately and return the error so the caller (`config-server` / `notif-server` accept loop or caller) rejects it cleanly and the client reconnects with a fresh `HelloMsg`.
2. **Phase 2 (Post-Handshake)**: Only after `WaitInitiation(conn)` succeeds, call `conn.SetIdleTimeout(idleTimeout)` (`10m` local, `3m` Docker, or configured `Deadline`) before handing `conn` to the per-connection handler goroutine (`go handleConnection(conn)`).
   - Microservice connection handlers MUST verify `identity := safesocket.GetIdentity(conn)` immediately on entry and close the connection if missing or malformed.

### B. Unified Hybrid Timeout Matrix & Client-Driven Unilateral Heartbeats
- `ResolveHybridTimeouts` (`safe-socket/src/models/hybrid_timeout.go`) is the sole default resolver for both `Create*` and `CreateHybrid`:
  - **Local TCP/TLS**: `60s` client (`24s` heartbeat at `IdleTimeout / 2.5`), `10m` server (`0` outbound heartbeat).
  - **Docker TCP/TLS**: `30s` client (`12s` heartbeat), `3m` server (`0` outbound heartbeat).
  - **UDP**: `5s` idle timeout, no heartbeat ticker.
  - **SHM**: `0` infinite wait (`DisableTimeout: true`).
- Infinite wait is explicitly honored whenever `DisableTimeout: true`, `Deadline < 0`, or `SetIdleTimeout(0)` is requested, and explicit per-operation `SetReadDeadline` / `SetWriteDeadline` values are never overwritten by automatic activity refreshes.
- `HeartbeatConnection` is client-driven (`disabled: interval <= 0`): server connections default to `HeartbeatInterval = 0` and never spawn outbound heartbeat tickers on `SetIdleTimeout(...)`.

### C. Fail-Fast Dial Boundary & Hot-Path Framing
- `SocketClient.Open()` performs a single bounded dial + optional `HelloProtocol.Initiate` attempt and closes partial sockets on failure. All reconnection backoff and 3-failure `AppConfig` live-sync resolution live in `microservice-toolbox/go/pkg/conn_manager`.
- `FramedTCPSocket.Write` uses a stack `[512]byte` buffer (`0 B/op`, single write syscall) for payloads `<= 508B` (including 0-byte heartbeats), `net.Buffers` (`writev`) scatter-gather I/O for large cleartext TCP frames, and a single coalesced write for large TLS records; `ReadMessage()` reads the 4-byte length prefix into a stack `[4]byte` array.

## 4. Consequences
- **Positive**: Slow-Loris / partial-packet clients can no longer wedge `Accept()` for 10 minutes; write-only clients cannot suffer server heartbeat buffer backpressure; dial failures surface immediately to `conn_manager`; small frames achieve zero heap allocation on write.
- **Note for AI Agents**: Never move `conn.SetIdleTimeout(idleTimeout)` above `proto.WaitInitiation(conn)` in `SocketServer.Accept()`, and never re-introduce retry loops inside `SocketClient.Open()`.

---
*Linked Nodes:* [[ADR-001-Safe-Socket-Protocol]], [[FEAT-004-Identity-Handshake]], [[FEAT-003-Deadline-Management]], [[FEAT-007-Reconnection-Strategy]], [[FEAT-004-Connection-Resilience]]
