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
# 📐 Level 07 - Core KMS

This document defines the architecture, governance principles, and management scripts for **Level 07: Core KMS** within the Bastien-Antigravity ecosystem.

---

## 🏛️ 1. Magnitude: System Ontology & Squad Memory (Scale: Global Organization Wisdom)

Level 07 serves as the **master knowledge, ontology, validation engine, and default identity registry** of the ecosystem. It governs the structural rules and playbooks used to keep the vault clean and consistent.

*   **Level Classification**: **Default Immutable**. Default agent roles, tag taxonomies, and playbooks act as a read-only fallback system library.
*   **Abstractions Governed**: Global agent templates, daily playbooks, tag taxonomy definitions, core workflows, and system validation rules.
*   **Cognitive Scope**: Global squad wisdom and organizational memory.
*   **Authority Limit**: The root definition layer for agent roles and metadata conventions; all notes across all submodules are audited against the taxonomy and validation scripts housed here.

---

## 🧱 2. Merged Filesystem & Git Submodule Colocation

*   **Submodule Mapping**: Maps physically to the `07-Core-KMS` Git repository.
*   **Logical Merge**: Mounts within the double-digit stack hierarchy of the master workspace:
    ```
    obsidian-brain (Workspace Root)
    └── 07-Core-KMS/               # Merged repository mount
        ├── Role-Prompts/          # Portable generic agent templates
        ├── Rules/                 # Global structural conventions
        ├── Workflows/             # Daily playbooks and task routines
        └── tag_taxonomy.md        # Definitive allowed-tag taxonomy
    ```
*   **Colocation Rule**: All default agent templates, taxonomies, playbooks, the Sovereignty validation library (`sovereignty.py`), the prompt compiler (`convert_agents.py`), and the real-time sentinel script (`vault-sentinel.py`) are physically stored inside the L07 repository/scripts folders, ensuring they check out together.
*   **Stateless Portability**: Links use Obsidian wikilinks and relative paths to ensure search engines can index files correctly.

---

## ⚙️ 3. Runnable Isolation & Progressive Dependencies

Level 07 is progressively runnable and requires preceding levels to be present:
*   **Required Dependencies**: Requires **Level 00** (session state), **Level 01** (strategy), **Level 02** (BDD specs), **Level 03** (tech guidelines), **Level 04** (prototypes), **Level 05** (fleet info), and **Level 06** (microservice hubs) to be checked out and present in the filesystem.
*   **Runnable Isolation**: Once L00 to L06 are verified, Level 07 is fully runnable. Validators check tags, links, and YAML frontmatter against the taxonomies and rules in this layer.

---

## 🐍 4. Python Management & Automation Suite

Level 07 contains or governs the core scripts and libraries that keep the master vault compliant:

### 🛡️ The Sovereignty Validation Engine (`sovereignty.py`)
*   **Script**: [sovereignty.py](../../08-Base-Scripts/lib/sovereignty.py) (colocated inside the L07 validation libraries).
*   **Operation**: The centralized library that audits note tags, checks double-bracket wikilinks, enforces YAML frontmatter, and verifies agent `[SCAN]` blocks against [tag_taxonomy.md](../../07-Core-KMS/tag_taxonomy.md).

### 🤖 Prompt Compiler (`convert_agents.py`)
*   **Script**: [convert_agents.py](../../08-Base-Scripts/convert_agents.py) (colocated inside L07).
*   **Operation**: Compiles human-editable agent files under `Role-Prompts/` into system-level CLI configs (Gemini, Claude, Deepseek).

### 🚨 Real-time Workspace Auditor (`vault-sentinel.py`)
*   **Script**: [vault-sentinel.py](../../08-Base-Scripts/vault-sentinel.py) (colocated inside L07).
*   **Operation**: Spawns a lightweight watcher daemon that executes sovereignty validations on any modified markdown files, alerting the operator immediately of any structural lint errors.
