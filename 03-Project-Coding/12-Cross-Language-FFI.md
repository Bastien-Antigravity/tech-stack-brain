---
title: Cross-Language FFI
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
- '#tech/polyglot'
- '#tech/ffi'
- '#zone/3-fleet'
---
# 🔌 Cross-Language FFI & Shared Libraries

This note defines the standards and memory safety constraints for compiled Go Shared Libraries wrapped in Python, Rust, or Excel/VBA facades across the Bastien-Antigravity fleet.

---

## 🏛️ Architecture & Bridging Model

The Bastien-Antigravity fleet relies on compiled **Go Shared Libraries** (e.g., `universal-logger` core) wrapped in Python, Rust, or Excel/VBA facades.

```
+--------------------+
|  Python / Rust     |
+--------------------+
          | (ctypes / libloading)
          v
+--------------------+
| Go FFI Shared Lib  | <--- Mutex locks dynamic string allocations
| (CGO compilation)  |
+--------------------+
```

---

## 🔒 1. The Static Loading Law ("Purger Rule")

*   **Never Unload a Go Runtime:** Once a Go-based shared library is loaded using C FFI (`ctypes.CDLL` in Python or `libloading` in Rust), **never call dlclose/drop on the library handles**. Unloading a Go runtime from a running process leads to memory access violation segmentations and immediate process crashes. Let it live for the entire lifecycle of the host process.
*   **Go Runtime Threading Limitations**: The Go runtime starts background threads (Garbage Collector, Scheduler) upon initialization. Standard OS library unloading mechanisms (`dlclose` in C, `drop` in Rust) do not support the termination of these Go-internal threads.
*   **Lazy/Static Singleton Implementation**: In Rust, use `once_cell` or `lazy_static` to load the library exactly once and leak the reference. In Python, load the library at the module level and never delete the reference.

---

## 📊 2. Static Buffering for VBA

*   **No Dynamic Pointers:** Go structures cannot return dynamic pointers to VBA without causing memory leaks or access violations.
*   **Global Mutex Buffer:** Use a global mutex-protected static buffer (`vbaBuffer` inside CGO) to return static addresses that VBA reads instantly via `StringFromPtr`.

---

## Motivation (Why?)
*   **Parity**: Allows Python, Rust, and VBA to share high-performance core libraries compiled in Go without duplicating code.
*   **Stability**: Preventing the unloading of Go runtimes completely eliminates a class of memory access violation segfaults and hangs during process teardowns.
*   **Safety**: Explicit mutexes and static buffering protect Excel/VBA boundaries from memory leaks.

---
*Reference: [[ADR-002-Static-Loading-Law]], [[07-Hidden-Patterns-and-Gotchas]], [[09-CPP-Performance-and-FFI]], [[10-VBA-Excel-Integration]]*
