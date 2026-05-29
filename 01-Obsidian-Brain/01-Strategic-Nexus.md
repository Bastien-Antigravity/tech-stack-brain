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
# 📐 Level 01 - Strategic Nexus

This document defines the architecture, governance principles, and management scripts for **Level 01: Strategic Nexus** within the Bastien-Antigravity ecosystem.

---

## 🏛️ 1. Magnitude: Meta-Cognitive Governance (Scale: Project Lifespan)

Level 01 governs the **strategic integrity and long-term memories** of the ecosystem. It exists above specifications and code, acting as the cognitive guardrail to prevent architectural drift.

*   **Level Classification**: **Contextual Override**. Strategy documents, anti-backlogs, and audit files override or direct the active behavior of downstream agents.
*   **Abstractions Governed**: Architectural visions, roadmap patterns, historical audits, and the registry of explicitly rejected concepts (the Anti-Backlog).
*   **Cognitive Scope**: Multi-session memory. While lower layers handle current tasks, Level 01 audits *why* decisions were made to avoid repeating resolved debates.
*   **Authority Limit**: Highest decision-making authority for architecture; any proposed changes at lower levels (BDD, Coding, Ops) must conform to Level 01 audits.

---

## 🧱 2. Merged Filesystem & Git Submodule Colocation

*   **Submodule Mapping**: Maps physically to the `01-Strategic-Nexus` Git repository.
*   **Logical Merge**: Integrates directly into the root folder structure of the master workspace:
    ```
    obsidian-brain (Workspace Root)
    └── 01-Strategic-Nexus/       # Merged repository mount
        ├── Strategy-Audit-MOC.md # Index of all strategic reports
        ├── Anti-Backlog.md       # Rejected ideas database
        └── STRAT-XXX/            # Transverse strategic audits
    ```
*   **Colocation Rule**: All templates and agent prompts specific to strategy (such as the Chronos-Oracle prompt) are physically attached (stored) inside the L01 repository, ensuring they check out together.
*   **Stateless Portability**: All links use relative paths (e.g., `[[../02-Business-BDD/01-Domain-Glossary/00-Glossary]]`) to support running L01 in isolation without absolute workspace paths.

---

## ⚙️ 3. Runnable Isolation & Progressive Dependencies

Level 01 is progressively runnable and requires preceding levels to be present:
*   **Required Dependencies**: **Level 00 (AI Orchestration)** must be checked out and present in the local filesystem to bootstrap active session state (`AI-Session-State.md`) and project configuration variables (`Project-Variables.md`).
*   **Runnable Isolation**: Once L00 is present, L01 is fully runnable. It can analyze strategy and anti-backlogs without requiring business specs (L02) or source code (L06).

---

## 🐍 4. Python Management & Automation Suite

Level 01 is governed and monitored by the following tools:

### 🤖 The Chronos-Oracle Agent
*   **Role Prompt**: [Prompt-Chronos-Oracle.md](../../07-Core-KMS/Role-Prompts/00-Oracle/Prompt-Chronos-Oracle.md) (colocated inside the L01 submodule and compiled to `.gemini/agents/oracle.md`).
*   **Operation**: Evaluates development session logs, tracks context window debt, and publishes new `STRAT-XXX` audits when architectural drift or design debt is detected.

### 🚨 Auditing and Validation (`vault-sentinel.py`)
*   **Script**: [vault-sentinel.py](../../08-Base-Scripts/vault-sentinel.py)
*   **Operation**: Analyzes Level 01 strategic audits and the anti-backlog registry to ensure that lower-level implementations do not introduce banned design patterns or duplicate solved issues.
