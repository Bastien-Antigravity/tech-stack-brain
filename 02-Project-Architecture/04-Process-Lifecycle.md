---
type: architecture
status: active
microservice: ecosystem-wide
title: "Process Lifecycle"
---

# 04 - Process Lifecycle

This document defines how services govern their own execution loops.

## Rules
- Services are managed via a gRPC `ProcessController`.
- **Standard Methods**: `Start()`, `Stop()`, `Restart()`.
- Graceful shutdown is mandatory. Use `context.WithTimeout` (Go) or `tokio::signal` (Rust) and listen for `SIGTERM`/`SIGINT` in the entry point.

See the [[05-Microservice-Map]] for the full list of services that must implement this logic.
