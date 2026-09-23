---
title: Health Checks
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# 📐 Health Checks & Operational Readiness

## Architectural Rule
Every service in the Bastien-Antigravity fleet MUST provide a non-destructive mechanism to verify its operational readiness. This allows the orchestrator (Docker Compose) to manage service dependencies accurately and restart stalled containers.

## Motivation (Why?)
- **Zero-Downtime Reboots**: Ensures a container is only considered "Live" when it can actually serve requests.
- **Dependency Sequencing**: Prevents application services from starting before their core dependencies (Database, Messaging) are fully ready to handle traffic.

## 🛠️ Implementation Guide

### 1. Infrastructure Services
Use the native CLI tools already present in the official base images.

| Service | Protocol | Docker Health Check Command |
|---|---|---|
| **TimescaleDB** | Postgres | `pg_isready -U ${DB_USER:-dbuser} -d ${DB_NAME:-maindb}` |
| **NATS Server** | HTTP | `wget -q --spider http://localhost:8222/healthz \|\| exit 1` |

### 2. Application Services (Go/Rust/Python)
To keep images lean (avoiding `EXPOSE` and extra probe tools), we prioritize simple **TCP Readiness** probing using `nc` (netcat), which is available in the base Alpine images.

#### 🔌 Simple TCP Check (Recommended)
If the service is a TCP server (e.g., SafeSocket, gRPC, or custom TCP), check if the port is bound and accepting connections.
```yaml
healthcheck:
  test: ["CMD", "nc", "-z", "localhost", "3306"]
  interval: 10s
  timeout: 5s
  retries: 3
```

#### 🌐 HTTP Probing (Web Services)
For services exposing an HTTP interface (like the `web-interface`), use `wget`.
```yaml
healthcheck:
  test: ["CMD", "wget", "-q", "--spider", "http://localhost:5000/health"]
```

## 🚦 Integration with Docker Compose
Always use `service_healthy` instead of `service_started` for critical dependencies to ensure robust startup sequences.

```yaml
services:
  data-ingestor:
    depends_on:
      timescale-db:
        condition: service_healthy
      nats-server:
        condition: service_healthy
```

## ⚡ Host-Side Ecosystem Readiness Engine (`modes/local/health.py`)
In addition to container-level Docker health checks, the native execution orchestrator implements a **Multi-Tier Host Readiness Probing Engine**:

1. **TCP Socket Verification**: Probes all microservice listening ports (`is_port_listening`) using non-blocking socket handshakes.
2. **HTTP Endpoint Probing**: Dynamically probes HTTP services (`/health`, `/api/v1/status`, `/`) via standard library HTTP requests. Any response `< 500` confirms the web server process is actively responding.
3. **Supervisor REST Status Polling**: Queries the `watchdog-agent` REST API (`http://127.0.0.1:9095/api/v1/status`) to ensure all child processes are in the `running: true` state and healthy.
4. **Mandatory Readiness Gate**: Startup sequences block until all services pass health verification or a timeout is reached. Bypassing readiness verification is strictly prohibited.
5. **Actionable Failure Diagnostics**: If startup times out, the engine prints a comprehensive diagnosis:
   - Unopened ports
   - Unresponsive HTTP endpoints
   - Terminated/crashed child processes
   - The last 15 lines of `watchdog.log`

