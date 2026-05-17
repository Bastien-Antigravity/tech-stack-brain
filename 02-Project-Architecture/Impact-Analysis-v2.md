---
type: legacy
status: active
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#service/tech-stack-brain'
- '#state/active'
- '#type/legacy'
microservice: ecosystem-wide
---
# 🔍 Impact Analysis: Global Architecture Rules Expansion (v2.1)

## 🛠️ Summary of Changes
Implemented 6 new core rules approved by the AI Squad:
1.  **Ghost-Protocol** (Failure Isolation)
2.  **Mission-Traceability** (Cross-Service Trace IDs)
3.  **State-Snapshots** (gRPC Integrity Checks)
4.  **AI-Ready Docstrings** (LLM-Optimized Context)
5.  **Standardized Program Naming** (Toolbox `GetServiceName()`)
6.  **Data Sovereignty** (Dedicated DB schemas/folders)

---

## ⚠️ Side Effects Analysis

### 1. Ghost-Protocol
*   **Latency Clipping**: Hard 5s deadlines might affect heavy data backfills.
*   **Stale Data**: Fallback strategies need careful "data-is-stale" marking.

### 2. Mission-Traceability
*   **Metadata Overhead**: Propagating IDs adds minor (1-2%) performance overhead.

### 3. State-Snapshots
*   **Serialization Load**: High-memory services might experience GC pauses during snapshots.

### 4. AI-Ready Docstrings
*   **Refactor Debt**: Requires manual/AI sweep of all interfaces.

### 5. Standardized Program Naming
*   **Toolbox Dependency**: Requires upgrade to `microservice-toolbox` v1.3.0+.
*   **Executable Mapping**: Services must ensure their binary names are descriptive (e.g., `data-ingestor` instead of `main`).

### 6. Data Sovereignty
*   **Migration Effort**: Services currently using the `public` schema or root folders must be migrated.
*   **Permissions**: DB users must have `CREATE SCHEMA` or specific schema permissions granted.

---

## 📈 Maintainability Analysis
*   **Unified Auditing**: Standard naming makes it trivial to map a log line to a DB table and a file folder.
*   **Lean Cleanup**: The Purger can now safely delete all service-related assets by simply following the Program Name.
*   **AI Context Loading**: `AI-CONTEXT` tags significantly reduce the token cost and time for AI agents to "understand" a new codebase.

## ✅ Recommendation
Update all templates in `04-Templates` to include the standard `GetServiceName()` and schema setup.
