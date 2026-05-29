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
# 📐 Level 05 - Fleet Operations

This document defines the architecture, governance principles, and management scripts for **Level 05: Fleet Operations** within the Bastien-Antigravity ecosystem.

---

## 🏛️ 1. Magnitude: Multi-Repository Operations & CI/CD Pipelines (Scale: Cluster Deployment)

Level 05 governs the **physical operations, synchronization, and deployment states** of the entire microservice fleet. It acts as the command center for repository inventory and build pipelines.

*   **Level Classification**: **Operational Realizations**. Tracks concrete repository configurations, Git state registries, and CD logs.
*   **Abstractions Governed**: Master repository inventories, Git submodule configurations, CI/CD pipeline structures, deployment logs, and remote synchronization routines.
*   **Cognitive Scope**: Multi-repository deployment and operational orchestration.
*   **Authority Limit**: The root authority for cluster deployments; all automation launch files and operations must register their state changes at this level.

---

## 🧱 2. Merged Filesystem & Git Submodule Colocation

*   **Submodule Mapping**: Maps physically to the `05-Fleet-Operation` Git repository.
*   **Logical Merge**: Mounts within the double-digit stack hierarchy of the master workspace:
    ```
    obsidian-brain (Workspace Root)
    └── 05-Fleet-Operation/        # Merged repository mount
        ├── 00-Repo-Control/       # Master inventory mapping (inventory.json)
        ├── 01-Fleet-Action-Plans/ # Standard deployment steps
        ├── 02-Deployment-Logs/    # Live operational output files
        ├── 05-Fleet-Strategy/     # CI/CD and lifecycle rules
        └── Role-Prompts/          # Colocated fleet commander agent prompts
    ```
*   **Colocation Rule**: All operational tools, submodule registries (`inventory.json`), deployment checklists, and the Fleet Commander agent prompt are stored physically inside the L05 repository, ensuring they check out together.
*   **Stateless Portability**: Inter-repo references use the local JSON registry to decouple operations from absolute local paths.

---

## ⚙️ 3. Runnable Isolation & Progressive Dependencies

Level 05 is progressively runnable and requires preceding levels to be present:
*   **Required Dependencies**: Requires **Level 00 (AI Orchestration)**, **Level 01 (Strategic Nexus)**, **Level 02 (Business BDD)**, **Level 03 (Tech Stack)**, and **Level 04 (Rapid Prototyping)** to be checked out and present in the local filesystem.
*   **Runnable Isolation**: Once L00 to L04 are present, L05 can execute Git submodule checkouts, validate repository inventory registries, and run health check templates in isolation without invoking main microservices.

---

## 🐍 4. Python Management & Automation Suite

Level 05 is governed and executed by the following scripts:

### 🐙 Master Repository Registry (`inventory.json`)
*   **Location**: [inventory.json](../../05-Fleet-Operation/00-Repo-Control/inventory.json) (colocated inside L05).
*   **Operation**: The definitive directory mapping every microservice repository in the fleet to its upstream Git URLs and active branches.

### 🤖 The Fleet Commander Agent
*   **Role Prompt**: [Prompt-FleetCommander.md](../../07-Core-KMS/Role-Prompts/07-FleetCommander/Prompt-FleetCommander.md) (colocated inside L05 and compiled to `.gemini/agents/fleet_commander.md`).
*   **Operation**: Coordinates multi-repository updates, verifies deployment pipelines, and logs pipeline completions.

### ⚙️ Automation Launcher (`fleet-manager.py` / `fleet-commander.py`)
*   **Scripts**: Located inside `08-Base-Scripts/fleet-commander.py` and `05-Fleet-Operation/` scripts.
*   **Operation**: Automates Git commands (submodule updates, mass branching, and cross-repo health audits) using Python's standard library.
