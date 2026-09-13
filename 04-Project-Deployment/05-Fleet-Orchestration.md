---
title: Fleet Orchestration Architecture
type: architecture
status: active
microservice: docker-deployment
tags:
- '#zone/3-fleet'
- '#service/docker-deployment'
- '#state/active'
- '#type/architecture'
---
# 🚀 Fleet Orchestration Architecture (`docker-deployment`)

## Architectural Purpose
The `docker-deployment` repository serves as the **Ecosystem Master Orchestrator** for the Bastien-Antigravity platform. It manages the full lifecycle of all microservices, infrastructure databases, compilation pipelines, cryptographic secret wizards, and deployment configurations across macOS, Linux, and Windows.

---

## 🏛️ Core Architectural Principles

### 1. One File, One Concern
Monolithic scripts are strictly prohibited. Each module is assigned a single, clear responsibility:
- **`scripts/fleet.py`**: Command-line argument parsing, strict subparser validation, and high-level routing.
- **`scripts/common.py`**: Shared cross-platform primitives (ANSI colors, port probing, key location, configuration extraction).
- **`scripts/operations.py`**: Cross-cutting utilities (compilation, container building, doctor diagnostics, secrets wizard).
- **`modes/local/run.py`**: Native mode lifecycle orchestrator.
- **`modes/local/infra.py`**: Database infrastructure detection (TimescaleDB & NATS) and local compose fallback.
- **`modes/local/health.py`**: Ecosystem readiness verification engine, HTTP/TCP probing, and failure diagnostics.
- **`modes/local/branch.py`**: Git branch auditing across active workspace repositories.
- **`modes/local/ide/setup_ide.py`**: Antigravity IDE configuration generator (`.vscode/tasks.json`).
- **`modes/local/ghcr/`**: GitHub Container Registry authentication and publishing routines.
- **`modes/docker/run.py`**: Containerized stack deployment bound to `127.0.0.2`.
- **`modes/production/run.py`**: VPS deployment bound to `0.0.0.0` with Watchtower.

### 2. Explicit, Typed CLI Parameters
- CLI commands are strict and unambiguous.
- Every command provides dedicated contextual help via `./fleet.sh <command> --help`.
- Unrecognized or deprecated subcommands (e.g. `start`) are strictly rejected with an explicit error and non-zero exit code (exit 2). Silent fallback launches are strictly forbidden.
- Zero third-party dependencies: Built strictly using Python 3 standard library (`argparse`, `urllib.request`, `socket`, `subprocess`, `pathlib`).

### 3. Sovereign Zero-Knowledge Secrets
- Cryptographic RSA keys are stored strictly outside all git repositories in `~/.bastien/keys/private.pem` with restricted POSIX permissions (`0600`).
- Configuration files and central servers (`config-server`, `web-interface`) never store plaintext secrets and cannot decrypt `ENC(...)` blocks.
- Containerized runtimes mount the private key read-only into `/etc/bastien/private.pem:ro`.

### 4. Dynamic Declarative Configuration
- Ports, IPs, and service URLs are resolved dynamically from `native.yaml` and environment variables.
- Hardcoded port numbers or IP bindings in code are strictly forbidden.

### 5. Mandatory Readiness Verification
- Starting native services always blocks until all TCP ports, HTTP endpoints, and process supervisor APIs confirm healthy status.
- Bypassing readiness verification is strictly prohibited.

---

## 🧭 Canonical Execution Modes

| Command | Target Interface | Supervisor | Backing Databases | Use Case |
|---|---|---|---|---|
| `./fleet.sh local` | `127.0.0.1` | `watchdog-agent` | Local Native or Docker Compose (`--infra=docker`) | Active local feature development and debugging on branch `develop` |
| `./fleet.sh docker` | `127.0.0.2` | Docker Engine | Containerized Compose (`modes/docker/`) | Integration testing in containerized isolation without host port fighting |
| `./fleet.sh production` *(or `prod`)* | `0.0.0.0` | Watchtower + Docker | Containerized Compose (`modes/production/`) | VPS production deployment with continuous GHCR image delivery |

---

## 📋 Complete CLI Command Reference

### Execution Modes
- `./fleet.sh local`: Start native stack supervised by `watchdog-agent`.
  - `--infra {native,docker}`: Specify database infrastructure (default: native).
  - `--timeout <SEC>`: Readiness timeout in seconds (default: 25).
- `./fleet.sh docker`: Start containerized stack on isolated loopback `127.0.0.2`.
  - `--build`: Build container images from local source before starting.
- `./fleet.sh production` (alias: `prod`): Start VPS stack on `0.0.0.0` with Watchtower.
  - `--build`: Build container images from local source before starting.

### Local Development Tools
- `./fleet.sh local ide-setup`: Configure Antigravity IDE (`.vscode/tasks.json` and workspace settings).
- `./fleet.sh local branch-check`: Verify all workspace repositories are checked out on `develop`.
- `./fleet.sh local ghcr-login`: Configure GitHub/GHCR authentication credentials.
- `./fleet.sh local ghcr-publish [SERVICE]`: Build and push container images to GHCR (supports `--force`).

### Lifecycle & Maintenance
- `./fleet.sh compile [native|docker|all]`: Incremental binary compilation & virtual environment setup (supports `--force`).
- `./fleet.sh rebuild`: Force clean rebuild of all native binaries and Docker container images.
- `./fleet.sh status`: Display real-time status of Docker containers, native PIDs, and listening ports (`--host-ip` optional).
- `./fleet.sh stop`: Terminate running services (`--scope {all,native,docker}`).
- `./fleet.sh doctor`: Pre-flight diagnostic check for required toolchains (Go, Rust, Python 3, Docker, Git).
- `./fleet.sh guide`: Interactive manual installation guide for TimescaleDB and NATS.
- `./fleet.sh secrets [action]`: Manage keys and secrets (`encrypt --token <TOKEN>`, `rotate-db`, `set-db-password`, `check-keys`).
- `./fleet.sh clone`: Clone missing ecosystem repositories from GitHub (`--all`, `--ssh`).

---

## 🤖 RAG / AI Agent Guidelines
When an AI agent interacts with or modifies `docker-deployment`:
1. **Never introduce third-party pip dependencies**: Keep all code standard-library only.
2. **Never store keys inside repositories**: Always resolve keys via `~/.bastien/keys/` or `BASTIEN_PRIVATE_KEY_PATH`.
3. **Never hardcode ports**: Use `get_service_port` and `get_service_ip` from `scripts/common.py`.
4. **Never create monolithic files**: Keep infrastructure logic in `modes/local/infra.py`, health logic in `modes/local/health.py`, and lifecycle coordination in `modes/local/run.py`.
5. **Always maintain test compatibility**: Verify changes against `sandbox-testing/02-Scenarios/go`.
