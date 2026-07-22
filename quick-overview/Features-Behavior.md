--- 
microservice: tech-stack-brain
type: architecture
status: active
tags:
- '#zone/3-fleet'
- '#ai/ignore'
- '#service/tech-stack-brain'
- '#type/architecture'
- '#state/active'
---
# Features & Behavior

The Tech Stack Brain provides several key behavioral features that ensure consistency across the Bastien-Antigravity fleet.

## 1. Engineering Governance
- **Rule Enforcement**: Defines the mandatory `CI/CD` quality gates that every repository must implement.
- **Pattern Standardization**: Enforces the Facade pattern to ensure all microservices have a predictable entry point (`src/facade/`).

## 2. Polyglot Parity
- **Unified Logic**: Uses CGO-based shared libraries (`libdistconf`, `libunilog`) to ensure that Python, Rust, and C++ services behave identically to Go services regarding configuration and logging.
- **Contract Enforcement**: Defines the superset/subset relationships between core library interfaces (e.g., `universal-logger` wrapping `flexible-logger`).

## 3. Configuration & Secrets
- **Layered Loading**: Implements a consistent 4-phase priority (CLI > Local YAML > Server > Env).
- **RSA Decryption**: Standardizes the `ENC(...)` pattern for sensitive data, ensuring secrets are decrypted only in volatile memory at runtime.

## 4. Fleet Validation
- **Automated Auditing**: The `Multi-Repo-Validator.py` script enables one-touch verification of the entire ecosystem's buildability and test status.
- **Language Detection**: The build system automatically adapts to Go, Rust, or Python environments without manual configuration.

## 5. Resilience Protocols
- **Zombie Detection**: Enforces the 2.5x heartbeat-to-timeout ratio for persistent sockets.
- **Ghost Protocol**: Mandates 5s hard deadlines and fallback strategies for all inter-service gRPC calls.
