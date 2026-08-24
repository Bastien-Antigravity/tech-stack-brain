---
microservice: 08-Base-Scripts
type: note
status: active
tags:
- '#service/08-Base-Scripts'
- '#type/note'
- '#state/active'
- '#zone/3-fleet'
---# 🏛️ Architecture V2: OOP & SDK Squad Core

## 🌟 Overview
The Bastien-Antigravity Squad has been refactored from a collection of procedural scripts into a robust, Object-Oriented engine. This migration ensures reliability, formalized workflows, and industry-standard security boundaries.

## 🏗️ Core Components

### 1. The Engine (`src/core/`)
*   **`SquadOrchestrator`**: The central brain. Coordinates rituals, mode switches, and agent execution.
*   **`SquadContext`**: The state manager. Reads/Writes to `MODE-MANUAL.md` as the source of truth.
*   **`AccessController`**: The security interceptor. Enforces Mode 1/3 boundaries at the code level.
*   **`MemoryManager`**: Persistence layer. Stores all agent thoughts and exchanges in SQLite.

### 2. The SDK Interface (`providers.py`)
Direct Python integration with AI models, bypassing fragile CLI subprocesses:
*   **Gemini SDK**: Native Google Generative AI integration.
*   **DeepSeek SDK**: OpenAI-compatible adapter for DeepSeek API.

### 3. Formalized Workflows
*   **Linear Automation**: Defined in `00-AI-Orchestration/Workflows/*.yaml`.
*   **Stateful Graphs**: Powered by **LangGraph** in `src/core/graph_workflow.py` for cyclical, self-correcting logic.

## 🛡️ Security & Rights
The `AccessController` provides reliable protection:
*   **Governance Lock**: Direct modification of `07-Core-KMS` is blocked by default.
*   **Isolation**: Mode 1 strictly restricts writes to the current vault/repo.

## 📊 Monitoring
*   **Chat UI**: A professional web interface powered by `Chainlit` (`squad_ui.py`).
*   **Database**: Logs are stored in `00-AI-Orchestration/logs/squad_memory.sqlite`.
