---
title: Documentation Requirements
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# 📚 Documentation Requirements

Every component of the Bastien-Antigravity fleet MUST adhere to these documentation standards to ensure long-term maintainability and AI-assisted orchestration.

## 🏁 Code Documentation (The Ritual)
All source code, regardless of language, MUST follow the **[[11-Unified-Comment-Standards|Unified Comment Standards]]**.

### The Triple-Block Header
Every file MUST start with:
1.  **ESSENTIAL PROCESS**: The high-level "Why".
2.  **DATA FLOW**: The logical path (Input -> Logic -> Output).
3.  **KEY PARAMETERS**: Critical configurations.

### Intent-First Docstrings
- Use docstrings for all exported/public members.
- Document the **Intent** (result), not the **Implementation** (process).

---

## 🏗 Repository Structure
Every repository in the ecosystem MUST contain the following standardized files at its root:

| File | Requirement | Purpose |
| :--- | :--- | :--- |
| `README.md` | Mandatory | User-facing entry point and build instructions. |
| `ARCHITECTURE.md` | Mandatory | Deep-dive into design decisions and package layout. |
| `VERSION.txt` | Mandatory | Single source of truth for semantic versioning (vX.Y.Z). Referenced by all documentation. |
| `AI-Project-DNA.md` | Mandatory | High-level behavioral summary for AI agents. |
| `AI-Session-State.md` | Mandatory | Context persistence for AI coding assistants. |
| `AI-Init.md` | Mandatory | Onboarding beacon for new agents. |
| `TESTING.md` | Mandatory | Instructions for unit and integration testing. |
| `TODO/` or `TODO.md` | Mandatory | Tracking of pending tasks and technical debt. |

### The `quick-overview/` Folder
Repositories MUST provide a `quick-overview/` directory containing markdown files for:
- `Architecture-Overview.md`
- `Features-Behavior.md`
- `Testing-Playbook.md`

---

## 🏷 Metadata & Taxonomy
All markdown documentation within the Obsidian Brain MUST include standardized YAML frontmatter.

### Taxonomy Rules
- **Service Tag**: Use `#service/[repo-name]` for repository-specific docs.
- **Global Tag**: Use `#service/ecosystem-wide` for cross-cutting standards.
- **Status**: Must be one of `active`, `skeleton`, `deprecated`, or `research`.
- **Type**: Must be one of `architecture`, `repository`, `session-state`, `moc`, or `ritual`.

### Sanitization Mandate
- **No Null Tags**: Do not use `tags: null` or empty arrays. 
- **Unique IDs**: Use `Sync-ID: [UUID]` for tracking document synchronization.

---

## 🔄 Governance Rituals
- **Sign-off**: Every session MUST be concluded by running `python3 20-Scripts/close_mission.py`. This script verifies that `AI-Session-State.md` is updated and metadata is compliant.
- **Audit**: The **Sentinel** role periodically runs `Multi-Repo-Validator.py lint` to identify technical debt and documentation drift across the fleet.

---
*Reference: [[00-Coding-Style-Guide]], [[11-Unified-Comment-Standards]]*
