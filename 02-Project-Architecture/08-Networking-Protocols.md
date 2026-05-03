# Networking & Communications: gRPC, NATS, Cap'n Proto, WebSockets

## Networking Stack
Our microservices communicate through four primary channels: gRPC for control, NATS for async messaging, Cap'n Proto for log transport, and WebSockets for metrics.

### 1. gRPC Control Service
- **Role**: Every microservice exposes a native `ProcessController` proto service for management.
- **Methods**: Must support `Start()`, `Stop()`, and `Restart()`.
- **Location**: `src/grpc_control/` (Go) or `proto/` (Rust).
- **Separation**: Decouple the gRPC socket server scaffolding (`grpc_service.go`) from the underlying execution definitions (`grpc_control.go`).
- **Health**: Always implement `grpc_health_v1` for service health checks.
- **Toolbox**: Use `microservice-toolbox` gRPC server builder for Rust services. Use `cfg.GetGRPCListenAddr(name)` for address resolution.

### 2. NATS Asynchronous Bus
- **Role**: Primary asynchronous ingestion bus for high-throughput data streams.
- **Pattern**: Pub/Sub for market data, order books, and events.
- **Handling**: Use asynchronous subscribers to avoid blocking the network thread.
- **Container**: Uses the `nats:2.12.6-alpine3.22` image with monitoring on port 8222.

### 3. Cap'n Proto Transport (safe-socket)
- **Role**: Binary serialization for log messages between services and `log-server`.
- **Library**: `github.com/Bastien-Antigravity/safe-socket` provides the transport layer.
- **Schemas**: Defined in `capnp/` directories within relevant services.
- **Server**: `log-server` (Rust) listens for Cap'n Proto messages on TCP.

### 4. Metric WebSockets (WSPublisher)
- **Role**: Outbound metrics (performance, health status, real-time data) are streamed via non-blocking concurrent WebSocket publishers.
- **Implementation**: `WSPublisher` is a standard component found in most Go microservices.
- **Performance**: Metrics must be buffered and sent asynchronously to avoid performance hits on the main processing engine.

### 5. The Shadow Port Protocol
To avoid the complexity of a global port registry, all microservices MUST follow the **Shadow Port** convention:
- **Rule**: The gRPC control port is always `Base TCP Port + 1`.
- **Implementation**: This logic is hardcoded into the `microservice-toolbox` address resolution layer. 
- **Auto-Discovery**: AI agents must assume `Port + 1` for gRPC traffic unless explicitly overridden in `distributed-config`.

### 6. Heartbeat Safety Ratio (2.5x)
To prevent "Zombie Connections" (where a process thinks a socket is alive but it's actually stuck), we enforce the **2.5x Safety Ratio**:
- **Rule**: The Heartbeat interval MUST be at least 2.5x faster than the Idle Timeout (Deadline).
- **Standard**: If `IdleTimeout = 500ms`, then `HeartbeatInterval = 200ms`.
- **Goal**: Proactively prove the connection is "Dead" and trigger reconnection before the application hits a blocking timeout.

### 6. Health & Status
- **Standard**: Always implement `grpc_health_v1` for service health checks.
- **Status Reporting**: Report serving status as `SERVING` only when all internal sub-processes are successfully initialized.
- **Container Health**: Docker health checks use `pg_isready` (DB), HTTP monitoring (NATS), or gRPC health (application services).
