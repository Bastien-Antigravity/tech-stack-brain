---
title: "Hidden Patterns and Gotchas"
type: architecture
status: active
microservice: ecosystem-wide
---

# ⚠️ Hidden Patterns and Gotchas

## 1. Safe Logger Guard (MANDATORY)
Every toolbox entry point wraps the logger in a nil-safe wrapper:
```
Go:     safeLogger := utils.EnsureSafeLogger(logger)
Rust:   let final_logger = ensure_safe_logger(logger)
Python: self.logger = ensure_safe_logger(logger)
```
**Why**: Prevents nil-pointer panics when no logger is provided.

## 2. gRPC Port Convention: `base_port + 1`
When no explicit gRPC config exists, ALL three languages fall back to `port + 1`. If you set port `9020`, gRPC will bind to `9021`.

## 3. Broadcast Sends are Fire-and-Forget
In `config-server`, broadcast writes spawn a goroutine per client with **no error handling** on `Write()`. Failed sends are silently dropped.

## 4. Store `Get()` Returns Shared Data
`config-server/src/store/store.go` `Get()` returns a dereferenced pointer to shared data. The comment says "SHOULD NOT be modified", but there's no enforcement. Always use `GetSection()` for safe copies, or `DeepCopy()` before mutation.

## 5. Python is Stricter Than Go/Rust
- **Go/Rust**: Silently skip missing config files
- **Python**: Raises `FileNotFoundError`
This means Python may break in scenarios where Go/Rust would degrade gracefully.

## 6. Config Profile Detection
Dev mode check is hardcoded: `profile == "standalone" || profile == "test"`. Profiles `"production"` and `"preprod"` fall through to the else branch without explicit check.

## 7. CGO Bridge & Shared Engine
The FFI logic is decoupled into a "Smart Bridge" (`src/cgo_bridge` in `distributed-config`). Multiple libraries (`libdistconf`, `libunilog`) import this same package.
*   **Why**: Ensures memory space unification. If both libraries are linked, they share the same handles and global state.
*   **Rule**: Never put `//export` statements in the core logic package; keep them in the standalone `main` entry points.

...

## 11. Go Shared Library Unloading (`dlclose`)
**CRITICAL**: Never unload a Go-based shared library (`dlclose` in C, `drop` of `Library` in Rust) once loaded.
*   **Why**: The Go runtime starts background threads (GC/Scheduler) that do not support shutdown. Unloading the library while these threads are active causes an indefinite hang or crash.
*   **Solution**: Use "load-once" patterns (e.g., leaked static references in Rust).

## 8. Domain-Specific Log Levels
Custom levels beyond standard: `Stream`, `Logon`, `Logout`, `Trade`, `Schedule`, `Report`. These are **financial services / market data** domain levels.

## 9. Config File Naming Inconsistency
Some config files use prefix (`config_preprod.yaml`) and others don't (`standalone.yaml`). Be aware when switching profiles.

## 10. Duplicate GoDoc in Socket Factory
`safe-socket/src/factory/socket_factory.go` has the `Create` function documented twice (copy-paste artifact). The function body is correct.
