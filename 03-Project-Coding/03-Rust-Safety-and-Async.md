---
title: Rust Safety and Async
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# 📐 Rust Safety and Async

## Architectural Rule
- **Polyglot Parity**: Rust implementations (especially in shared libraries) MUST maintain behavioral and API parity with the Go "Source of Truth".
- **The Performance Exception**: `unsafe` code is permitted for performance-critical logic (e.g., FFI, zero-copy parsing) but must be encapsulated within safe abstractions and explicitly justified in comments.
- **Atomic State Management**: Mirror the Go **Atomic Pointer Swap** pattern using `ArcSwap` or atomic primitives to manage shared state without locks in hotpaths.
- **Async Runtime**: Use `tokio` with full features.
- **Error Handling**: Use `Result<T, Box<dyn std::error::Error>>` and propagate with `?`. Use `.ok_or_else()` for descriptive error mapping.
- **Ownership**: Prefer borrowing over cloning. Explicitly `.clone()` only when struct ownership is required.
- **Polymorphism**: Use `Arc<dyn Trait>` for thread-safe shared ownership. Mirror the Go **Factory/Profile** pattern to enable deterministic dependency injection.
- **Entry Point Errors**: Use `match` with `eprintln!` + `std::process::exit(1)`. Never `unwrap()` in production paths.
- **Feature Flags**: Use `#[cfg(feature = "...")]` for optional integrations (e.g., `unilog`).

## ⚙️ Configuration & Merging
- **Recursive Merging**: Use a `deep_merge` logic for matching YAML/Mapping values to ensure layered configuration consistency across the ecosystem.

## 📦 Dynamic Versioning (`VERSION.txt` ONLY via `AppConfig`) & Standard Toolbox Modules
- **Dedicated `AppConfig` Accessor**: Rust microservices MUST access their version via `app_config.get_version()` (backed strictly by `VERSION.txt`, fail-fast if absent). Hardcoding version strings, `"0.0.1"` fallbacks, runtime `APP_VERSION` / `SERVICE_VERSION` env overrides, and ad-hoc `VERSION.txt` readers are strictly prohibited (`HARDCODED_VERSION_VIOLATION`).
- **Built-In Standard Tools**: Use `microservice_toolbox::spec` (`publish_with_lifecycle`, `build_spec_from_config`), `microservice_toolbox::contracts` (`ExchangeContract`, `ContractsEnvelope`, `extract_proto_operations`, `extract_capnp_operations`, `build_contracts_envelope`), `microservice_toolbox::wiretap` (`configure_from_config`, `set_enabled`/`is_enabled`, `record_event`, `snapshot`), `microservice_toolbox::notification`, `microservice_toolbox::lifecycle`, `microservice_toolbox::connectivity`, and `microservice_toolbox::business` instead of hand-rolling registration, IDL parsers, or telemetry clients.
- **Cold-Path Validation**: Validate configuration and capabilities once at startup; trust `AppConfig` string outputs verbatim inside handlers with zero silent fallbacks.

## 🏷 Identity & Logging
- **Static Identity**: Every struct implementing logic should have a `Name` static property (or field) used for logging traceability.

## Naming Conventions (Rust-specific)
- **Functions**: `snake_case` — `load_config()`, `run_server()`, `deep_merge()`
- **Structs**: `PascalCase` — `AppConfig`, `LogServer`, `ToolboxArgs`
- **Methods**: `snake_case` — `get_listen_addr()`, `apply_cli_overrides()`
- **Modules**: `mod.rs` for directory modules

## Logger Integration
```rust
// Optional UniLogger bootstrap via feature flag
#[cfg(feature = "unilog")]
{
    match unilog_rs::UniLog::new(profile, app_name, "standard", LogLevel::Info, false) {
        Ok(unilog) => Arc::new(UniLogger::new(unilog)),
        Err(e) => {
            let fallback = ensure_safe_logger(None);
            fallback.warning(&format!("Failed to bootstrap UniLogger: {}", e));
            fallback
        }
    }
}
```

## Motivation (Why?)
- Performance: Leverages Rust's zero-cost abstractions for high-performance servers.
- Reliability: Enforces compile-time safety and prevents runtime panics.

## Examples
```rust
// Preferred borrowing
fn process(data: &str) { ... }

// Error propagation
fn run() -> Result<(), Box<dyn Error>> {
    let config = load_config()?;
    Ok(())
}

// Tokio async server (log-server pattern)
fn run_server(name: &str, host: &str, port: u16, ...) -> Result<(), Box<dyn Error>> {
    let runtime = tokio::runtime::Runtime::new()?;
    runtime.block_on(async {
        let server = LogServer::new(name, host, port, ...).await?;
        server.run().await
    })
}
```
