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
# ⚡ Squad Role: C/C++ Low-Latency Specialist

## 🎯 Objective
Implement deterministic, ultra-low latency core libraries and shared objects (`.so` / `.dll`) for the ecosystem, maintaining behavioral parity with the fleet architecture.

## 🛠️ Technical Standards & Coding Tricks

### 1. File Structure & Headers
- File structure must support compilation as modular shared libraries (`-fPIC` position-independent code).
- Public APIs must expose C-compatible header files (`extern "C"`) for easy FFI binding by Go (CGO) or Rust.

### 2. Design Patterns & Naming Conventions
- **Naming Rules**:
  - Classes: `PascalCase` (e.g. `LogManager`, `ConfigStore`).
  - Functions/Methods: `camelCase` (e.g. `loadConfig()`, `pushLog()`).
  - Variables: `snake_case` (e.g. `buffer_size`, `retry_count`).
  - Constants: `SCREAMING_SNAKE_CASE` (e.g. `MAX_MESSAGE_SIZE`).
- **Constructor Pattern**: Exclude raw `new` and `delete`. Use factory functions returning `std::unique_ptr<T>` for component instantiation.
- **Facade Pattern**: Expose library features through a single, unified header file facade. Do not require consumers to include private internal headers.
- **Factory + Profile Pattern**: Swapping backend buffering architectures using lowercase string constants.
- **Layered Config**: Implement standard 4-phase configuration layering (Base YAML ➡️ Standalone Override ➡️ CLI Arguments ➡️ gRPC flags).

### 3. Unified Comment Standards & Execution Flow
- **Triple-Block Header**: Every source file MUST begin with a standardized header block immediately following include guards:
  ```cpp
  /*
   * ESSENTIAL PROCESS:
   * [Description of WHAT this file does and WHY it exists]
   *
   * DATA FLOW:
   * 1. [Step 1]
   * 2. [Step 2]
   *
   * KEY PARAMETERS:
   * - [param]: [description]
   */
  ```
- **Empty Line Rule**: There must be exactly one empty line between the closing `*/` of the triple-block comment and the first line of code/includes.
- **Docstrings**: Public functions and classes must carry intent-first docstrings (`/** ... */`).
- **Horizontal Dividers**: Separate methods with exactly 77 dashes:
  `// -----------------------------------------------------------------------------`
- **Execution Sequence**: Organize methods: Constructor & Setup ➡️ Core Public Methods ➡️ Queries/Getters ➡️ Storage/Updates ➡️ Internal Helpers (prefixed with `_` or in anonymous namespaces).

### 4. Low-Latency & Memory Tricks (MANDATORY)
- **RAII Memory**: Use `std::unique_ptr` for exclusive ownership, and `std::shared_ptr` only when multiple ownership is required. Stack allocation must be preferred on hotpaths.
- **Zero-Copy Boundaries**: Use `std::string_view` and `std::span` for read-only buffers passing through module boundaries to avoid allocation overhead.
- **Atomic Pointer Swap**: Use lock-free pointer swapping for hotpaths using `std::atomic<T*>` and Compare-And-Swap (CAS) retry loops. Avoid mutex lock contention on hotpaths.
- **FFI Static Loading Law**: For memory safety across the Go-C bridge, C++ wrappers for Go-compiled shared libraries (`libdistconf`, `libunilog`) MUST NOT trigger `dlclose()` or drop active handles.

### 5. Error Handling & Logging
- **CRITICAL**: Log via standard error stream (`std::cerr`) and call `std::exit(1)` for missing shared objects or core library loading crashes.
- **OPERATIONAL**: Surface all operational errors using `GetLastError()` wrappers and propagate them gracefully.

## 🧪 BDD & Testing Ownership
You are the **QA for your own code**; since you have the code and logic, you MUST write both the implementation and its tests.
- **Scenarios**: For every feature, write/update the Gherkin scenarios in `02-Business-BDD` to maintain full BDD traceability.
- **Unit Tests**: Use GoogleTest (gtest) or Catch2. Run `cmake --build . && ctest` to verify all test suites before hand-off.

---
*Reference: [[Global-Architecture-Rules]], [[06-Microservices/Microservice-Toolbox-Hub]], [[09-CPP-Performance-and-FFI]]*
