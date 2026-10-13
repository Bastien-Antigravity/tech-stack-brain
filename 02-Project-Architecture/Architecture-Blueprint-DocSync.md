---
title: "Architecture Blueprint: Code-Doc Semantic Synchronizer (FEAT-010)"
type: architecture
status: active
microservice: tech-stack-brain
tags:
- '#service/tech-stack-brain'
- '#type/architecture'
- '#state/active'
- '#zone/1-frozen'
---

# Architecture Blueprint: Code-Doc Semantic Synchronizer (FEAT-010)

## 1. System Overview
The **Code-Doc Semantic Synchronizer** is a proactive service within the RAG Engine that ensures the Obsidian documentation vault remains in lock-step with the physical codebase. It automates file mirroring, injects architectural context from the semantic graph, and extracts manual @obsidian links from source code.

## 2. Core Components

### 2.1 CodeDocSynchronizer (Service)
- **Path**: `09-RAG-Engine/src/services/alignment/synchronizer.py`
- **Role**: Orchestrator of the sync pipeline.
- **Dependencies**: 
    - `AlignmentService` (Interface)
    - `CodebaseAnalyzer` (for graph queries)
    - `RAGFacade` (for high-level orchestration)

### 2.2 Mirroring Protocol
- **Storage Location**: `${WORKSPACE_ROOT}/obsidian-brain/11-Code-Doc/`
- **Structure**: Mirrors the repository structure: `obsidian-brain/11-Code-Doc/<workspace_name>/<relative_path_to_file>.md`
- **Frontmatter Template**:
```yaml
---
source: <relative_path_to_source>
workspace: <workspace_name>
type: code-mirror
status: auto-generated
last_sync: <timestamp>
---
```

### 2.3 Intent-First Description & Graph Context Injector
- **Target Sections**:
  - `## 📝 Description`: Injects the `ESSENTIAL PROCESS` extracted directly from the source file's Triple-Block header block.
  - `## 🏗️ Architectural Context`: Contains the machine-generated graph boundaries.
- **Idempotency Markers**:
  - Start: `<!-- SYNC:START -->`
  - End: `<!-- SYNC:END -->`
- **Injected Content**:
  - **Imports/Dependencies (Outbound)**: List of internal files and symbols called/imported, annotated with their 1-line docstring/intent summary (e.g. `- [[...|HealSymlinks]] (function: calls) — *Summary intent*`).
  - **Used By/Consumers (Inbound)**: Inbound callers and consumers across the fleet.
  - **Untouchable Section**: `## 🔍 Implementation Details` (at the bottom) is strictly reserved for manual developer notes and is never altered during synchronization.

### 2.4 Tag Extraction Engine
- **Regex Standard**: `@obsidian \[\[(.*?)\]\]`
- **Logic**: Scans source files (Python, Go, Rust, etc.) for tags in comments or docstrings.
- **Registration**: Calls `AlignmentService.register_link(code_id, doc_id, code_hash)`.

## 3. Data Flow

1. **Discovery Phase**:
    - Query `CodebaseDB` for all nodes of type `file`.
2. **Mirroring Phase**:
    - For each file node:
        - Check if mirror `.md` exists in `obsidian-brain/11-Code-Doc/`.
        - If missing, create it with standard frontmatter and extracted `ESSENTIAL PROCESS`.
3. **Extraction Phase**:
    - Read source code content.
    - Compute SHA-256 hash.
    - Search for `@obsidian [[Link]]` tags.
    - For each tag found, register/update the link in `alignment_registry.db`.
4. **Injection Phase**:
    - Query `CodebaseDB` for edges related to the current file.
    - Format Markdown block with "Imports" and "Used By" sections.
    - Update the mirror `.md` file, replacing content between `<!-- SYNC:START -->` and `<!-- SYNC:END -->`.
5. **Cleanup Phase**:
    - Scan `codedoc/mirror/`.
    - Delete any `.md` file that doesn't have a corresponding node in `CodebaseDB`.

## 4. Interface Definitions

### 4.1 CodeDocSynchronizer
```python
class CodeDocSynchronizer:
    async def run_sync(self) -> SyncReport:
        """Main entry point for the sync process."""
        pass

    async def _process_file(self, file_node: Dict[str, Any]) -> None:
        """Mirror, extract tags, and inject context for a single file."""
        pass

    def _extract_tags(self, content: str) -> List[str]:
        """Regex-based tag extraction."""
        pass

    def _format_context_block(self, inbound: List[Edge], outbound: List[Edge]) -> str:
        """Generates the Markdown context section."""
        pass
```

### 4.2 AlignmentService (Existing Updates)
- Ensure `get_linked_docs` supports the heuristic mirror path check (already implemented in `SQLiteAlignmentService`).

## 5. Constraints & Standards
- **Decoupling**: No direct SQLite calls; use `CodebaseDB` or `AlignmentService` methods.
- **Performance**: Use `asyncio.to_thread` for heavy file I/O operations.
- **Logging**: Use the unified `RAGEngine` logger.
- **Idempotency**: NEVER delete content outside the `SYNC` markers in existing mirror files.

## 6. CLI Command
- `python main.py sync-docs [--workspace <name>]` (Cleanup of orphaned mirror files runs automatically on every sync)
- `python main.py index [--structure-only] [--no-structure] [--enrich-only]` (Decoupled indexing stages)
