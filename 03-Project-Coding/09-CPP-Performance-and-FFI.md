---
title: C++ Performance and FFI
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
- '#tech/cpp'
---
# 📐 C++ Performance and FFI

## Architectural Rule
- **Standard**: **C++17** is the mandatory baseline for C++ headers/services (`-std=c++17`, `std::optional`), and **C11/C99** (`-std=c11`) for pure C ABI headers like `microservice_toolbox/spec/contracts.h`.
- **Polyglot Parity**: C++ implementations in `microservice-toolbox/cpp` MUST maintain behavioral parity with the Go "Source of Truth" (`config`, `version` via `ac->GetVersion()`, `connectivity::Resolver`, `lifecycle::LifecycleManager`, `spec::SpecPublisher` & `contracts.hpp`/`contracts.h`, `wiretap::WireTap.hpp`, `notification::NotificationClient`, `business::Models.hpp`).
- **Atomic Hotpaths**: For shared state in performance-critical paths, use lock-free atomics (`std::atomic<bool>`, `std::atomic<uint64_t>`). Eliminate mutex contention in hot-path telemetry (e.g., `WireTap.hpp`) and validated `AppConfig` reads.
- **Memory Management (RAII)**: Raw `new` and `delete` are strictly forbidden. Use `std::unique_ptr` for ownership and `std::shared_ptr` only when multiple ownership is required.
- **Error Transparency**: Surfaces all engine-level errors from the underlying C-bridge via `GetLastError()` wrappers.
- **FFI Stability (Static Loading Law)**: When wrapping `libdistconf`, `libunilog`, or `libnotif`, the library MUST NOT be unloaded via `dlclose`. This ensures memory safety across the Go-C bridge.

## 🛠 Construction & Implementation
- **Constructor Pattern**: Use factory functions returning `std::unique_ptr<T>` for component instantiation.
- **Zero-Copy Architecture**: Prefer `std::string_view` and `std::span` for read-only access to buffers crossing module boundaries.

## 🏷 Naming Conventions
- **Classes**: `PascalCase` — `LogManager`, `ConfigStore`.
- **Functions/Methods**: `camelCase` — `loadConfig()`, `pushLog()`.
- **Variables**: `snake_case` — `buffer_size`, `retry_count`.
- **Constants**: `SCREAMING_SNAKE_CASE`.

## 📦 Standard Toolbox & FFI Integration
```cpp
#include "microservice_toolbox/config/AppConfig.hpp"
#include "microservice_toolbox/lifecycle/LifecycleManager.hpp"
#include "microservice_toolbox/spec/spec.hpp"

// Use LoadConfig / AppConfig rather than raw DistConf C symbols in services:
auto ac = microservice_toolbox::config::LoadConfig("standalone", argc, argv);
std::string ver  = ac->GetVersion();              // VERSION.txt only, fail-fast
std::string addr = ac->GetListenAddr("my_svc");   // Validated string, zero fallback
```

## Motivation (Why?)
- Performance: Minimizes latency in high-frequency trading or logging scenarios.
- Safety: RAII and smart pointers eliminate common C++ memory leaks and double-free errors.
- Stability: Atomic swaps ensure lock-free state transitions during configuration hot-reloads.

---
*Reference: [[ADR-002-Static-Loading-Law]], [[07-Configuration-Standard]]*
