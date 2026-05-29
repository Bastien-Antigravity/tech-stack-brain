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
# 📐 Level 06 - Microservices

This document defines the architecture, governance principles, and management scripts for **Level 06: Microservices** within the Bastien-Antigravity ecosystem.

---

## 🏛️ 1. Magnitude: Active Service Realization (Scale: Individual Microservice Hub)

Level 06 exposes **operational directories and hub notes** that act as structural bridges linking physical code repositories (such as `config-server`, `log-server`, or `safe-socket`) to live documentation.

*   **Level Classification**: **Operational Realizations**. Contains concrete documentation hubs representing the live microservice repositories.
*   **Abstractions Governed**: Individual microservice hubs, startup CLI protocols, API routing schemas, service-specific logging rules, and registry bindings.
*   **Cognitive Scope**: Single-service architecture and API endpoints.
*   **Authority Limit**: The hub note serves as the definitive reference manual for a microservice; any code changes or API modifications must be documented here.

---

## 🧱 2. Merged Filesystem & Git Submodule Colocation

*   **Submodule Mapping**: Maps physically to the `06-Microservices` Git repository.
*   **Logical Merge**: Mounts within the double-digit stack hierarchy of the master workspace:
    ```
    obsidian-brain (Workspace Root)
    └── 06-Microservices/          # Merged repository mount
        ├── Config-Server-Hub.md   # Hub note for Go config server
        ├── Log-Server-Hub.md      # Hub note for Rust log server
        ├── Market-Observer-Hub.md # Hub note for Go market observer
        └── ...                    # Specific service hub md notes
    ```
*   **Colocation Rule**: All individual service hub notes, API routing schemas, and service-specific guidelines are stored physically inside the L06 repository, ensuring they check out together.
*   **Stateless Portability**: All links use relative paths to easily map documentation to sibling capability directories.

---

## ⚙️ 3. Runnable Isolation & Dependencies

Level 06 is progressively runnable and requires preceding levels to be present:
*   **Required Dependencies**: Requires **Level 00** (session variables), **Level 01** (strategy), **Level 02** (BDD specs), **Level 03** (tech guidelines), **Level 04** (prototypes), and **Level 05** (fleet submodules inventory) to be checked out and present in the filesystem.
*   **Runnable Isolation**: Once L00 to L05 are verified, L06 service hubs are fully runnable. Developers can inspect configurations, review API routing, and trace logging rules in isolation for a single repository.

---

## 🐍 4. Python Management & Automation Suite

Level 06 is governed and monitored by the following files and rules:

### 📜 Technical Startup Protocol
*   **Standard**: [Microservice-Startup-Protocol.md](../../06-Microservices/Microservice-Startup-Protocol.md) (colocated inside L06).
*   **Operation**: Governs the command-line interface arguments, exit codes, and flag conventions that every microservice in the fleet must support.

### 🧹 The DocMaintainer Agent
*   **Role Prompt**: [Prompt-DocMaintainer.md](../../07-Core-KMS/Role-Prompts/06-DocMaintainer/Prompt-DocMaintainer.md) (compiled to `.gemini/agents/doc_maintainer.md`).
*   **Operation**: Automatically audits the microservices directory, ensuring that every hub has up-to-date documentation and that the `quick-overview/` folder contains Architecture, Features, and Testing sheets.
