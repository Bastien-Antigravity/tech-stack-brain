---
title: "Docker Infrastructure"
type: architecture
status: active
microservice: ecosystem-wide
---

# 📐 Docker Infrastructure

## Architectural Rule
The platform runs as a set of Docker containers orchestrated by `docker-compose`. Each service has its own `Dockerfile`. Services communicate through **Docker's internal DNS resolver** (e.g., `postgresql://timescale-db:5432`).

## Motivation (Why?)
- Isolate environments and ensure uniform production deployments.
- The `Docker Guard` in `microservice-toolbox` ensures CLI network overrides are ignored inside containers, preserving container-to-container DNS resolution.

## Examples
### Infrastructure Services
| Service | Image | Default Port | Purpose |
|---|---|---|---|
| `timescale-db` | `timescale/timescaledb-ha:pg18` | 5432 | TimescaleDB for time-series storage |
| `nats-server` | `nats:2.12.6-alpine3.22` | 4222 | NATS messaging bus |

### Application Services
| Service | Image | Default Port | gRPC Port |
|---|---|---|---|
| `config-server` | `ghcr.io/bastien-antigravity/config-server` | 1862 | — |
| `log-server` | `ghcr.io/bastien-antigravity/log-server` | 9020 | 9021 |
