---
type: architecture
status: active
microservice: ecosystem-wide
title: Repository Structure
tags:
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
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

## Human Onboarding (All Languages — Mandatory)
Every microservice and library repository MUST include a `quick-overview/` folder at the root. This folder is **exclusively for human readers** and is excluded from AI agent context.

- `quick-overview/Architecture-Overview.md`: Visual graphs and explanations of the repo's internal structure.
- `quick-overview/Features-Behavior.md`: High-level overview of the service's features and core behaviors for human readers.
- `quick-overview/Testing-Playbook.md`: How to test this specific service (unit, integration, sandbox).
- `quick-overview/General-Misc.md`: Purpose, philosophy, and optimization tips for human operators.
- `quick-overview/.geminiignore`, `quick-overview/.mcpignore`, `quick-overview/.aiignore`: Mandatory ignore files to ensure AI agents skip this folder.

> [!IMPORTANT]
> AI agents MUST ignore `quick-overview/`. The **DocMaintainer** is the only agent responsible for keeping these files up-to-date after major architectural changes, even though the content targets human readers.

> [!NOTE]
> In `obsidian-brain`, the equivalent folder is called `99-Humans/` to follow the Obsidian 2-digit numbering convention.
