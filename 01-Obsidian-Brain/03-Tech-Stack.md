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
# 📐 Level 03 - Tech Stack

This document defines the architecture, governance principles, and management scripts for **Level 03: Tech Stack** within the Bastien-Antigravity ecosystem.

---

## 🏛️ 1. Magnitude: Architectural Conventions & Engineering Guidelines (Scale: Code Syntax & Facades)

Level 03 defines **how** the ecosystem is constructed physically. It establishes the global coding styles, language-specific idioms, decoupling patterns, and memory safety laws to ensure system performance and portability.

*   **Level Classification**: **Contextual Override**. Technical styles, naming conventions, and developer specialist prompts override fallback behaviors when engineering tasks are executed.
*   **Abstractions Governed**: Coding styles, naming conventions, language standards (Go, Rust, Python, C++, VBA), cross-language binary boundaries (FFI), Facade patterns, process lifecycles, and deployment configurations.
*   **Cognitive Scope**: Engineering and system-wide technical conventions.
*   **Authority Limit**: Governs the coding conventions for all active developers; all microservice repositories must conform to the standards detailed inside the `03-Tech-Stack` folders.

---

## 🧱 2. Merged Filesystem & Git Submodule Colocation

*   **Submodule Mapping**: Maps physically to the `03-Tech-Stack` Git repository.
*   **Logical Merge**: Mounts within the double-digit stack hierarchy of the master workspace:
    ```
    obsidian-brain (Workspace Root)
    └── 03-Tech-Stack/             # Merged repository mount
        ├── 01-Obsidian-Brain/     # Vault structure & organization notes
        ├── 02-Project-Architecture/# System rules, ADRs, & facade patterns
        ├── 03-Project-Coding/     # Language style guides & FFI laws
        ├── 04-Project-Deployment/ # Docker & CI/CD deployment rules
        └── Role-Prompts/          # Colocated developer specialist agent prompts
    ```
*   **Colocation Rule**: All technical guidelines, ADR templates, and role prompts specific to engineering specialists (like CPP, VBA, and Rust developers) are physically attached (stored) inside the L03 repository, ensuring they check out together.
*   **Stateless Portability**: Links use Obsidian wikilinks and relative paths to maintain local navigation integrity.

---

## ⚙️ 3. Runnable Isolation & Progressive Dependencies

Level 03 is progressively runnable and requires preceding levels to be present:
*   **Required Dependencies**: Requires **Level 00 (AI Orchestration)** (for session state), **Level 01 (Strategic Nexus)** (for strategic constraints), and **Level 02 (Business BDD)** (for behavioral specification contracts) to be checked out and present in the local filesystem.
*   **Runnable Isolation**: Once L00, L01, and L02 are verified, Level 03 can validate structural layouts, conventions compliance, and coding style guides in isolation without compiling code or deploying active containers.

---

## 🐍 4. Python Management & Automation Suite

Level 03 is managed and verified by the following tools:

### 🤖 Specialist Developer Agents
*   **Role Prompts**: Located in `03-Tech-Stack/Role-Prompts/03-Developer/Squad/` (e.g., [CPP-Low-Latency-Specialist.md](../Role-Prompts/03-Developer/Squad/CPP-Low-Latency-Specialist.md), [Rust-Safety-Specialist.md](../Role-Prompts/03-Developer/Squad/Rust-Safety-Specialist.md)).
*   **Operation**: Agents consume the specific coding guides colocated at this level to write compilable, memory-safe, and low-latency logic.

### 📜 Multi-Repo Validator Script
*   **Script**: [Multi-Repo-Validator.py](../05-Project-Scripts/Multi-Repo-Validator.py)
*   **Operation**: Standard script that validates multiple service repositories against the style guides and standard layout directories defined in L03.
