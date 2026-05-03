---
id: ADR-002
title: "The Static Loading Law (Go-FFI Safety)"
status: accepted
date: 2026-05-03
tags:
  - polyglot
  - ffi
  - safety
---

# ADR-002: The Static Loading Law (Go-FFI Safety)

## Context
Our ecosystem uses Go-based shared libraries (`.so`, `.dylib`, `.dll`) via CGO to provide 100% architectural parity for Python, Rust, and C++ applications. 

## The Problem
The Go runtime starts background threads (Garbage Collector, Scheduler) upon initialization. Standard OS library unloading mechanisms (`dlclose` in C, `drop` in Rust) do not support the termination of these Go-internal threads. Attempting to unload a Go-based library while the process is running results in:
1.  **Indefinite Hangs**: The process locks up waiting for threads that cannot exit.
2.  **Segmentation Faults**: Memory is freed while the Go GC is still trying to scan it.

## Decision
All Go-based shared libraries in the Bastien-Antigravity ecosystem MUST be treated as **Static/Immortal** components for the duration of the host process's life.

1.  **No Unloading**: Explicit unloading calls (like `dlclose`) are strictly forbidden.
2.  **Lazy/Static Singleton**: In Rust, use `once_cell` or `LazyStatic` to load the library exactly once and leak the reference. In Python, load the library at the module level and never delete the reference.
3.  **Process-Bound**: The library life must be bound to the process life.

## Consequences
- **Positive**: Complete elimination of FFI-related crashes during shutdown.
- **Negative**: Slightly higher memory footprint for short-lived processes (though negligible in our microservice context).

---
*Linked Docs: [[07-Hidden-Patterns-and-Gotchas]], [[distributed-config/README]]*
