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
# 📐 Level 04 - Rapid Prototyping

This document defines the architecture, governance principles, and management scripts for **Level 04: Rapid Prototyping** within the Bastien-Antigravity ecosystem.

---

## 🏛️ 1. Magnitude: Sandbox Experimentation & Spikes (Scale: Trial & Research Playground)

Level 04 provides a sandbox area for **quick research spikes, experiments, and labs**. It isolates experimental code from clean production codebases, preventing early technical debt and packaging experiments cleanly.

*   **Level Classification**: **Sandbox Spikes**. Ephemeral experiments and research files that do not affect the main production codebase.
*   **Abstractions Governed**: Spikes, prototypes, temporary proof-of-concepts, and lab evaluations.
*   **Cognitive Scope**: Short-lived experimentation. Ingests long LLM chat conversations, clones/stubs code inside dedicated root-level workspaces, performs comparisons/merging, and outputs ecosystem merge proposals that can be accepted, refused, saved (moved to experiments/ where they are ignored), or completely removed.
*   **Authority Limit**: Highly permissive. Spikes are allowed to bypass standard production lint gates or strict unit testing requirements, but must be "graduated" under Level 02 BDD standards before merging into production.

---

## 🧱 2. Merged Filesystem & Git Submodule Colocation

*   **Submodule Mapping**: Maps physically to the `04-Rapid-Prototyping` Git repository.
*   **Logical Merge**: Mounts within the double-digit stack hierarchy of the master workspace:
    ```
    obsidian-brain (Workspace Root)
    └── 04-Rapid-Prototyping/       # Merged repository mount
        ├── experiments/            # Archive directory for saved spikes (ignored by RAG/AI)
        ├── Templates/              # Experiment templates
        ├── Template-Experiment.md  # Standard experiment template
        └── archive.py              # Colocated packaging script
    ```
*   **Colocation & Sandboxing Rule**: All experimental scripts, scratch folders, and archive utilities are stored inside the L04 submodule. **For every new test, a dedicated sandbox directory must be created at the root of `04-Rapid-Prototyping/`** to remain accessible to the AI during development, and archived to `experiments/` upon completion.
*   **Stateless Portability**: Contains local `.gitignore` and `.aiignore` configurations to prevent temporary spike data from polluting the global workspace context.

---

## ⚙️ 3. Runnable Isolation & Progressive Dependencies

Level 04 is progressively runnable and requires preceding levels to be present:
*   **Required Dependencies**: Requires **Level 00 (AI Orchestration)** (for modes), **Level 01 (Strategic Nexus)** (for strategic vision), **Level 02 (Business BDD)** (for requirements), and **Level 03 (Tech Stack)** (for base formatting conventions) to be checked out and present in the filesystem.
*   **Runnable Isolation**: Once L00 to L03 are verified, spikes can be created, run, and evaluated in the L04 sandbox in isolation without compiling main microservice clusters.

---

## 🐍 4. Python Management & Automation Suite

Level 04 is managed and audited by the following tools within a local `.venv` virtual environment:

### 📄 Spikes & Experiment Template (`Template-Experiment.md`)
*   **Template**: [Template-Experiment.md](../../04-Rapid-Prototyping/Template-Experiment.md) (colocated inside L04).
*   **Operation**: Bootstraps the experiment documentation, stating objectives, test parameters, and graduation checklist.

### 🧪 Sandbox Manager (`lab_manager.py`)
*   **Script**: [lab_manager.py](../../04-Rapid-Prototyping/lab_manager.py) (colocated inside L04).
*   **Operation**: Automates the creation of isolated sandboxes, cloning target repositories from the fleet, and extracting code stubs for comparative analysis.

### 🧹 Archive Utility (`archive.py`)
*   **Script**: [archive.py](../../04-Rapid-Prototyping/archive.py) (colocated inside the L04 submodule).
*   **Operation**: Automates the packaging and archiving of resolved experiments, moving them to deep storage once their lessons are integrated into the main fleet.
