---
microservice: tech-stack-brain
type: moc
status: active
tags:
- '#service/tech-stack-brain'
- '#type/moc'
- '#state/active'
- '#zone/1-nexus'
---
# 📐 Obsidian Brain Management & Progressive Capability Stack

This note centralizes the governance of the **Conceptually Nested Capability Stack**, the **Merged Filesystem Paradigm**, and the **Submodule Classification Taxonomy** that governs the Bastien-Antigravity master vault.

---

## 🏛️ 1. The Merged Filesystem & Script Colocation

The master vault operates as a single unified directory structure locally, but is physically constructed from multiple independent Git repositories (submodules) mapped to double-digit folders:

```
                     [Master Workspace Root]
                                │
   ┌──────────────────┬─────────┴────────┬──────────────────┐
   ▼                  ▼                  ▼                  ▼
00-AI-...          01-Strat-...       02-Biz-...         03-Tech-...  (Git Submodules)
```

### 🧱 Core Structural Rules
1.  **Script & Prompt Colocation**: To ensure each submodule can be checked out and developed in isolation, **all scripts, templates, and agent prompts specific to a capability level MUST be physically stored inside that submodule's folder**. When a level is loaded, its tools are instantly available.
2.  **Sequential Dependencies**: Lower-digit levels are base dependencies. A given level `XX` requires all preceding levels `00` through `XX-1` to be checked out and present in the filesystem to function.
3.  **Stateless Portability**: Submodules use relative paths (e.g. `../02-Business-BDD/`) instead of absolute workspace locations, allowing any subset of the stack to boot and run.

---

## 🏷️ 2. Submodule Classification Taxonomy

Each capability level belongs to a specific architectural classification, defining its state mutability and scope of authority:

### A. Mutable Active Local State
*   **Purpose**: Tracks the real-time progress, variables, and mode gates of the current development session.
*   **Mutability**: Highly mutable; updated constantly during execution.
*   **Examples**: `00-AI-Orchestration` (Session State, Mode Manual).

### B. Contextual Overrides
*   **Purpose**: Houses specific guidelines, Gherkin specs, and custom agent personas that override default templates when working within a particular domain context.
*   **Mutability**: Semi-mutable (updated as specifications and technical choices evolve).
*   **Examples**: `01-Strategic-Nexus` (Strategy audits), `02-Business-BDD` (BDD specifications & specialized QA agent), `03-Tech-Stack` (Coding standards & developer agents).

### C. Default Immutable / Fallback Templates
*   **Purpose**: Serves as the global system library, housing default agent prompts, taxonomy definitions, and playbooks. These act as read-only fallbacks.
*   **Mutability**: Immutable (only updated during master system refactors).
*   **Examples**: `07-Core-KMS` (Default Agent Roles, tag taxonomies).

### D. Sandbox Spikes
*   **Purpose**: Isolated playground for spikes, lab experiments, and research.
*   **Mutability**: Mutable and ephemeral.
*   **Examples**: `04-Rapid-Prototyping` (Labs).

### E. Operational Realizations & Hubs
*   **Purpose**: Directories and command centers mapping active code repositories and deployment pipelines to the vault.
*   **Mutability**: Registry-based (updated when new microservices are registered).
*   **Examples**: `05-Fleet-Operation` (submodule registries, deploy logs), `06-Microservices` (operational hubs).

### F. Cognitive Retrieval Memory
*   **Purpose**: Local sqlite/vector database indexing the entire workspace for semantic search.
*   **Mutability**: Auto-updated via background debounced watchers.
*   **Examples**: `09-RAG-Engine`.

---

## 🛰️ Progressive Capability Levels (Step-by-Step)

Click on each level below to explore its specific **Magnitude of Abstraction**, Classification Type, Git submodule mounting rules, progressive dependencies, and colocated scripts:

### ⚡ Base Layer
*   **[[03-Tech-Stack/01-Obsidian-Brain/00-AI-Orchestration|📐 Level 00: AI Orchestration]]** — *Type: Mutable Active Local State*. Magnitude: Single-Session Scope. Governs boot settings and mode switches.

### 🌌 Reflective Governance
*   **[[03-Tech-Stack/01-Obsidian-Brain/01-Strategic-Nexus|📐 Level 01: Strategic Nexus]]** — *Type: Contextual Override*. Magnitude: Project Lifespan Scope. Governs anti-backlogs, audits, and Oracle agent.

### 👔 Behavioral Contracts
*   **[[03-Tech-Stack/01-Obsidian-Brain/02-Business-BDD|📐 Level 02: Business BDD]]** — *Type: Contextual Override*. Magnitude: System Boundaries Scope. Governs glossaries, Gherkin specs, and QA agent.

### 📐 Technical Rules
*   **[[03-Tech-Stack/01-Obsidian-Brain/03-Tech-Stack|📐 Level 03: Tech Stack]]** — *Type: Contextual Override*. Magnitude: Code Syntax & FFI Scope. Governs style guides and developer specialists.

### 🧪 Research Sandbox
*   **[[03-Tech-Stack/01-Obsidian-Brain/04-Rapid-Prototyping|📐 Level 04: Rapid Prototyping]]** — *Type: Sandbox Spikes*. Magnitude: Trial & Research Playground. Governs temporary spikes and labs.

### 🚀 Operations & Deployment
*   **[[03-Tech-Stack/01-Obsidian-Brain/05-Fleet-Operation|📐 Level 05: Fleet Operations]]** — *Type: Operational Realizations*. Magnitude: Cluster Scope. Governs Git submodules commands and CD pipelines.

### 🌐 Individual Realization
*   **[[03-Tech-Stack/01-Obsidian-Brain/06-Microservices|📐 Level 06: Microservices]]** — *Type: Operational Realizations*. Magnitude: Single-Service Scope. Governs microservice hub notes and startup Protocols.

### 🧠 Organizational Memory
*   **[[03-Tech-Stack/01-Obsidian-Brain/07-Core-KMS|📐 Level 07: Core KMS]]** — *Type: Default Immutable*. Magnitude: Global Ontology Scope. Governs default agent templates and the Sovereignty engine.

### 🛠️ Active Utilities
*   **[[03-Tech-Stack/01-Obsidian-Brain/08-Base-Scripts|📐 Level 08: Base Scripts]]** — *Type: Active Utility / Executable Scaffolding*. Magnitude: System-Wide Control. Governs workspace automation, environment setup, and CLI integrations.

### 🔍 Cognitive Retrieval
*   **[[03-Tech-Stack/01-Obsidian-Brain/09-RAG-Engine|📐 Level 09: RAG Engine]]** — *Type: Cognitive Retrieval Memory*. Magnitude: Vector Memory Scope. Governs vector/lexical database indexing and watchers.

---
*See Also: [[03-Tech-Stack/01-Obsidian-Brain/Obsidian-Brain-Organization|Obsidian Brain & Repository Organization]]*
