---
title: General Naming Conventions
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# 📐 General Naming Conventions

## Architectural Rule

### Interfaces
- **Python/Go/Rust**: MUST NOT use an `I`-prefix. Use descriptive nouns (e.g., `Logger`, `DataProcessor`, `Socket`).
- **C++**: Abstract base classes follow `PascalCase` without prefix.
- **VBA**: Interface-like Class Modules use `PascalCase` nouns.

### Functions & Methods
| Language | Exported/Public | Private/Unexported |
| :--- | :--- | :--- |
| **Go** | `PascalCase` | `camelCase` |
| **Rust** | `snake_case` | `snake_case` |
| **Python** | `snake_case` | `_snake_case` |
| **C++** | `PascalCase` (Parity Rule) | `snake_case_` (member) |
| **VBA** | `PascalCase` (Parity Rule) | `Private m_camelCase` |

> [!NOTE]
> **C++ & VBA: Parity Rule** — All public methods MUST use `PascalCase` to maintain semantic identity with the Go reference implementation (e.g., `GetListenAddr` in Go → `GetListenAddr()` in C++ → `GetListenAddr` in VBA).

## 🛠 Constructor Conventions

| Language | Pattern | Example |
|----------|---------|---------| 
| **Go** | `New{Type}` / `New{Type}With{Dep}` | `NewStandardLogger()`, `NewResolver()` |
| **Rust** | `pub fn new()` | `AppConfig::new()`, `LogServer::new()` |
| **Python** | `ClassName()` | `FinvizScraper()`, `AppConfig()` |
| **C++** | Free function `LoadConfig(...)` | `LoadConfig("standalone")` |
| **VBA** | `Class_Initialize` / `LoadConfig` Sub | `ac.LoadConfig "standalone"` |

> [!NOTE]
> In **Go**, use `New{Type}With{Dependency}` for factory methods requiring explicit dependencies (e.g., `LoadConfigWithLogger`).

## File Naming

| Language | Convention | Example |
|----------|-----------|---------| 
| Go | `snake_case.go` | `request_handler.go`, `socket_factory.go` |
| Rust | `snake_case.rs` | `loader.rs`, `args.rs`, `mod.rs` |
| Python | `snake_case.py` | `loader.py`, `args.py`, `test_logger.py` |
| C++ | `PascalCase.hpp` / `.cpp` | `AppConfig.hpp`, `NetworkManager.cpp` |
| VBA | `PascalCase.cls` / `.bas` | `AppConfig.cls`, `DistConf.bas` |
| Scripts | `PascalCase-Hyphenated.py` | `Build-Wrapper.py`, `Hide-Empty-Folders.py` |

## 🔗 Ecosystem Import Aliasing
All `Bastien-Antigravity` repositories MUST be aliased using standardized descriptive names across all languages to ensure polyglot readability.

### Go
```go
safe_socket        "github.com/Bastien-Antigravity/safe-socket"
safe_socket_ifaces "github.com/Bastien-Antigravity/safe-socket/src/interfaces"
distributed_config "github.com/Bastien-Antigravity/distributed-config/src/schemas"
toolbox_config     "github.com/Bastien-Antigravity/microservice-toolbox/go/pkg/config"
flexible_logger    "github.com/Bastien-Antigravity/flexible-logger/src/interfaces"
unilog             "github.com/Bastien-Antigravity/universal-logger/src/bootstrap"
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
Class Modules and Global Objects MUST use the `PascalCase` version of the repository name:
- `Safe_Socket` (from safe-socket)
- `Microservice_Toolbox` (from microservice-toolbox)
- `Distributed_Config` (from distributed-config)
- `UniLog` (from universal-logger)

```vba
' Example usage
Dim socketManager As New Safe_Socket.SocketManager
```

## Python Stdlib Aliasing
Use `moduleAction` or `moduleLocation` aliasing to distinguish standard imports from local variables:
```python
from os.path import join as osPathJoin
from os.path import exists as osPathExists
from requests import get as requestsGet
from time import sleep as timeSleep
from argparse import ArgumentParser as argparseArgumentParser
```

## Variable Naming Conventions

| Variable Type | Language | Convention | Example |
| :--- | :--- | :--- | :--- |
| Configuration | ALL | `ac` or `dConf` | `ac := &AppConfig{}`, `auto ac = LoadConfig(...)` |
| Loggers | ALL | `logger`, `unilog` | `logger = profiles.NewStandardLogger()` |
| Sockets | Go/Python | `sock`, `conn` | `serverSock, err := factory.Create(...)` |
| Private Member | VBA | `m_camelCase` | `Private m_handle As LongPtr` |
| Private Member | C++ | `snake_case_` | `std::string profile_;` |
| Local Variables | Rust/Python | `snake_case` | `retry_count = 5`, `let buffer_size = 1024` |
| Error handling | Go | Always `err` | `if err != nil { return nil, err }` |

## Motivation (Why?)
- Unified readability across polyglot microservices.
- Instant recognition of types and abstractions when switching between Go, Rust, Python, C++, and VBA.

## Examples
- `Logger` (Interface — all languages)
- `app_logger` (Variable — Python/Rust)
- `NewServer()` (Go Constructor)
- `LoadConfig("standalone")` (C++ / VBA factory)
