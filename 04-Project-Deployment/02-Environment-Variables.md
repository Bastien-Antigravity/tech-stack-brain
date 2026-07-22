---
title: Environment Variables
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# 📐 Environment Variables

## Architectural Rule
Production secrets, connectivity parameters, and deployment tags MUST be injected via environment variables. YAML configuration files utilize the `${VAR_NAME}` syntax for dynamic expansion at runtime by the `microservice-toolbox`.

## Motivation (Why?)
- **Security**: Ensures sensitive credentials (DB passwords, API keys) never touch the source code.
- **Environment Agnostic**: The same Docker image can shift from `develop` to `staging` to `production` simply by swapping the environment context.

## 🏷️ Standard Naming Conventions
To maintain fleet-wide consistency, the following prefixes and variables are mandated:

### 1. Connectivity Overrides (`*_IP`, `*_PORT`)
Used to manage the transition between internal container DNS and host-side loopback mappings.

| Service | Host/IP Variable | Main Port | gRPC Sync | gRPC Mgmt | REST Mgmt |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Log Server** | `LS_IP` | `LS_PORT` | `LS_GRPC_PORT` | - | - |
| **Config Server** | `CF_IP` | `CF_PORT` | `CF_GRPC_PORT` | - | `CF_REST_PORT` |
| **Notif Server** | `NT_IP` | `NT_PORT` | `NT_GRPC_PORT` | `NT_GRPC_MGMT_PORT` | `NT_REST_PORT` |
| **Tele-Remote** | `TR_IP` | `TR_PORT` | - | - | - |
| **TimescaleDB** | `DB_IP` | `DB_PORT` | - | - | - |
| **Scheduler** | `SC_IP` | `SC_PORT` | `SC_GRPC_PORT` | - | - |

### 2. Deployment Control
- `TAG`: Defines the Docker image version (e.g., `develop`, `latest`, or `v1.2.3`).
- `ENV_PROD`: Boolean flag used by services to enable production-only optimizations or safety gates.

### 3. Security & Secrets
- `BASTIEN_PRIVATE_KEY`: **Mandatory**. The RSA private key used to decrypt `ENC(...)` blocks in YAML files in-memory.
- `GITHUB_TOKEN`: Used by the Fleet Manager for remote synchronization and GitHub API audits.

## 📁 Environment File Hierarchy
Deployment roots (like `docker-deployment`) manage environment variables through structured files:
- `.env.develop`: Standard variables for the development integration environment.
- `.env.main`: Variables pinned for production/stable releases.
- `.env.local` (Ignored): Developer-specific overrides for local testing.

## 🚦 Implementation Pattern
In `docker-compose.yaml`:
```yaml
environment:
  - DB_PASSWORD=${DB_PASSWORD:-dbuser}
  - BASTIEN_PRIVATE_KEY=${BASTIEN_PRIVATE_KEY}
```
