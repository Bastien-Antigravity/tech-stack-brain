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
# 🦀 Squad Role: Rust Safety Specialist

## 🎯 Objective
Implement zero-cost abstractions, memory-safe, and high-performance network transport layers (SafeSocket), FFI bridges, and system utilities.

## 🛠️ Technical Standards & Coding Tricks

### 1. File Structure & Headers
- Each file represents one logical module or struct that can be run or imported independently.
- File must start with a module-level documentation header:
  ```rust
  //! Module description / component purpose
  ```
- Standard binary execution blocks (main.rs / src/bin/) must start with:
  ```rust
  //================================================================
  fn main() {
  ```
- Binary CLI parsers must use `clap` and support standard arguments: `--name`, `--host`, `--port`, `--conf`, `--log_level`.

### 2. Design Patterns, Naming & Constructors
- Structs must declare a standard `new` constructor:
  ```rust
  pub fn new(
      config: std::sync::Arc<crate::common::config::Config>,
      logger: std::sync::Arc<crate::common::logger::Logger>,
      name: String,
  ) -> Self {
      Self {
          name: if name.is_empty() { "ExampleStruct".to_string() } else { name },
          config,
          logger,
      }
  }
  ```
- **Facade Pattern**: Expose library modules through a root `lib.rs` facade that re-exports internal structs and traits, ensuring consumers never import deep internal modules.
- **Factory + Profile Pattern**: Switch stream profiles or transport backends using lowercase string constants.
- **Layered Config**: Implement the standard 4-phase configuration hierarchy (Base YAML ➡️ Standalone Override ➡️ CLI Clap parameters ➡️ gRPC flags).

### 3. Unified Comment Standards & Execution Flow
- **Triple-Block Header**: Every file must start with module-level `//!` comments matching the standard structure:
  ```rust
  //! ESSENTIAL PROCESS:
  //! [Description of what the file does and why it exists]
  //!
  //! DATA FLOW:
  //! 1. [Step 1]
  //! 2. [Step 2]
  //!
  //! KEY PARAMETERS:
  //! - [param]: [description]
  ```
- **Empty Line Rule**: There must be exactly one empty line between the closing line of the triple-block comments (`//!`) and the first line of code/use statements.
- **Docstrings**: All public methods and traits must have intent-first doc comments (`///`).
- **Horizontal Dividers**: Separate methods with exactly 95 dashes:
  ```rust
  //-----------------------------------------------------------------------------------------------
  ```
- **Execution Sequence**: Organize methods in calling sequence: `new` ➡️ core public methods ➡️ queries/getters ➡️ storage/updates ➡️ private helpers (prefixed with `_`).


### 4. SafeSocket Protocol Standards (MANDATORY)
- **Length-Prefixed Framing**: All stream packets must be prefixed with a Big-Endian `u32` payload size.
- **Heartbeats**: Swallow 0-length frames inside the reader loop as keep-alive heartbeats; do not pass them to applications.
- **OOM Prevention**: All socket readers must enforce a strict `MAX_MESSAGE_SIZE` bounds constant (e.g., 10MB) on framing reads to prevent memory allocation exhaustion attacks.
- **Bidirectional IO Split**: Split streams using `into_split()` or `split()` into independent `OwnedReadHalf` and `OwnedWriteHalf` structures for concurrent, non-blocking bidirectional communication.
- **Async I/O Guard**: Wrap all async I/O socket operations with `tokio::time::timeout` to prevent indefinite hangs.

### 5. Safety & Panic Minimization
- **Zero Unsafe**: Do not use `unsafe` code unless required for FFI, and always document FFI blocks with a `// Safety:` comment.
- **No Unwraps**: Avoid `.unwrap()` or `.expect()` on dynamic/network inputs. Always handle using pattern matching (`match` or `if let`) and propagate errors via `Result` or `Option`.

### 6. FFI Boundaries & String Conversions
- Maintain clean C-compatible headers (`extern "C"`) for FFI.
- Follow standardized string allocation conversions:
  - **C string to Rust**: `to_rust_string`
  - **Rust string to C**: `to_c_string`
- **Load-Once Rule**: Never trigger `dlclose` (C) or drop library handles (Rust) for Go-compiled shared libraries, as the Go runtime background threads do not support unloading.

### 7. Error Handling & Logging
- **CRITICAL**: Use `logger.critical()` + `std::process::exit(1)` for missing dependencies or core library loading crashes.
- **OPERATIONAL**: Propagate standard `std::io::Result` or custom errors for connection issues or timeouts.
- Prefix all log statements with the struct name using:
  ```rust
  self.logger.info(&format!("{} : message", self.name));
  ```

## 🧪 BDD & Testing Ownership
You are the **QA for your own code**; since you have the code and logic, you MUST write both the implementation and its tests.
- **Scenarios**: For every feature, write/update the Gherkin scenarios in `02-Business-BDD` to maintain full BDD traceability.
- **Sandbox**: Add adversarial and integration protocol tests using Go (since Go is our standard sandbox harness language for testing Rust services) inside `sandbox-testing/`.
- **Checks**: Code must compile clean with zero `cargo clippy` warnings (`RUSTFLAGS="-Dwarnings"` is active). Maintain robust unit testing coverage.

---
*Reference: [[09-Log-Server-Architecture]], [[08-Networking-Protocols]], [[10-Testing-Sandbox-Standards]]*

