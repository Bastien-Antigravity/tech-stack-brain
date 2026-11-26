---
type: architecture
status: active
microservice: ecosystem-wide
title: Process Lifecycle
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# 04 - Process Lifecycle

This document defines how services govern their own execution loops.

## Rules
- **External Process/Container Supervision**: Process start, stop, restart, and circuit-breaker pause/resume are managed per host by `watchdog-agent` (and Docker Engine in containerized deployments), coordinated across machines over NATS (`<prefix>.watchdog.node.<hostname>.*`) and controlled via `tele-remote` (`TeleClient` `:1863`) or OpenMFE (`:9095`).
- **Deterministic Graceful Shutdown (`lifecycle.Manager`)**: Every microservice wires its listeners and background workers into `microservice-toolbox` `lifecycle.Manager`, trapping `SIGTERM`/`SIGINT` to stop ingress, drain in-flight work with bounded timeouts, and await worker exit in LIFO order.

See the [[05-Microservice-Map]] for the full list of services that must implement this logic.
