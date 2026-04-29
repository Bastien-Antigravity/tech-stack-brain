---
type: architecture
status: active
microservice: ecosystem-wide
title: "Repository Structure"
---

# 03 - Repository Structure

This governs the folder structure for all microservices in the ecosystem.

## Go Services (Primary Language)
- `cmd/<service-name>/main.go`: The entry point. It should ONLY handle bootstrap (config, logging, signal handling, and Facade instantiation).
- `src/`: The heart of the application logic.
    - `src/interfaces/`: Interface definitions (`IBroker`, `IDataSource`).
    - `src/models/`: Shared data structures (`MMarketData`).
    - `src/config/`: Configuration mapping (`config.go`).
    - `src/grpc_control/`: Service lifecycle and gRPC management.
    - `src/factories/`: Strategy pattern implementations for creating concrete types.
- `config/`: Root folder containing `standalone.yaml` and other environment-specific configurations.
- `doc/`: Architectural documentation and ASCII diagrams.

## Rust Services (e.g., log-server)
- `src/main.rs`: The entry point. Uses `microservice-toolbox` for config loading.
- `src/core/`: Central server/engine logic.
- `src/servers/`: Network server implementations (TCP, gRPC).
- `src/models/`: Shared data structures.
- `src/protocols/`: Serialization schemas (Cap'n Proto).
- `Cargo.toml`: Dependency manifest. Use local `path` dependencies for `microservice-toolbox`.

## Python Services (e.g., enhanced-backtesting, fundamental-analysis)
- `main.py`: The entry point.
- `src/`: Business logic modules.
    - `src/interfaces/`: Abstract base classes for decoupling.
    - `src/factories/`: Strategy pattern.
    - `src/calculators/`, `src/data_loaders/`, `src/strategies/`: Domain logic.
- `config/`: YAML configuration files.
- `requirements.txt`: Python dependency manifest.
