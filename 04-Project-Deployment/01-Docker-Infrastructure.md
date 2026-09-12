---
title: Docker Infrastructure
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# 📐 Docker Infrastructure

## Architectural Rule
The platform runs as a set of Docker containers orchestrated by `docker-compose`. Each service has its own `Dockerfile`. To ensure isolation and resilience, services MUST communicate through **Docker's internal DNS resolver** using container names/aliases (e.g., `postgresql://timescale-db:5432`) rather than static IPs.

## Motivation (Why?)
- **Environment Isolation**: Ensures identical behavior across development, sandbox, and production.
- **Docker Guard**: The `microservice-toolbox` uses a "Docker Guard" to detect the environment and automatically switch between local loopback (`127.0.0.1`) and internal DNS (`timescale-db`), ensuring seamless cross-environment mobility.

## Examples
### Infrastructure Services
| Service | Image | Default Port | Purpose |
|---|---|---|---|
| `timescale-db` | `timescale/timescaledb-ha:pg18` | 5432 | TimescaleDB for time-series storage |
| `nats-server` | `nats:2.12.6-alpine3.22` | 4222 | NATS messaging bus |

### Application Services
> [!IMPORTANT] DYNAMIC REGISTRY
> To ensure architectural consistency and avoid stale documentation, the AI Agent MUST consult the **[[05-Fleet-Operation/00-Repo-Control/service-registry.json|📡 Service Registry]]** for the latest port matrix, image names, and protocol definitions.

| Service | Source of Truth | Key Ports |
|---|---|---|
| **Core Fleet** | `service-registry.json` | 1862 (Config), 9021 (gRPC Log), 1863 (Tele) |
| **Data Pipeline** | `service-registry.json` | 5432 (DB), 4222 (NATS) |

AI Agents should use the following logic:
1.  Read `service-registry.json` to identify the target service's ports and archetype.
2.  Cross-reference with `inventory.json` for repository paths.
3.  Apply the corresponding `docker-compose.yaml` configuration.

## 🌐 Network Topology
- **The Standard**: All services reside on a shared, external bridge network named **`teleremote-network`**.
- **Service Discovery**: Use container names as hostnames (e.g., `http://log-server:9020`, `nats-server:4222`).
- **External Access**: Port mappings default to standard loopback `${HOST_IP:-127.0.0.1}` across macOS, Linux, and Windows. For production VPS deployments, `HOST_IP=0.0.0.0` is used.

## 🔑 Secrets Management (Zero-Knowledge Pattern)
The platform follows a **Sovereign Decryption** pattern to ensure end-to-end security of sensitive configuration:

1.  **Zero-Knowledge Config Server & Web Interface**: `config-server` and `web-interface` do NOT possess private keys. They distribute and display configuration blobs with secrets remaining strictly encrypted as `ENC(...)` and **cannot decrypt them**.
2.  **Private Service Decryption via Read-Only Volume Mounts**: Consumer microservices receive their RSA Private Key mounted read-only into `/etc/bastien/private.pem:ro`. Using volume mounts instead of environment variables prevents key material from leaking into `docker inspect` or container inspect metadata files.
3.  **On-Demand Decryption**: The `microservice-toolbox` preserves secrets as `ENC(...)` in configuration AST and memory snapshots. Decryption happens **strictly on-demand** inside the consumer microservice code via `appConfig.DecryptSecret(secret)` at point-of-use. Plaintext secrets exist only in volatile runtime variables and never touch disk, network transit, or central distributors.
4.  **Per-Service Private Keys**: Each microservice can have its own distinct RSA key pair (e.g. `tele-remote-private.pem`, `notif-server-private.pem`). Secrets encrypted for Service A cannot be decrypted by Service B even if both have private keys.

### Variable Roles & Key Discovery:
- `BASTIEN_PUBLIC_KEY`: Used to validate and encrypt configuration items.
- `BASTIEN_PRIVATE_KEY`: Contains the RSA Private Key content (PEM format) for local, in-service decryption.
- `BASTIEN_PRIVATE_KEY_PATH`: Path to the service's private key file.

> [!TIP] KEY RESOLUTION FALLBACK
> If `BASTIEN_PRIVATE_KEY` (content) is not provided, the system falls back to the following locations in order:
> 1.  Path specified in **`BASTIEN_PRIVATE_KEY_PATH`** environment variable (or `--key` flag).
> 2.  **`/etc/bastien/private.pem`** (Standard Production host path).
> 3.  **`docker-deployment/config/keys/private.pem`** (Self-contained repository fallback for zero-configuration multi-machine portability).
> 4.  **`./private.pem`** (Local/Sandbox development fallback).

## 🚦 Operational Readiness
- **Health Checks**: Every service must be monitored for readiness to ensure correct dependency sequencing. See **[[03-Health-Checks|📐 Health Checks]]** for implementation details.
