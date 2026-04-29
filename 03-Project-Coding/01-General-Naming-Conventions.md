---
title: "General Naming Conventions"
type: architecture
status: active
microservice: ecosystem-wide
---

# 📐 General Naming Conventions

## Architectural Rule
- **Interfaces (Python)**: MUST start with `I` (e.g., `ILogger`, `IDataProcessor`).
- **Interfaces (Go)**: Follow idiomatic Go — NO `I`-prefix. Use descriptive nouns (e.g., `Logger`, `Socket`, `ConfigStrategy`).
- **Interfaces (Rust)**: Use traits with descriptive names (e.g., `Logger`).
- **Models**: prefix with `M` (e.g., `MMarketData`, `MOrderBook`).
- **Functions/Methods**: Go: `PascalCase` (exported) / `camelCase` (unexported). Rust: `snake_case`. Python: `snake_case` with `_underscore_prefix` for private.

## 🛠 Constructor Conventions

| Language | Pattern | Example |
|----------|---------|---------|
| **Go** | `New{Type}` | `NewStandardLogger()`, `NewResolver()` |
| **Rust** | `pub fn new()` | `AppConfig::new()`, `LogServer::new()` |
| **Python** | `ClassName()` | `FinvizScraper()`, `AAACalculator()` |

> [!NOTE]
> In **Go**, use `New{Type}With{Dependency}` for more specific factory methods (e.g., `LoadConfigWithLogger`).


## File Naming

| Language | Convention | Example |
|----------|-----------|---------|
| Go | `snake_case.go` | `request_handler.go`, `socket_factory.go` |
| Rust | `snake_case.rs` | `loader.rs`, `args.rs`, `mod.rs` |
| Python | `snake_case.py` | `loader.py`, `args.py`, `test_logger.py` |
| Scripts | `PascalCase-Hyphenated.py` | `Build-Wrapper.py`, `Hide-Empty-Folders.py` |

## 🔗 Ecosystem Import Aliasing
To ensure parity across our polyglot environment, all `Bastien-Antigravity` repositories MUST be aliased using a standardized set of short, descriptive names.

### Go
```go
safe_socket          "github.com/Bastien-Antigravity/safe-socket"
safe_socket_ifaces   "github.com/Bastien-Antigravity/safe-socket/src/interfaces"
distributed_config   "github.com/Bastien-Antigravity/distributed-config/src/schemas"
toolbox_config       "github.com/Bastien-Antigravity/microservice-toolbox/go/pkg/config"
flexible_logger      "github.com/Bastien-Antigravity/flexible-logger/src/interfaces"
unilog               "github.com/Bastien-Antigravity/universal-logger/src/bootstrap"
```

### Rust
```rust
use safe_socket as safe_socket;
use microservice_toolbox as toolbox;
use distributed_config as distributed_config;
use universal_logger as unilog;
```

### Python
```python
import safe_socket as safe_socket
import microservice_toolbox as toolbox
import distributed_config as distributed_config
import universal_logger as unilog
```

### VBA
Class Modules and Global Objects MUST use the PascalCase version of the repository name:
- `Safe_Socket` (from safe-socket)
- `Microservice_Toolbox` (from microservice-toolbox)
- `Distributed_Config` (from distributed-config)
- `UniLog` (from universal-logger)

```vba
' Example usage
Dim socketManager As New Safe_Socket.SocketManager
```

## Python Stdlib Aliasing
Use `moduleAction` or `moduleLocation` aliasing to distinguish standard actions from local variables:
```python
from os.path import join as osPathJoin
from os.path import exists as osPathExists
from requests import get as requestsGet
from time import sleep as timeSleep
from argparse import ArgumentParser as argparseArgumentParser
```

## Variable Naming Conventions

| Pattern | Convention | Example |
|---------|-----------|---------|
| Configuration objects | `ac` or `dConf` | `ac := &AppConfig{}` |
| Loggers | `logger`, `flexLogger`, `unilog` | `flexLogger = profiles.NewStandardLogger()` |
| Sockets | `sock`, `serverSock`, `conn` | `serverSock, err := factory.Create(...)` |
| Error handling | Always `err` | `if err != nil { return nil, err }` |

## Motivation (Why?)
- Unified readability across polyglot microservices.
- Instant recognition of types and abstractions when switching between Go, Rust, and Python.

## Examples
- `Logger` (Go Interface)
- `ILogger` (Python Interface)
- `MMarketData` (Model)
- `app_logger` (Variable)
- `NewServer()` (Go Constructor)
