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

## 🤖 AI Governance
AI agents are encouraged to generate new scenarios directly in `01-Specifications/` and provide corresponding validation logic in `02-Scenarios/` to ensure 100% specification coverage.

---
*Status: Production Standard v1.0*
*Enforced by: Sentinel / Fleet Architect*
