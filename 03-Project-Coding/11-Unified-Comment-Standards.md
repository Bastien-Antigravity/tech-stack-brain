---
title: Unified Comment Standards
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# 📐 Unified Comment Standards

To ensure total clarity and rapid onboarding in our polyglot fleet, all source code MUST adhere to a unified commenting and documentation ritual.

## 🏁 The Triple-Block Header
Every source file MUST begin with a standardized header block immediately following the file-level declarations (Shebang/Package). This block provides the "Intent Context" required for both human audit and AI orchestration.

### Template:
```text
ESSENTIAL PROCESS:
A high-level description of WHAT this file does and WHY it exists. Focus on the business value or technical necessity.

DATA FLOW:
1. Input: Where does the data come from? (e.g., config, network, disk)
2. Logic: The primary transformation or decision logic.
3. Output: Where does the data go? (e.g., logs, database, downstream service)

KEY PARAMETERS:
List the 3-5 most critical configuration fields or environment variables that control this file's behavior.
```

## 🧱 Section Dividers
Use standardized horizontal dividers to separate logical blocks (e.g., Imports, Constants, Interface Implementation, Helper Functions).

| Language | Divider Pattern |
| :--- | :--- |
| **Go / Rust / C++** | `// -----------------------------------------------------------------------------` |
| **Python / VBA** | `# -----------------------------------------------------------------------------------------------` |

### Usage Rule:
- Place dividers between **every** exported function or method.
- Place a divider before major internal logic sections (e.g., `// ### INTERNAL HELPERS ###`).

## 📖 Docstrings & Inline Comments
- **Docstrings**: Required for all **Public/Exported** members.
    - Focus on the **Intent** (what it achieves) rather than the **Implementation** (how it works).
    - Include specific sections for `Args:`, `Returns:`, and `Raises:` where applicable.
- **Inline Comments**: Use sparingly.
    - **Rule of Thumb**: Only comment the "Why". If the "What" isn't clear from the code, refactor the naming conventions first.
- **Ritual Comments**: Use specialized markers for lifecycle events (e.g., `// ### STARTUP SEQUENCE ###`).

## 🏷️ Metadata Markers
Use standard markers to signal intent to AI agents and audit tools:
- `TODO`: Planned features or known technical debt.
- `FIXME`: Critical bugs requiring immediate attention.
- `NOTE`: Contextual nuance that isn't obvious from the code.
- `PERF`: Optimization notes for high-frequency hotpaths.

## 🧠 Obsidian Architecture Alignment Tags (`@obsidian [[...]]`)
To bind physical source code directly to the Obsidian knowledge vault and activate automated documentation drift detection, engineers and AI assistants MUST tag critical interfaces, entry points, and domain components with the `@obsidian` directive.

### Tag Syntax
Place the `@obsidian` tag in a line comment immediately preceding the struct, class, interface, function, or file-level header:
- **Go / Rust / C++**: `// @obsidian [[Note-Title]]`
- **Python / Shell**: `# @obsidian [[Note-Title]]`
- **VBA**: `' @obsidian [[Note-Title]]`

### When to Tag:
1. **Core Service Interfaces & Handlers**: Link exported interfaces to their architectural blueprint (e.g. `// @obsidian [[Architecture-Blueprint-DocSync]]`).
2. **Feature Implementations**: Link BDD feature entry points to their specification note (e.g. `// @obsidian [[FEAT-010-Doc-Sync]]`).
3. **Domain Entities**: Link domain models to the domain glossary (e.g. `// @obsidian [[00-Glossary]]`).

### Synchronization & Drift Detection Lifecycle
1. The **CodeDocSynchronizer** (`09-RAG-Engine`) scans `@obsidian [[...]]` tags on file save and registers `(code_id, doc_id, SHA-256)` in the PostgreSQL `alignment_links` registry.
2. When the implementation changes, the RAG engine detects hash disparity and flags the document as **drifted**.
3. Squad agents run `suggest_doc_rewrite` or `resolve_documentation_drift` to keep architecture documentation in lock-step with code.

---
*Reference: [[01-General-Naming-Conventions]], [[07-Hidden-Patterns-and-Gotchas]]*

## 🏛️ Governance & Maintenance
The integrity of our documentation is a shared responsibility, enforced by specialized roles and automated triggers.

### Roles & Responsibilities
- **Developer (Persona: Lead-Developer)**: **Primary Owner**. Responsible for authoring the Triple-Block Header and Intent-First docstrings during the development phase.
- **Sentinel (Persona: Sentinel)**: **Enforcement Owner**. Responsible for auditing code for comment compliance during the session sign-off.
- **Architect (Persona: Architect)**: **Governance Owner**. Responsible for maintaining and evolving the Comment Standards defined in this document.

### Mandatory Triggers
1. **Creation Ritual**: Mandatory upon file creation. AI agents MUST scaffold the Triple-Block Header before writing any functional logic.
2. **Logic Drift**: Mandatory update when a change modifies the `DATA FLOW` or introduces new `KEY PARAMETERS`.
3. **The Governance Gate**: Enforcement during the `close_mission.py` ritual. Commits with missing or stale headers MUST be rejected.
4. **Fleet Health Audit**: Periodic mass-scan (e.g., via `Brain-Health-Audit.py`) to identify and remediate "Intent-Drift" across the fleet.

> [!TIP]
> **AI-Intent Alignment**: Keeping the `ESSENTIAL PROCESS` and `DATA FLOW` accurate is critical for future AI agents to correctly interpret your architectural intent without deep-diving into implementation details.
