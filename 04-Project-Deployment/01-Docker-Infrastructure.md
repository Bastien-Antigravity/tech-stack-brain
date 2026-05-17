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
- **Service Discovery**: Use container names as hostnames (e.g., `http://log-server:9021`).
- **External Access**: Port exposure on the host is restricted. Only `web-interface` and `tele-remote` should expose ports to the host machine. Infrastructure services (DB, NATS) should only expose ports for debugging purposes, using local mappings (e.g., `127.0.0.2:5432:5432`).

## 🔑 Secrets Management (Zero-Knowledge Pattern)
The platform follows a **Sovereign Decryption** pattern to ensure end-to-end security of sensitive configuration:

1.  **Public Config Server**: The `config-server` only possesses the **RSA Public Key**. It serves encrypted configuration blobs (`ENC(...)`) to the fleet but **cannot decrypt them**.
2.  **Private Service Decryption**: Individual microservices (dockerized or standalone) receive the **RSA Private Key** via the `BASTIEN_PRIVATE_KEY` environment variable.
3.  **In-Memory Decryption**: The `microservice-toolbox` performs local, in-memory decryption of `ENC(...)` blocks during the configuration loading phase. This ensures plaintext secrets never touch the disk or the network in transit.

### Variable Roles:
- `BASTIEN_PUBLIC_KEY`: Used by the `config-server` to validate and serve configuration.
- `BASTIEN_PRIVATE_KEY`: **Mandatory for services.** Contains the RSA Private Key content (PEM format) for local decryption.

> [!TIP] KEY RESOLUTION FALLBACK
> If `BASTIEN_PRIVATE_KEY` (content) is not provided, the system falls back to the following locations in order:
> 1.  Path specified in **`BASTIEN_PRIVATE_KEY_PATH`** environment variable.
> 2.  **`/etc/bastien/private.pem`** (Standard Production path).
> 3.  **`./private.pem`** (Local/Sandbox development fallback).

## 🚦 Operational Readiness
- **Health Checks**: Every service must be monitored for readiness to ensure correct dependency sequencing. See **[[03-Health-Checks|📐 Health Checks]]** for implementation details.
