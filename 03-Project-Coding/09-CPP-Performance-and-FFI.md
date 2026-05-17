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
- **Standard**: C++20 is the mandatory baseline.
- **Polyglot Parity**: C++ implementations MUST maintain behavioral parity with the Go "Source of Truth".
- **Atomic Hotpaths**: For shared state in performance-critical paths, MUST use the **Atomic Pointer Swap** pattern (using `std::atomic<T*>`). This eliminates lock contention in hot-reloading scenarios.
- **Memory Management (RAII)**: Raw `new` and `delete` are strictly forbidden. Use `std::unique_ptr` for ownership and `std::shared_ptr` only when multiple ownership is required.
- **Error Transparency**: Surfaces all engine-level errors from the underlying C-bridge via `GetLastError()` wrappers.
- **FFI Stability (Static Loading Law)**: When wrapping `libdistconf` or `libunilog`, the library MUST NOT be unloaded via `dlclose`. This ensures memory safety across the Go-C bridge.

## 🛠 Construction & Implementation
- **Constructor Pattern**: Use factory functions returning `std::unique_ptr<T>` for component instantiation.
- **Zero-Copy Architecture**: Prefer `std::string_view` and `std::span` for read-only access to buffers crossing module boundaries.

## 🏷 Naming Conventions
- **Classes**: `PascalCase` — `LogManager`, `ConfigStore`.
- **Functions/Methods**: `camelCase` — `loadConfig()`, `pushLog()`.
- **Variables**: `snake_case` — `buffer_size`, `retry_count`.
- **Constants**: `SCREAMING_SNAKE_CASE`.

## 📦 FFI & Shared Engine
```cpp
// Example C-Bridge Wrapper for libdistconf
extern "C" {
    void* Toolbox_LoadConfig(const char* profile, const char* path);
    const char* Toolbox_GetLastError();
}

class ConfigHandle {
public:
    explicit ConfigHandle(const std::string& profile) {
        handle_ = Toolbox_LoadConfig(profile.c_str(), nullptr);
        if (!handle_) {
            throw std::runtime_error(Toolbox_GetLastError());
        }
    }
    ~ConfigHandle() = default; // Static Loading Law: No dlclose
private:
    void* handle_;
};
```

## Motivation (Why?)
- Performance: Minimizes latency in high-frequency trading or logging scenarios.
- Safety: RAII and smart pointers eliminate common C++ memory leaks and double-free errors.
- Stability: Atomic swaps ensure lock-free state transitions during configuration hot-reloads.

---
*Reference: [[ADR-002-Static-Loading-Law]], [[07-Configuration-Standard]]*
