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

## 🛡️ Strict 2-Zone GitHub CI Isolation & Adversarial Testing Rules

1. **Zone 1 (Tier 1 & Tier 2 Repos — Standalone CI Safe)**:
   - In GitHub Actions, each repository is checked out in isolation without sibling directories (`../<repo>`), without the `standalone.yaml -> ../docker-deployment/modes/local/config/native.yaml` target, and without `~/.bastien/keys/private.pem`.
   - Unit tests inside service and library repositories **MUST** use self-contained fixtures (`t.TempDir()` + `t.Setenv("CONFIG_PATH", yamlPath)` and ephemeral test keys) and **MUST NOT** perform unguarded file reads across `../<sibling-repo>`.
   - Mechanically enforced by `validate_compliance.py` (`UNIT_TEST_STANDALONE_SYMLINK_DEPENDENCY` and `UNIT_TEST_CROSS_REPO_LEAK`).
2. **Zone 2 (Tier 3 `sandbox-testing` — Cross-Repo & Live Fleet)**:
   - All tests that inspect sibling repository files, verify compiled FFI shared library parity across repositories, or connect to live fleet daemons MUST reside in `sandbox-testing/02-Scenarios/`.
   - When `sandbox-testing` runs in single-repo GitHub CI (`master-ci.yml`), all Go scenario packages are compile-verified (`GOWORK=off go test -c -o /dev/null .`) while multi-repo/live-daemon execution skips cleanly unless `SANDBOX_LIVE_FLEET=true` or sibling checkouts are present.
3. **Adversarial & Fault-Injection Mandate**:
   - Every feature or protocol test suite must pair normal-operation tests with adversarial fault scenarios: timeouts, buffer saturation, oversized/corrupt frames (`MaxPayloadSize`), stale revision conflicts, concurrent writer races (`go test -race`), and disk/crash recovery.

## 🤖 AI Governance
AI agents are encouraged to generate new scenarios directly in `01-Specifications/` and provide corresponding validation logic in `02-Scenarios/` to ensure 100% specification coverage.

---
*Status: Production Standard v1.0*
*Enforced by: Sentinel / Fleet Architect*
