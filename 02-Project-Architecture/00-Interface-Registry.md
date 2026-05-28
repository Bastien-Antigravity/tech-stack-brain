---
microservice: tech-stack-brain
type: architecture
status: active
tags:
- '#service/tech-stack-brain'
- '#type/architecture'
- '#state/active'
- '#zone/3-fleet'
---
# 🗺️ Cross-Repo Interface Registry

> "The Source of Truth for all FFI, gRPC, and Socket boundaries in the Bastien-Antigravity fleet."

## 📜 The Facade Law (Enforcement)
All cross-repository communication **MUST** be registered here. Any change to these interfaces requires an **ADR (Architectural Decision Record)** and a version bump in `VERSION.txt`.

---

## 🔌 1. Low-Level FFI Boundaries
These interfaces allow Python/Go to call high-performance Rust/C++ logic directly.

| Interface Name | Provider Repo | Consumer Repos | Protocol | Status |
| :--- | :--- | :--- | :--- | :--- |
| **SafeSocket** | `safe-socket` | `market-observer`, `mt5-gateway` | C-ABI / FFI | ✅ Active |
| **UniversalLogger**| `universal-logger`| ALL | FFI / Shared Lib | ✅ Active |
| **ConfigBridge** | `distributed-config`| ALL | FFI / YAML | 🛠 In-Progress |

---

## 📡 2. Fleet Networking (RPC/Events)
High-level service-to-service communication.

| Interface Name | Provider Repo | Consumer Repos | Protocol | Port |
| :--- | :--- | :--- | :--- | :--- |
| **NATS Bus** | `docker-deployment`| ALL | Pub/Sub | 4222 |
| **RAG-Engine** | `09-RAG-Engine` | AI Agents | MCP (stdio) | N/A |
| **ConfigServer** | `config-server` | Microservices | gRPC / HTTP | 50051|
| **LogServer** | `log-server` | ALL | gRPC | 50052|

---

## 📦 3. Data Schemas (Shared)
Centralized definitions for data structures.

| Schema Name | Path | Format | version |
| :--- | :--- | :--- | :--- |
| **Orderbook-V1** | `orderbook-aggregator/capnp/`| Cap'n Proto | 1.0.2 |
| **Telemetry-V2** | `universal-logger/proto/` | Protobuf | 2.1.0 |
| **Audit-Schema** | `07-Core-KMS/schemas/` | JSON-Schema | 1.0.0 |

---

## 🛠️ Update Protocol
1. **Architect** identifies a new contract during the Blueprint phase.
2. **Developer** implements the FFI/gRPC layer.
3. **Fleet Architect** verifies the Port/Socket alignment in Docker.
4. **Registry Update**: This file is updated before the final "Mission Sign-off."

---
*Reference: [[03-Tech-Stack/02-Project-Architecture/01-Facade-Pattern]], [[03-Tech-Stack/02-Project-Architecture/08-Networking-Protocols]], [[ADR-001-Safe-Socket-Protocol]]*
