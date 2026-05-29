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
# 📐 Level 02 - Business BDD

This document defines the architecture, governance principles, and management scripts for **Level 02: Business BDD** within the Bastien-Antigravity ecosystem.

---

## 🏛️ 1. Magnitude: Domain Specifications & Ubiquitous Language (Scale: System Boundaries)

Level 02 translates high-level strategic directives from Level 01 into formal, unambiguous behavior contracts that bridge business stakeholders with technical implementers.

*   **Level Classification**: **Contextual Override**. Behavior specifications, glossaries, and the QA specialist prompt override generic fallbacks when running within BDD context.
*   **Abstractions Governed**: Ubiquitous domain vocabularies (Domain Glossary), acceptance criteria, and Gherkin feature specifications (Given/When/Then).
*   **Cognitive Scope**: System boundary and specifications scope. It defines the "WHAT" of the system without prescribing code details.
*   **Authority Limit**: The single source of truth for application behavior; any coding implementation (L03) or active microservice execution (L06) must pass the behavior specs defined at this level.

---

## 🧱 2. Merged Filesystem & Git Submodule Colocation

*   **Submodule Mapping**: Maps physically to the `02-Business-BDD` Git repository.
*   **Logical Merge**: Mounts inside the double-digit stack hierarchy of the master workspace:
    ```
    obsidian-brain (Workspace Root)
    └── 02-Business-BDD/          # Merged repository mount
        ├── 01-Domain-Glossary/   # Ubiquitous domain dictionary (Glossary)
        ├── 02-Behavior-Specs/    # Gherkin G/W/T specifications
        ├── Templates/            # Standardized spec scaffolding templates
        └── Role-Prompts/         # Colocated specialist agent prompts (QA)
    ```
*   **Colocation Rule**: All specification templates and role prompts specific to QA testing (like the QA Specialist prompt) are physically attached (stored) inside the L02 repository, ensuring they check out together.
*   **Stateless Portability**: Submodule is entirely self-contained; links point to local sibling directories to support standalone development.

---

## ⚙️ 3. Runnable Isolation & Progressive Dependencies

Level 02 is progressively runnable and requires preceding levels to be present:
*   **Required Dependencies**: Requires **Level 00 (AI Orchestration)** (for active session variables) and **Level 01 (Strategic Nexus)** (for strategic anti-backlogs and guidelines) to be checked out and present in the filesystem.
*   **Runnable Isolation**: Once L00 and L01 are loaded, L02 behavior specs can be drafted, refined, and validated in isolation without needing any active code compilers or microservice deployments.

---

## 🐍 4. Python Management & Automation Suite

Level 02 is managed and verified by the following tools:

### 🤖 The QA Specialist Agent
*   **Role Prompt**: [Prompt-QA.md](../../02-Business-BDD/Role-Prompts/04-QA/Prompt-QA.md) (colocated inside the L02 submodule and compiled to `.gemini/agents/qa.md`).
*   **Operation**: Gathers requirements, writes Gherkin feature tests, and validates that proposed implementation plans fully cover all acceptance criteria.

### ⚙️ Multi-Folder Precedence Prompt Compiler (`convert_agents.py`)
*   **Script**: [convert_agents.py](../../08-Base-Scripts/convert_agents.py)
*   **Operation**: Automatically scans the `02-Business-BDD/Role-Prompts/` folder during agent compilation. Since it scans L02 before L07, the colocated QA Specialist prompt automatically overrides the default/fallback QA prompt inside L07 KMS.
