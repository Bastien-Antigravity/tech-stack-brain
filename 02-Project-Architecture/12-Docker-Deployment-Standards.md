---
title: Docker & Container Deployment Standards
type: architecture
status: active
microservice: ecosystem-wide
tags:
  - '#zone/3-fleet'
  - '#service/ecosystem-wide'
  - '#state/active'
  - '#type/architecture'
---

# 🐳 Docker & Container Deployment Standards

This document defines the authoritative architecture, build guidelines, and operational principles for containerized microservices across the Bastien-Antigravity ecosystem.

---

## 1. Single Source of Truth for Fleet Orchestration

All multi-service compositions, production releases, and container networking topology are centrally managed within:
`docker-deployment/docker-compose.yaml`

- **Authoritative Orchestrator**: The Python-driven fleet manager (`docker-deployment/scripts/fleet.py` via `./fleet.sh` / `fleet.cmd`) is the single canonical entry point for container operations (`./fleet.sh docker`, `./fleet.sh production`, `./fleet.sh compile --docker`).
- **No Divergent Fleet Manifests**: Microservices must not create competing top-level multi-container compositions. Fragment compose files in individual repositories (if kept for isolated module development) must strictly conform to canonical ports and syntax.

---

## 2. Dockerfile Design & Standalone Buildability

Every microservice that runs containerized must provide a production-ready `Dockerfile` in its repository root satisfying these non-negotiable rules:

### A. Standalone Build Rule
Running `docker build -t <image> .` from the repository root **MUST** succeed without requiring external filesystem mounts or assuming parent directory access.

### B. Shared Library Resolution for Polyglot & CGO Directives
Because Go microservices rely on internal ecosystem modules (`microservice-toolbox`, `distributed-config`, `safe-socket`, `universal-logger`, `flexible-logger`) using `go.mod` replace directives, the multi-stage build stage must clone authoritative library versions from the active branch:

```dockerfile
# === BUILD STAGE ===
FROM golang:1.25-alpine AS builder

LABEL org.opencontainers.image.source="https://github.com/Bastien-Antigravity/<service-name>"

RUN apk add --no-cache git gcc musl-dev ca-certificates tzdata

WORKDIR /workspace

# Clone shared library modules for replace directives in builder stage
RUN git clone --depth 1 -b develop https://github.com/Bastien-Antigravity/microservice-toolbox.git /workspace/microservice-toolbox && \
    git clone --depth 1 -b develop https://github.com/Bastien-Antigravity/distributed-config.git /workspace/distributed-config && \
    git clone --depth 1 -b develop https://github.com/Bastien-Antigravity/safe-socket.git /workspace/safe-socket && \
    git clone --depth 1 -b develop https://github.com/Bastien-Antigravity/universal-logger.git /workspace/universal-logger && \
    git clone --depth 1 -b develop https://github.com/Bastien-Antigravity/flexible-logger.git /workspace/flexible-logger

WORKDIR /workspace/<service-name>
COPY . .

RUN go mod tidy && \
    CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /<service-name>-bin ./cmd/<service-name>

# === RUNTIME STAGE ===
FROM alpine:3.20
RUN apk add --no-cache ca-certificates tzdata
WORKDIR /<service-name>
COPY --from=builder /<service-name>-bin /<service-name>/<service-name>
ENTRYPOINT ["/<service-name>/<service-name>"]
```

### C. Host-Native Supervisor Exclusions
Processes designed strictly as native OS supervisors (specifically `watchdog-agent`) operate directly on host PIDs and host symlinks. They are managed natively under Mode 1 (`./fleet.sh local`) and are excluded from Docker fleet execution.

---

## 3. Network Architecture & Port Allocations

To prevent port collision across native host execution and Docker containers:

1. **Host Execution (`local`)**:
   Binds directly to `127.0.0.1`.
2. **Container Host Port Mapping (`docker`)**:
   Containers bind to host loopback alias `127.0.0.2` via `${HOST_IP:-127.0.0.1}` override or explicit isolated interface:
   ```yaml
   ports:
     - "${HOST_IP:-127.0.0.1}:${WB_PORT:-5000}:${WB_PORT:-5000}"
   ```
3. **Inter-Container Communication**:
   All services communicate over the named bridge network `teleremote-network` using service aliases (e.g. `http://config-server:3306`, `nats://nats-server:4222`, `postgresql://timescale-db:5432`).

### Canonical Port Registry:
| Service | Container Internal Ports | Protocol | Docker Host Port (`docker-compose`) |
| :--- | :--- | :--- | :--- |
| `web-interface` | `5000` | HTTP | `5000` |
| `tele-remote` | `1863` | gRPC | `1863` |
| `config-server` | `3306` (TCP), `3307` (gRPC), `3308` (REST) | SafeSocket / gRPC / REST | `3306` (TCP sync) |
| `notif-server` | `1026` (TCP), `1027` (gRPC), `1029` (REST) | SafeSocket / gRPC / REST | `1026`, `1027`, `1029` |
| `log-server` | `9020` (TCP), `9021` (gRPC) | SafeSocket / Tonic | `9020` (TCP log sink) |
| `nats-server` | `4222` (TCP), `8222` (HTTP) | NATS | `4222`, `8222` |
| `timescale-db` | `5432` | PostgreSQL | `5432` |
| `rag-engine` | `8090` (MCP), `8082` (Dash), `8091` (gRPC) | SSE / HTTP / gRPC | `8090`, `8082`, `8091` |

---

## 4. Zero Plaintext Secrets in Containers

1. **Production Slices**:
   Service configuration is mounted read-only from `docker-deployment/modes/docker/config/services/<service>.yaml`.
2. **Ciphertext Standard**:
   All passwords, API keys, and bot tokens must use `ENC(...)` ciphertext.
3. **Private Key Mounting**:
   Services decrypt secrets on-demand using the master RSA key mounted at runtime:
   ```yaml
   volumes:
     - ${BASTIEN_PRIVATE_KEY_PATH:-/etc/bastien/private.pem}:/etc/bastien/private.pem:ro
   ```
4. **Zero-Knowledge Web Interface**:
   Public-facing dashboards (`web-interface`) **MUST NOT** mount the master private key `/etc/bastien/private.pem`.
