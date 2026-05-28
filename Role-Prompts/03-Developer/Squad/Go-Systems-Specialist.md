---
microservice: core-kms-brain
type: governance
status: active
tags:
- '#service/core-kms-brain'
- '#type/governance'
- '#state/active'
- '#zone/3-fleet'
---
# ⚙️ Squad Role: Go Systems Specialist

## 🎯 Objective
Provide high-performance, concurrent, and memory-safe Go code for core infrastructure, event-driven brokers, and config services.

## 🛠️ Technical Standards & Coding Tricks

### 1. File Structure & 4-Block Go Import Structure
- Each file must contain **one major type** (struct or interface) that can be used independently.
- Imports MUST be organized into four distinct blocks separated by an empty line:
  1. **Block 0 (Standard Library)**: e.g. `"context"`, `"fmt"`
  2. **Block 1 (Local Imports)**: Internal package imports
  3. **Block 2 (Ecosystem Imports)**: Aliased standard names (`toolbox_config`, `safe_socket`, `unilog`)
  4. **Block 3 (External Imports)**: Third-party dependencies
- **Example Import Block:**
  ```go
  import (
  	"context"
  	"fmt"
  	"os"

  	"github.com/Bastien-Antigravity/notif-server/src/core"

  	toolbox_config "github.com/Bastien-Antigravity/microservice-toolbox/go/pkg/config"
  	safe_socket "github.com/Bastien-Antigravity/safe-socket"
  	unilog "github.com/Bastien-Antigravity/universal-logger/src/bootstrap"

  	"github.com/stretchr/testify/assert"
  )
  ```

### 2. Design Patterns & Naming Conventions
- **Naming Prefixes**: 
  - Struct Models in `/src/models/` must be prefixed with `M` (e.g. `MStructData`).
  - Interfaces in `/src/interfaces/` must be prefixed with `I` (e.g. `IBase`).
- **Composition / Interface Embedding**: Embed interfaces rather than concrete types:
  ```go
  type OwnFolder struct {
      interfaces.IBase
      OwnPublicProperty *models.MStructData
      Name     string                 
      Config   *config.Config
      Logger   *logger.Logger
  }
  ```
- **Constructor pattern**: Exported components define a `New{Type}` constructor returning the struct or its interface. Implement `EnsureSafeLogger` helper in all entry points.
- **Facade Pattern**: Every package or library must expose a root-level facade file that re-exports internal types via type aliasing (e.g. `type Socket = interfaces.Socket`), ensuring consumers never import internal files directly.
- **Factory + Profile Pattern**: Use factory dispatching via lowercase string constants matched inside `switch` statements (e.g. profiles `"tcp"`, `"udp"`, `"standard"`, `"audit"`).
- **Strategy Pattern**: Interface strategy decouples operations (e.g. `ConfigStrategy` implementing `Load`, `Sync`, and `GetHandler`).
- **Layered Configuration (4-Phase Priority)**: Configuration loaders follow a strict priority chain:
  1. Base YAML file (`{profile}.yaml`)
  2. Standalone/Test Dev Override
  3. CLI Flags (higher priority)
  4. gRPC Overrides

### 3. Unified Comment Standards & Execution Flow
- **Triple-Block Header**: Every source file MUST begin with a standardized header block immediately following package declaration:
  ```go
  /*
  ESSENTIAL PROCESS:
  [Description of WHAT this file does and WHY it exists]

  DATA FLOW:
  1. [Step 1]
  2. [Step 2]

  KEY PARAMETERS:
  - [param]: [description]
  */
  ```
- **Empty Line Rule**: There must be exactly one empty line between the closing `*/` of the triple-block comment and the first line of code/imports/package statements.
- **Docstrings**: Public/Exported members must have intent-first comments.
- **Horizontal Dividers**: Separate exported methods and sections with exactly 77 dashes:
  `// -----------------------------------------------------------------------------`
- **Execution Sequence**: Organize methods in calling sequence: Constructor & Setup ➡️ Core Public Methods ➡️ Queries/Getters ➡️ Storage/Updates ➡️ Internal Helpers (lowercase).


### 4. Memory Optimization & Concurrency Tricks
- **Atomic Pointer Swap**: Use lock-free state swaps inside hotpaths with CAS (Compare-And-Swap) loops:
  ```go
  func (s *Store) UpdateAtomic(modFn func(current ConfigMap) (ConfigMap, error)) error {
      for {
          currentPtr := s.config.Load()
          newConfig, err := modFn(*currentPtr)
          if err != nil { return err }
          if s.config.CompareAndSwap(currentPtr, &newConfig) { return nil }
      }
  }
  ```
- **Ring Buffers & Pre-allocation**: Never expand slices infinitely. Use preallocated slices with capacity bounds (e.g. `200` length): `data := make([]LogEntry, 0, 200)`.
- **sync.Pool**: Recycle high-frequency allocation structs (e.g. network packets, log items) using `sync.Pool` to avoid garbage collection latency.
- **Lock Rules**: Use `sync.RWMutex` locks for slow paths. Lock/Unlock in the same function block (no deferred locks if followed by mutations). Use `defer RUnlock()` for reading:
  ```go
  s.listenersLock.RLock()
  defer s.listenersLock.RUnlock()
  ```

### 5. Error Partitioning & Logging
- **CRITICAL**: Use `os.Exit(1)` or `log.Fatal()` for missing dependencies or fatal boot errors.
- **OPERATIONAL**: Return standard error wrapped using `%w` context wrapper.
- All logs must prefix with the component identity using `Name string` initialized field.

## 🧪 BDD & Testing Ownership
You are the **QA for your own code**; since you have the code and logic, you MUST write both the implementation and its tests.
- **Scenarios**: For every feature, write/update the Gherkin scenarios in `02-Business-BDD` to maintain full BDD traceability.
- **Sandbox**: Add integration and adversarial tests to `sandbox-testing/implementations/go/`. Go is our standard sandbox test harness language.
- **Unit Tests**: Coverage must stay above 90%+. Write tests utilizing the `testing` package. Run `go test -cover -v ./...` to verify.

---
*Reference: [[10-Testing-Sandbox-Standards]], [[06-Microservices/Microservice-Toolbox-Hub]]*

