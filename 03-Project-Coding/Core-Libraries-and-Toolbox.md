---
microservice: obsidian-brain
type: architecture
status: active
tags:
- '#state/active'
- null
- '#type/architecture'
---

# Shared Libraries Reference

## Library Hierarchy
The Bastien-Antigravity platform uses a layered library architecture. Understanding the dependency chain is critical for any modifications.

```
microservice-toolbox  (config, CLI, networking primitives)
    └── distributed-config  (YAML loading, env expansion, config-server sync)
        └── safe-socket  (Cap'n Proto transport)

universal-logger  (logging facade + bootstrap)
    └── flexible-logger  (underlying log routing engine)
    └── distributed-config  (for config-based log level)
```

---
## 1. microservice-toolbox
**Module**: `github.com/Bastien-Antigravity/microservice-toolbox/go` (v1.2.2)
**Languages**: Go, Rust, Python, C++, VBA
**Role**: The standardized entry point for all microservice configuration, resilience, and networking.

### Packages
| Package | Purpose |
|---|---|
| `config` | `LoadConfig(profile)`, CLI argument parsing, Docker Guard |
| `conn_manager` | **ConnectNonBlocking**, background reconnection, strategy-based connection pools |
| `connectivity` | Network resolver, Docker detection |
| `lifecycle` | Graceful shutdown helpers |
| `network` | gRPC server builder |
| `serializers` | Cap'n Proto / Protobuf message serialization |

### Usage Pattern
```go
// Go - Non-blocking reconnection
nm := conn_manager.NewNetworkManager()
conn := nm.ConnectNonBlocking(&ip, &port, nil, "tcp-hello")
```

### API Parity Rule
**Go is the source of truth.** When adding features to the toolbox, implement in Go first, then port to all supported languages with identical behavior and matching method signatures.

---

## 2. universal-logger
**Module**: `github.com/Bastien-Antigravity/universal-logger` (v1.2.0)
**Languages**: Go, C++, Python, Rust, VBA (via CGO bridge)
**Role**: Standardized logging facade. Ensures microservices are decoupled from the underlying logging engine.

### Key Interfaces
- `interfaces.Logger` — The main logging interface with methods: `Debug`, `Info`, `Warning`, `Error`, `Critical`, `Stream`, `Logon`, `Logout`, `Trade`, `Schedule`, `Report`.
- `bootstrap.Init(Name, ConfigProfile, LoggerProfile, LogLevel, useLocalNotifier, existingConfig)` → Returns `(*config.DistConfig, interfaces.Logger)`.
- `bootstrap.InitWithOptions(BootstrapOptions{})` → **Preferred** advanced entry point with dependency injection and metadata support.

### Log Levels
`NotSet`, `Debug`, `Stream`, `Info`, `Logon`, `Logout`, `Trade`, `Schedule`, `Report`, `Warning`, `Error`, `Critical`

### Usage Pattern
```go
import "github.com/Bastien-Antigravity/universal-logger/src/bootstrap"

// Modern Init using Options
distConfig, logger := bootstrap.InitWithOptions(bootstrap.BootstrapOptions{
    Name:          "my-service",
    ConfigProfile: "standalone",
    LoggerProfile: "standard",
    Metadata:      map[string]string{"env": "prod"},
})
defer logger.Close()
```

---

## 3. distributed-config
**Module**: `github.com/Bastien-Antigravity/distributed-config` (v1.6.0)
**Language**: Go
**Role**: YAML-based configuration with environment variable expansion, capability mapping, and config-server synchronization. Supports native RSA decryption via `ENC(...)`.

---

## 4. safe-socket
**Module**: `github.com/Bastien-Antigravity/safe-socket` (v1.9.0)
**Languages**: Go, Python, C API
**Role**: Universal high-performance transport (TCP/UDP/SHM) with profile-based protocols and **Infinite Wait** resilience.

### Architecture
Uses the Facade pattern with transport profiles. **v1.9.0+** introduces `SetIdleTimeout(0)` for persistent background streams, allowing for zero-timeout blocking reads while maintaining active **Zombie Detection** through adaptive heartbeats.
