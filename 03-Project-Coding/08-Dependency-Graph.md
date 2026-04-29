---
title: "Dependency Graph"
type: architecture
status: active
microservice: ecosystem-wide
---

# 🔗 Dependency Graph

## Go Module Dependencies

```
                    ┌──────────────────┐
                    │  config-server   │
                    │     (Go)         │
                    └───────┬──────────┘
                            │
            ┌───────────────┼───────────────────┐
            ▼               ▼                   ▼
   ┌────────────────┐  ┌──────────────┐  ┌──────────────────┐
   │  safe-socket   │  │ distributed- │  │ microservice-    │
   │     (Go)       │  │   config     │  │   toolbox (Go)   │
   └────────────────┘  └──────┬───────┘  └────────┬─────────┘
                              │                   │
                              └─────────┬─────────┘
                                        │
                                        ▼
                               ┌────────────────┐
   ┌────────────────┐◄─────────│ universal-     │
   │ flexible-      │          │   logger       │
   │   logger       │          └───────┬────────┘
   └────────────────┘                  │
                                       ▼
                              ┌────────────────┐
                              │ notif-server   │
                              └────────────────┘
```

## Rust Dependencies
- `log-server` → `microservice-toolbox` (Rust crate)
- Optional `unilog` feature flag for UniLogger integration

## Python Dependencies
- `microservice-toolbox` (Python package) → `PyYAML`, `argparse`

## Go Workspace (`go.work`)
```
go 1.25.4
use (
    ./config-server
    ./distributed-config
    ./flexible-logger
    ./microservice-toolbox/go
    ./notif-server
    ./safe-socket
    ./universal-logger
)
```
All 7 Go modules are bound into a single workspace. Local changes propagate instantly.

## Polyglot Component Map

| Component | Go | Rust | Python |
|-----------|-----|------|--------|
| Config Loader | `microservice-toolbox/go` | `microservice-toolbox/rust` | `microservice-toolbox/python` |
| Log Engine | `flexible-logger` | N/A (uses CGO) | N/A (uses CGO) |
| Log Facade | `universal-logger` | `unilog-rs` (binding) | `unilog-py` (binding) |
| Socket | `safe-socket` | N/A | `safe-socket/python` |
| Config Service | `distributed-config` | N/A | N/A |
| Serialization | Protobuf + JSON | Cap'n Proto + Protobuf | MessagePack |

## Polyglot Parity Gaps

| Area             | Gap                                                               |
| ---------------- | ----------------------------------------------------------------- |
| CLI flags        | Go and Python accept `specificFlags`, Rust does NOT               |
| gRPC overrides   | Go separates into dedicated function; Rust/Python merge into CLI  |
| Missing config   | Go/Rust silently skip; Python raises `FileNotFoundError`          |
| Logger bootstrap | Rust auto-bootstraps UniLogger via feature flag; Go/Python do not |
