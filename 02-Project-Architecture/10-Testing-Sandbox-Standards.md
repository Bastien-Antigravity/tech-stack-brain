# 🧪 Testing Sandbox Standards (BDD)

## 🎯 Architecture Intent
The sandbox is the central validation hub for the Bastien-Antigravity ecosystem. It enforces a strict separation between **Behavioral Features** and **Technical Implementations**.

## 📂 Standard Directory Structure
All testing sandboxes must follow this hierarchy:

- **`features/`**: High-level YAML/Markdown definitions. 
    - MUST include a `Spec: [[...]]` link to the Business BDD brain.
    - MUST use `FEAT-XXX` prefixes.
- **`implementations/`**: Polyglot code (Go, Python) that executes the steps.
    - Path format: `implementations/<lang>/<test_file>`.
- **`infra/`**: Environment orchestration (Docker, NATS, etc.).
- **`bin/`**: Standard execution scripts.

## 🚀 Orchestration Standard
- Scenarios MUST be executable via the `scenario_orchestrator.py` tool.
- The orchestrator MUST print the Business Spec link at the start of every run.
- Tests MUST support both `native` (local binary) and `docker` modes.

## 🤖 AI Governance
AI agents are encouraged to generate new scenarios directly in `features/` and provide corresponding `implementations/` to ensure 100% specification coverage.

---
*Status: Production Standard v1.0*
*Enforced by: Sentinel / Fleet Architect*
