---
microservice: ecosystem-wide
type: architecture
status: active
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#service/obsidian-brain'
- '#state/active'
- '#type/architecture'
---
# 🧪 Testing Sandbox Standards (BDD)

## 🎯 Architecture Intent
The sandbox is the central validation hub for the Bastien-Antigravity ecosystem. It enforces a strict separation between **Behavioral Features** and **Technical Implementations**.

## 📂 Standard Directory Structure (2-Digit System)
All testing sandboxes must follow this hierarchy:

- **`00-Environment`**: Infrastructure as Code (Docker Compose, NATS, network topologies).
- **`01-Specifications`**: BDD-style YAML files defining the "What" (Business Scenarios).
    - MUST include a `Spec: [...]` link to the Business BDD brain.
    - MUST use `FEAT-XXX` prefixes.
- **`02-Scenarios`**: Technical implementations in Go, Rust, or Python defining the "How" (Validation Logic).
    - Path format: `02-Scenarios/<lang>/<test_file>`.
- **`03-Orchestration`**: Management scripts and the `scenario_orchestrator.py` engine.
- **`04-Reporting`**: Centralized output for logs, test results, and performance audit trails.

## 🚀 Orchestration Standard
- Scenarios MUST be executable via the `03-Orchestration/scenario_orchestrator.py` tool.
- The orchestrator MUST print the Business Spec link at the start of every run.
- Tests MUST support both `native` (local binary) and `docker` modes.

## 🏛️ The 3-Tier Testing Pyramid & Scope Allocation
To prevent duplicate test maintenance and eliminate blurred boundaries across repositories, tests in the Bastien-Antigravity fleet strictly adhere to a 3-tier hierarchy:

1. **Tier 1: Core Service & Daemon Unit Tests (Service Repository)**
   - **Location**: Inside the service repository (e.g. `notif-server/src/core/`, `notif-server/src/server/`, `log-server/src/`).
   - **Scope**: Internal daemon logic, Go/Rust network protocols, worker pools, buffer saturation, and compiling the CGO shared library (`libnotif`, `libdistconf`, `libunilog`).
   - **Boundary**: Daemon repositories do NOT maintain redundant end-user polyglot client test suites in `notif/python/tests/` or `notif/rust/tests/`. Their duty is strictly compiling and exposing the C ABI.

2. **Tier 2: Unified Developer Facade & Client SDK Tests (`microservice-toolbox`)**
   - **Location**: Inside `microservice-toolbox` (`go/pkg/.../*_test.go`, `python/tests/`, `rust/tests/`, `cpp/tests/`).
   - **Scope**: Single source of truth for polyglot client behavior consumed by microservices (`from_config`, dynamic address resolution, zero silent fallback, parameter validation, timeout handling, and connection lifecycle across all supported languages).

3. **Tier 3: Multi-Service Orchestration Scenarios (`sandbox-testing`)**
   - **Location**: Inside `sandbox-testing` (`01-Specifications/`, `02-Scenarios/{go,python,rust}/`).
   - **Scope**: Multi-service orchestration and end-to-end fleet integration (e.g., client microservice -> `microservice-toolbox` -> `notif-server` -> Telegram/Discord mock sinks; network partitions, port drift, and Docker Guard validation).
   - **Boundary**: Does NOT test unit-level syntax or low-level library shims.

## 🤖 AI Governance
AI agents are encouraged to generate new scenarios directly in `01-Specifications/` and provide corresponding validation logic in `02-Scenarios/` to ensure 100% specification coverage.

---
*Status: Production Standard v1.0*
*Enforced by: Sentinel / Fleet Architect*
