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
# 📐 01 - Obsidian Brain & Repository Organization

This note governs the structural organization, Git submodule integration, and mandatory file layouts across the Bastien-Antigravity master vault and microservice repositories.

---

## 🏛️ 1. Conceptual Paradigm: Nested Capability stack

The master `obsidian-brain` vault is built on a **Conceptually Nested Capability Stack** (`00` to `09`).

```
obsidian-brain (Workspace Root)
├── 00-AI-Orchestration/      # L00: Boot, Intake, & YAML workflows
├── 01-Strategic-Nexus/       # L01: Strategy, Audits, & Rejections
├── 02-Business-BDD/          # L02: Gherkin specs & Domain Glossary
├── 03-Tech-Stack/            # L03: Coding style, Standards, & Facades
├── 04-Rapid-Prototyping/     # L04: Spikes, experiments, and labs
├── 05-Fleet-Operation/       # L05: Ops, git control, & deployments
├── 06-Microservices/         # L06: Architecture Hub notes mapping repos
├── 07-Core-KMS/              # L07: Playbooks & Tag Taxonomies
└── 08-RAG-Engine/            # L08: Local vector database & code search
```

### 🧱 Key Principles
*   **The Filesystem Merge:** While folders (`00-AI-Orchestration`, `01-Strategic-Nexus`, etc.) represent independent Git submodules, they merge into a single local directory hierarchy when checked out in the master workspace.
*   **Context Isolation:** By separating concerns into double-digit directories, we limit the active search space of our AI agents. Agents are configured to only load the capability folders relevant to their task, preventing reasoning drift and token blowup.
*   **Downstream Upgradability:** Lower-numbered layers (like L00 and L01) have zero dependencies on higher-numbered layers. The vault can boot even if submodules like L06 or L08 are missing.

---

## 📦 2. Mandatory Files in Every Submodule Module

To ensure that each Git submodule can be developed and audited in isolation, every capability folder (L00 through L08) **MUST** contain the following structural files:

### 1. `README.md`
*   **Purpose:** Describes the role of the submodule within the ecosystem, the repository URL, and the active branch.

### 2. `AI-Init.md`
*   **Purpose:** The bootstrapping prompt that must be copied and pasted whenever starting a standalone AI session directly inside the submodule directory. It tells the agent how to initialize context.

### 3. `AI-Project-DNA.md`
*   **Purpose:** Lists the local constraints, naming conventions, and technology restrictions specific to this submodule.

### 4. `AI-Session-State.md`
*   **Purpose:** The local session checklist and state log. It functions as a hard-stop context block to prevent memory loss across sequential chat runs.

### 5. `Role-Prompts/` (Folder)
*   **Purpose:** Contains the prompts of the agents who primarily work at this level (e.g., [Prompt-QA.md](../../02-Business-BDD/Role-Prompts/04-QA/Prompt-QA.md) belongs inside `02-Business-BDD/Role-Prompts/04-QA/`).

### 6. `quick-overview/` (Folder)
*   **Purpose:** Houses human-only onboarding documentation. It must contain:
    *   `Architecture-Overview.md`, `Features-Behavior.md`, `Testing-Playbook.md`, and `General-Misc.md`.
    *   **Strict Ignore Files:** `.aiignore`, `.mcpignore`, and `.geminiignore` configured to prevent AI agents from reading this folder (saving context tokens).

---

## 🤫 3. Hidden Rules of Repository Organization

> [!IMPORTANT] THE PRECEDENCE RULE
> When compiling agent prompts, the compiler (`convert_agents.py`) scans folders in order of capability precedence: `01-Strategic-Nexus` ➡️ `02-Business-BDD` ➡️ `03-Tech-Stack` ➡️ `07-Core-KMS`. If a prompt file exists in a submodule (e.g., L02 QA), it **overrides** the legacy prompt inside L07 KMS.

> [!TIP] THE STATE ISOLATION STANDARD
> Submodules must remain stateless relative to the overall workspace launcher control, but carry local session status (`AI-Session-State.md`) to support standalone micro-development.

> [!CAUTION] OCCAM'S RAZOR FOR SCHEMAS
> Avoid adding a double-digit folder for a new service unless it represents a distinct capability level. Code, schemas, and directories are liabilities; keep the vault hierarchy flat and delete obsolete placeholders quickly.

---

## 💻 4. Coding Rules for Orchestration & Base Scripts

All automation and orchestration launcher scripts inside `08-Base-Scripts/` must adhere to these strict rules:

### A. The Virtual Environment Re-Execution Ritual
To prevent dependency errors when run directly from the native shell, every Python script must contain a venv re-execution block at the top:
```python
import os, sys
_venv_dir = os.path.dirname(os.path.abspath(__file__))
while _venv_dir and _venv_dir != '/' and not os.path.exists(os.path.join(_venv_dir, ".venv")):
    _parent = os.path.dirname(_venv_dir)
    if _parent == _venv_dir:
        break
    _venv_dir = _parent
_venv_python = os.path.join(_venv_dir, ".venv", "bin", "python3") # (or python.exe on Windows)
if os.path.exists(_venv_python) and not os.path.samefile(sys.executable, _venv_python):
    os.execl(_venv_python, _venv_python, *sys.argv)
```

### B. Standard Output Encoding Standardization
Ensure standard output streams are configured to `utf-8` to prevent runtime crashes when printing emojis or special characters on Windows CLI boundaries:
```python
from sys import stdout as sysStdout
if sysStdout.encoding != 'utf-8':
    try:
        sysStdout.reconfigure(encoding='utf-8')
    except (AttributeError, Exception):
        pass
```

### C. Zero-Dependency Mandate
Orchestration launchers must rely only on Python's standard library (e.g., `os`, `sys`, `subprocess`, `re`, `json`) or highly standard modules like `yaml` and `dotenv`. Avoid importing custom code modules from other microservices to prevent import loop panics.
