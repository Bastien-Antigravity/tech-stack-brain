---
title: "Architecture Patterns"
type: architecture
status: active
microservice: ecosystem-wide
---

# 📐 Architecture Patterns

## 1. Facade Pattern (Universal Entry Point)
Every library exposes a **root-level facade file** that re-exports its internals. Consumers never import internal packages directly.

| Repo | Facade File | Entry Point |
|------|-------------|-------------|
| `safe-socket` | `safe_socket.go` | `safesocket.Create(profile, addr, ip, type, auto)` |
| `distributed-config` | `distributed_config.go` | `distributed_config.New(profile)` |
| `universal-logger` | `src/bootstrap/unilog.go` | `bootstrap.Init(name, config, logger, level, notif, existingCfg)` |
| `microservice-toolbox` | `go/pkg/config/loader.go` | `config.LoadConfig(profile, flags)` |

## 2. Factory + Profile Pattern
Both `safe-socket` and `flexible-logger` use factory dispatching via profile name strings:
- `safe-socket`: profiles `"tcp"`, `"tcp-hello"`, `"udp"`, `"udp-hello"`, `"shm"`, `"shm-hello"`
- `flexible-logger`: profiles `"standard"`, `"devel"`, `"audit"`, `"cloud"`, `"high_perf"`, `"minimal"`, `"no_lock"`, `"notif_logger"`

Profile names are always **lowercase string constants** matched via `switch` statements.

## 3. Strategy Pattern (Config Loading)
`distributed-config` uses the Strategy pattern for config profiles:
```go
type ConfigStrategy interface {
    Name() string
    Load(cfg *core.Config) error
    Sync(cfg *core.Config) error
    GetHandler() *network.ConfigProtoHandler
}
```
Profiles: `production`, `preprod`, `test`, `standalone`.

## 4. Layered Configuration (4-Phase Priority)
The `microservice-toolbox` config loader follows **identical 4-phase layering** across Go, Rust, and Python:
1. **Base File** (`{profile}.yaml`)
2. **Dev Override** — If `standalone` or `test`, re-applies file as hard override
3. **CLI Flags** — Highest priority
4. **gRPC Overrides** — Separate gRPC host/port flags

## 5. Atomic State Management (Lock-Free Reads)
`config-server/src/store/store.go` uses Go's `atomic.Pointer` for a CAS loop:
- Reads: Lock-free via `atomic.Load()`
- Writes: Retry loop using `CompareAndSwap()`
- Immutability: Returned maps must be treated as immutable

## 6. Bootstrap Composition (Dependency Injection)
`universal-logger/src/bootstrap/unilog.go`:
- `Init()` = simple entry point (string params)
- `InitWithOptions(BootstrapOptions{})` = advanced entry point with optional `ExistingConfig` injection

## 7. Type Alias Re-Export
Facade files re-export all necessary types so consumers never need internal imports:
```go
type Socket = interfaces.Socket
type Level = logger_models.Level
type NotifMessage = logger_models.NotifMessage
```

## 8. Go Workspace Monorepo
Root `go.work` binds 7 Go modules: `config-server`, `distributed-config`, `flexible-logger`, `microservice-toolbox/go`, `notif-server`, `safe-socket`, `universal-logger`.
