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
# 📐 Level 00 - AI Orchestration

This document defines the architecture, governance principles, and management scripts for **Level 00: AI Orchestration** within the Bastien-Antigravity ecosystem.

---

## 🏛️ 1. Magnitude: Session Boot & User Interface (Scale: Single-Session)

Level 00 governs the **initialization, configuration, and interface execution** of the active development session. It acts as the gateway to the entire capability stack, setting up the environments and variables before downstream agents are deployed.

*   **Level Classification**: **Mutable Active Local State**. Session files, variables, and mode settings are updated constantly during active execution.
*   **Abstractions Governed**: Session log state (`AI-Session-State.md`), boot instructions (`AI-Init.md`), dynamic variables (`Project-Variables.md`), active protocol manuals (`MODE-MANUAL.md`), and automation files (`workflows/`).
*   **Cognitive Scope**: Single session span. It retains the immediate memory of the current chat loop and guards against context loss across sequential agent invocations.
*   **Authority Limit**: The root initialization layer; no downstream capability levels (L01 to L09) can run until Level 00 prepares the workspace and variables.

---

## 🧱 2. Merged Filesystem & Git Submodule Colocation

*   **Submodule Mapping**: Maps physically to the `00-AI-Orchestration` Git repository.
*   **Logical Merge**: Mounts at the base of the double-digit stack hierarchy of the master workspace:
    ```
    obsidian-brain (Workspace Root)
    └── 00-AI-Orchestration/       # Merged repository mount
        ├── workflows/             # YAML task execution pipelines
        ├── Templates/             # Standardized spec and task templates
        ├── AI-Init.md             # Standalone boot instruction prompt
        ├── AI-Project-DNA.md      # Local project quality gates
        ├── AI-Session-State.md    # Active checklist and session memory
        ├── Project-Variables.md   # Path mappings and global constants
        └── MODE-MANUAL.md         # Active protocol selector
    ```
*   **Colocation Rule**: All session-state tracking, environment variables, workflows, and templates specific to initialization are stored physically inside the L00 repository.
*   **Stateless Portability**: Requires no absolute path strings. All references utilize relative workspace paths or variables resolved dynamically during boot.

---

## ⚙️ 3. Runnable Isolation & Progressive Dependencies

Level 00 is the foundation layer:
*   **Required Dependencies**: None. Level 00 is completely independent. It can be checked out, initialized, and run in total isolation.
*   **Runnable Isolation**: Serves as the starting point. When booted, it verifies path existence and configures Model Context Protocol (MCP) server constraints before letting any other level load.

---

## 🐍 4. Python Management & Automation Suite

Level 00 boot and lifecycle are driven and verified by the base orchestration script:

### 🚀 Launcher Engine (`start_squad.py`)
*   **Script**: [start_squad.py](../../08-Base-Scripts/start_squad.py) (located in `08-Base-Scripts/` and running from the workspace root).
*   **Operation**: Reads `MODE-MANUAL.md` to switch protocols, configures MCP filesystem permissions based on active zone isolation rules, and launches the AI client (Gemini, Claude, or Deepseek API).

### ⚙️ Workspace Variable Sync
*   **Target**: [Project-Variables.md](../../00-AI-Orchestration/Config/Project-Variables.md)
*   **Operation**: Standard keys such as `ecosystem_name` and repo mappings are updated during initial scaffolding, ensuring downstream scripts can read paths dynamically.
