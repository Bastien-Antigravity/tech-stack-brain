---
title: "Go Memory and Concurrency"
type: architecture
status: active
microservice: ecosystem-wide
---

# 📐 Go Memory and Concurrency

## Architectural Rule
- **Interface-First Design**: Major components MUST define their behavior via interfaces in a dedicated `src/interfaces` package. This prevents circular dependencies and enables deterministic testing with mocks.
- **Memory Efficiency**: Use fixed-length slices/ring-buffers (e.g., `200` length). NEVER expand arrays infinitely. Use `make` with capacity.
- **Concurrency**: Use `context.Context` for cancellation. Always deep-copy shared resources before crossing Goroutine boundaries.
- **Atomic State**: Use `atomic.Pointer` with CAS loops for lock-free reads (see `config-server/src/store/store.go`).

## 🛠 Construction & Implementation
- **Constructor Paradigm**: Use the `New{Type}` convention for instantiating components.
- **Safeguards**: Use "Ensure" helpers (e.g., `EnsureSafeLogger`) to provide default functional behavior if a dependency is nil.

## 🔗 Connectivity & Self-Healing
- **Automatic Reporting**: Internal failures in background routines must be reported via a centralized handler (e.g., `error_handler.ReportInternalError`).
- **Resilient Sockets**: Networking components must use the `microservice-toolbox` connection manager to handle retries and multiplicative backoff.

## 🏷 Metadata & Logging
- **Clean Metadata**: When detecting source information (caller info), always trim the path using `filepath.Base()` to keep log entries efficient and readable.
- **Component Identity**: Every struct implementing logic should have a `Name string` field, initialized during construction, and used as a prefix for all logs.

## Concurrency Patterns (from source code)

### Goroutine Conventions
- **Fire-and-forget broadcasts**: `go s.broadcastRegistry()`
- **Per-connection handlers**: `go s.handleConnection(conn)`
- **Async sends with captured variables**: `go func(n string, sk ...) { sk.Write(bytes) }(name, sock)`

### Lock Patterns
- **RWMutex for client maps**: `listenersLock sync.RWMutex`
- **Lock/Unlock in same function**: Never deferred if followed by mutations
- **Deferred RUnlock for reads**: `s.listenersLock.RLock(); defer s.listenersLock.RUnlock()`

### Channel Patterns
- **Buffered notification queues**: `make(chan *utils.NotifMessage, 1024)`
- **Graceful shutdown**: `shutdown chan struct{}` with `select` multiplexing

## Error Handling Pattern
```go
// Always wrap errors with context
if err := proto.Unmarshal(data, req); err != nil {
    return nil, fmt.Errorf("protobuf unmarshal error: %w", err)
}

// Fatal errors use os.Exit(1), never panic()
// Non-fatal errors log and continue
```

## Comment Style
Every Go file uses **horizontal rule comments** to separate logical sections:
```go
// -----------------------------------------------------------------------------
// Section Name
// -----------------------------------------------------------------------------
```
Applied between every exported function, interface method groups, and struct definitions.

## 📦 Go Import Structure
Imports MUST be organized into four distinct blocks, separated by a single empty line, to ensure readability and maintain a clear hierarchy of dependencies:

1.  **Block 0 (Standard Library)**: Pure Go standard library packages.
2.  **Block 1 (Local Imports)**: Internal packages from within the same repository.
3.  **Block 2 (Ecosystem Imports)**: Packages from other `Bastien-Antigravity` repositories. Every ecosystem library MUST be aliased using its explicit standard name (e.g., `toolbox_config`, `safe_socket`, `unilog`).
4.  **Block 3 (External Imports)**: All other third-party dependencies.

**Example Structure:**
```go
import (
	"context"
	"fmt"
	"os"

	"github.com/Bastien-Antigravity/notif-server/src/core"
	"github.com/Bastien-Antigravity/notif-server/src/server"

	toolbox_config "github.com/Bastien-Antigravity/microservice-toolbox/go/pkg/config"
	safe_socket "github.com/Bastien-Antigravity/safe-socket"
	unilog "github.com/Bastien-Antigravity/universal-logger/src/bootstrap"

	"github.com/stretchr/testify/assert"
)
```


## Motivation (Why?)
- Performance: Minimizes GC pressure and prevents OOM in high-throughput data processing.
- Safety: Eliminates data races in shared memory environments.

## Examples
```go
// Correct Slice Pre-allocation
data := make([]LogEntry, 0, 200)

// Atomic Store with CAS loop (from config-server)
func (s *Store) UpdateAtomic(modFn func(current ConfigMap) (ConfigMap, error)) error {
    for {
        currentPtr := s.config.Load()
        newConfig, err := modFn(*currentPtr)
        if err != nil { return err }
        if s.config.CompareAndSwap(currentPtr, &newConfig) { return nil }
    }
}
```
