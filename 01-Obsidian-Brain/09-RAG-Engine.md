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
# 📐 Level 09 - RAG Engine

This document defines the architecture, governance principles, and management scripts for **Level 09: RAG Engine** within the Bastien-Antigravity ecosystem.

---

## 🏛️ 1. Magnitude: Cognitive Retrieval & Semantic Watcher (Scale: Global Vector Memory)

Level 09 provides **sovereign semantic search and automatic context watchers** for the entire workspace. Instead of loading whole notes (which blows up agent token counts), the RAG engine chunks documents dynamically and indexes them semantically.

*   **Level Classification**: **Cognitive Retrieval Memory**. Locally indexed vector database and real-time document watcher that keeps vault search completely secure and offline.
*   **Abstractions Governed**: Chunking algorithms, local offline vector storage (PostgreSQL/pgvector), embedding models (`BAAI/bge-m3`), Model Context Protocol (MCP) servers, and file-watching daemons.
*   **Cognitive Scope**: Real-time semantic document retrieval.
*   **Authority Limit**: Governs how agents query the vault's memory; any semantic query or similarity search goes through this layer.

---

## 🧱 2. Merged Filesystem & Git Submodule Colocation

*   **Submodule Mapping**: Maps physically to the `obsidian-rag-mcp` Git repository.
*   **Logical Merge**: Mounts within the root of the master workspace:
    ```
    obsidian-brain (Workspace Root)
    └── 09-RAG-Engine/             # Merged repository mount
        ├── src/                   # Python server & watcher source
        ├── requirements.txt       # Dependencies
        └── README.md              # Setup & usage guide
    ```
*   **Colocation Rule**: All embedding configurations, the python MCP server code, and watchdog watcher scripts are stored physically inside the L09 repository, ensuring they check out together.
*   **Stateless Portability**: Runs 100% offline, keeping all indexed knowledge local and secure.

---

## ⚙️ 3. Runnable Isolation & Dependencies

Level 09 is progressively runnable and requires preceding levels to be present:
*   **Required Dependencies**: Requires **Level 00** through **Level 07** to be checked out and present in the local filesystem.
*   **Runnable Isolation**: Once L00 to L07 are verified, Level 09 can spin up its local database, index all workspace documents progressively, and expose search tools to the agent squad.

---

## 🐍 4. Python Management & Automation Suite

Level 09 is executed and maintained by the following Python processes:

### 🔍 Model Context Protocol (MCP) Server
*   **Source**: [main.py](../../09-RAG-Engine/main.py) (colocated inside L09).
*   **Operation**: Standard Python server exposing tools such as `query_brain` and `find_similar_files` to any MCP-compliant agent.

### 📡 Automatic File Watcher Daemon (`watcher.py`)
*   **Source**: Located inside the `09-RAG-Engine/src/` folder (colocated inside L09).
*   **Operation**: A background process utilizing `watchdog` to monitor the workspace directories. When any note is updated, renamed, or deleted in Obsidian, it triggers a thread-safe, `0.5s` debounced update to PostgreSQL/pgvector in the background.

### 🧪 Setup and Query Test (`test_query.py`)
*   **Script**: [test_query.py](../../09-RAG-Engine/test_query.py) (colocated inside L09).
*   **Operation**: Standard testing script to execute search queries and check vector indexing accuracy offline.
