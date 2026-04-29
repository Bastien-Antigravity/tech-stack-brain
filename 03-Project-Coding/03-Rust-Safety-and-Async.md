---
title: "Rust Safety and Async"
type: architecture
status: active
microservice: ecosystem-wide
---

# 📐 Rust Safety and Async

## Architectural Rule
- **Polyglot Parity**: Rust implementations (especially in shared libraries) MUST maintain behavioral and API parity with the Go "Source of Truth".
- **Async Runtime**: Use `tokio` with full features.
- **Error Handling**: Use `Result<T, Box<dyn std::error::Error>>` and propagate with `?`. Use `.ok_or_else()` for descriptive error mapping.
- **Ownership**: Prefer borrowing over cloning. Explicitly `.clone()` only when struct ownership is required.
- **Polymorphism**: Use `Arc<dyn Trait>` for thread-safe shared ownership of polymorphic components (e.g., Loggers, Config Loaders).
- **Entry Point Errors**: Use `match` with `eprintln!` + `std::process::exit(1)`. Never `unwrap()` in production paths.
- **Feature Flags**: Use `#[cfg(feature = "...")]` for optional integrations (e.g., `unilog`).

## ⚙️ Configuration & Merging
- **Recursive Merging**: Use a `deep_merge` logic for matching YAML/Mapping values to ensure layered configuration consistency across the ecosystem.

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
