---
microservice: tech-stack-brain
type: architecture
status: active
tags:
- '#service/tech-stack-brain'
- '#type/architecture'
- '#state/active'
- '#zone/1-nexus'
---
# 📐 Level 08 - Base Scripts

This document defines the architecture, governance principles, and management scripts for **Level 08: Base Scripts** within the Bastien-Antigravity ecosystem.

---

## 🏛️ 1. Magnitude: Active Utilities & Launch Control (Scale: Repository Operations)

Level 08 houses the **primary vault automation scripts, preflight validators, and agent session controllers**. While folders like `07-Core-KMS` define rules and metadata schemas, Level 08 contains the active Python processes that parse, validate, and execute them.

*   **Level Classification**: **Active Utility / Executable Scaffolding**. Real-time execution entrypoints, launcher scripts, and validation hooks.
*   **Abstractions Governed**: Preflight checkers, environment detection routines, git hooks, multi-client launching scripts, and folder replication scaffolding.
*   **Cognitive Scope**: Active vault process automation.
*   **Authority Limit**: The executable automation layer; scripts housed here run locally on the host machine to sync config states and audit file governance rules.

---

## 🧱 2. Merged Filesystem & Git Submodule Colocation

*   **Submodule Mapping**: Maps physically to the `08-Base-Scripts` Git repository.
*   **Logical Merge**: Mounts within the root of the master workspace:
    ```
    obsidian-brain (Workspace Root)
    └── 08-Base-Scripts/           # Merged repository mount
        ├── clients/               # AI clients integrations (deepseek, gemini, etc.)
        ├── lib/                   # Validation libraries and helper scripts
        ├── convert_agents.py      # Compile agent prompt configurations
        ├── start_squad.py         # Multi-agent squad launcher and coordinator
        └── vault-sentinel.py      # Background vault auditor and watcher daemon
    ```
*   **Colocation Rule**: All launcher frameworks, client SDK wrappers, and helper libraries (`lib/sovereignty.py`) are stored physically inside this capability folder, ensuring they are versioned and checked out together.

---

## ⚙️ 3. Runnable Isolation & Dependencies

Level 08 is progressively runnable and requires preceding levels to be present:
*   **Required Dependencies**: Requires **Level 00** through **Level 07** to be checked out and present in the local filesystem.
*   **Runnable Isolation**: Once preceding levels are verified, Level 08 scripts can boot the CLI, compile active personas, and run real-time audits against the metadata taxonomies configured in the KMS.

---

## 🐍 4. Python Management & Automation Suite

All automation and orchestration launcher scripts inside `08-Base-Scripts/` must adhere to these strict coding rules:

### A. The Virtual Environment Re-Execution Ritual
Every python script must locate and run in the local `.venv` by walking up the directory structure.

### B. Standard Output Encoding Standardization
Standard outputs must be reconfigured to UTF-8 to prevent console crashes across varying operating system bounds.

### C. Zero-Dependency Mandate
Scripts must strictly limit external imports to avoid bootstrapping loops.
