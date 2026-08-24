---
microservice: 08-Base-Scripts
type: note
status: active
tags:
- '#service/08-Base-Scripts'
- '#type/note'
- '#state/active'
- '#zone/3-fleet'
---# 🚀 SDK & Agent Guide

## 🤖 Role-Prompt Personas
The system dynamically loads agent personalities from `07-Core-KMS/Role-Prompts`. 
Instead of manual conversion, the **`PersonaManager`** reads markdown files directly and injects the mandatory **[SCAN]** restoration block for context integrity.

## 📡 RAG Integration
The **09-RAG-Engine** is connected via the **Model Context Protocol (MCP)**.
*   **Automatic Registration**: The `MCPManager` detects the RAG server and registers it in your AI client settings (`settings.json`).
*   **Firewall Isolation**: Based on the active Mode (1-4), the `MCPManager` dynamically restricts which folders are visible to the agent, providing a first layer of hardware-level isolation.

## 🎯 Creating Workflows
You can automate complex tasks by creating YAML files in `00-AI-Orchestration/Workflows/`.

### Example `audit-and-fix.yaml`:
```yaml
name: Audit and Fix
description: Scan for issues and fix them.
steps:
  - name: Audit
    action: audit
  - name: Fix
    action: prompt
    persona: developer
  - name: Verify
    action: shell
    params:
      cmd: npm test
```

## 🔄 Stateful Interaction (LangGraph)
For tasks requiring loops (e.g., "retry if tests fail"), use `src/core/graph_workflow.py`. This formalizes agent handoffs through a **Shared State** object, allowing agents to collaborate without losing context.
