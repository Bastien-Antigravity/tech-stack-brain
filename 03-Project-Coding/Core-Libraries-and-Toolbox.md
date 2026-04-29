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
**Module**: `github.com/Bastien-Antigravity/microservice-toolbox/go` (v0.1.6)
**Languages**: Go, Rust, Python
**Role**: The standardized entry point for all microservice configuration and networking.

### Packages
| Package | Purpose |
|---|---|
| `config` | `LoadConfig(profile)`, CLI argument parsing, Docker Guard |
| `connectivity` | Network resolver, Docker detection |
| `lifecycle` | Graceful shutdown helpers |
| `network` | gRPC server builder |
| `serializers` | Cap'n Proto message serialization |

### Usage Pattern
```go
// Go
cfg, err := config.LoadConfig("standalone", nil)
addr, _ := cfg.GetListenAddr("my_service")
```
```rust
// Rust
let ac = microservice_toolbox::config::load_config("standalone")?;
let addr = ac.get_listen_addr("my_service")?;
```
```python
# Python
from microservice_toolbox.config import load_config
cfg = load_config("standalone")
addr = cfg.get_listen_addr("my_service")
```

### API Parity Rule
**Go is the source of truth.** When adding features to the toolbox, implement in Go first, then port to Rust and Python with identical behavior and matching method signatures.

---

## 2. universal-logger
**Module**: `github.com/Bastien-Antigravity/universal-logger` (v1.1.6)
**Languages**: Go, C++, Python, Rust, VBA (via CGO bridge)
**Role**: Standardized logging facade. Ensures microservices are decoupled from the underlying logging engine.

### Key Interfaces
- `interfaces.Logger` — The main logging interface with methods: `Debug`, `Info`, `Warning`, `Error`, `Critical`, `Stream`, `Logon`, `Logout`, `Trade`, `Schedule`, `Report`.
- `bootstrap.Init(Name, ConfigProfile, LoggerProfile, LogLevel, useLocalNotifier, existingConfig)` → Returns `(*config.DistConfig, interfaces.Logger)`.
- `bootstrap.InitWithOptions(BootstrapOptions{})` → Advanced entry point with dependency injection.

### Log Levels
`NotSet`, `Debug`, `Stream`, `Info`, `Logon`, `Logout`, `Trade`, `Schedule`, `Report`, `Warning`, `Error`, `Critical`

### Usage Pattern
```go
import "github.com/Bastien-Antigravity/universal-logger/src/bootstrap"

cfg, logger := bootstrap.Init("my-service", "standalone", "standard", "INFO", false, nil)
defer logger.Close()

logger.Info("Service started on %s", addr)
```

### Integration Note
- `flexible-logger` operates alongside `universal-logger` as the underlying routing engine.
- Language wrappers (C++, Python, Rust, VBA) communicate through the **CGO bridge** (`src/cgo_bridge/`), not Go directly.
- The Go function signature can change without breaking wrappers, as long as the CGO bridge remains stable.

---

## 3. distributed-config
**Module**: `github.com/Bastien-Antigravity/distributed-config` (v1.6.0)
**Language**: Go
**Role**: YAML-based configuration with environment variable expansion, capability mapping, and config-server synchronization.

### Key Types
- `Config` — Main config struct with `Common`, `Logger`, `Capabilities` fields.
- `Config.Capabilities` — `map[string]interface{}` of named service entries.
- `Config.GetCapability(name, target)` — Safely unmarshals a capability into a typed struct.
- `Config.Get(section, key)` — Returns a string value from config sections.

### Capability Pattern
```go
type DatabaseConfig struct {
    IP       string `json:"ip"`
    Port     string `json:"port"`
    User     string `json:"user"`
    Password string `json:"password"`
    DBName   string `json:"dbname"`
}

var dbCfg DatabaseConfig
cfg.GetCapability("timescale_db", &dbCfg)
```

---

## 4. safe-socket
**Module**: `github.com/Bastien-Antigravity/safe-socket` (v1.7.0)
**Languages**: Go, Python
**Role**: Lightweight Cap'n Proto binary transport for log message transmission between services and the `log-server`.

### Architecture
Uses the Facade pattern with transport profiles (TCP, Unix socket) and protocol schemas for serialized log entries.

---

## 5. flexible-logger
**Module**: `github.com/Bastien-Antigravity/flexible-logger` (v1.1.0)
**Status**: **Active** — Log processing engine and structured data router.
**Integration**: Functions alongside `universal-logger` as the underlying engine.
