---
title: Ecosystem Taxonomy & Repository Categorization Guide
version: 0.0.1
classification: Orchestration
last_updated: 2026-08-05
microservice: 03-Tech-Stack
type: overview
status: active
tags:
- '#service/03-Tech-Stack'
- '#type/overview'
- '#state/active'
- '#ai/ignore'
---
# Ecosystem Taxonomy & Classification Guide

This document establishes the official architectural boundaries and classification rules across the Bastien-Antigravity ecosystem. All AI agents, IDE tools, and human contributors must strictly observe these distinctions when reading, modifying, or creating components.

---

## 1. Version Policy
* **Universal Workspace Version**: All repositories across the ecosystem adhere strictly to Version `0.0.1`.
* **Internal Dependency Alignment**: All internal module imports in `go.mod` (e.g., `github.com/Bastien-Antigravity/*`) must reference `v0.0.1`.
* **Local Development Overrides**: Local relative `replace` directives (`=> ../<repo>`) are maintained for multi-repo local development and automatically sanitized by CI for isolated single-repo builds.

---

## 2. Repository Classifications

The ecosystem repositories are divided into three distinct functional tiers:

### Tier 1: Shared Libraries (SDKs, Protocols & Toolboxes)
Shared cross-language packages, transport protocols, and CGO bridges imported or linked by microservices. **Libraries do NOT run as standalone daemons or containers.**

* **microservice-toolbox**
  * *Purpose*: Cross-language utilities for configuration loading, network dialing, retry policies, and application lifecycle bootstrap.
  * *Languages*: Go, Python, Rust.
* **universal-logger**
  * *Purpose*: Standardized logging interface, CGO bridge, and facade linking polyglot code to the logging system.
  * *Languages*: Go, Python, Rust, C++, VBA.
* **flexible-logger**
  * *Purpose*: Underlying high-performance log engine, file appender, and console formatter core.
  * *Languages*: Go.
* **distributed-config**
  * *Purpose*: Dynamic configuration client SDK, RCU lock-free atomic pointer state manager, and CGO bridge.
  * *Languages*: Go, Python, Rust, C++, VBA.
* **safe-socket**
  * *Purpose*: Framed TCP socket transport protocol implementation, framing, and identity extraction library.
  * *Languages*: Go.

---

### Tier 2: Level 1 Microservices (Independent Infrastructure & Domain Daemons)
Standalone, executable daemons and web applications that expose network ports, run containerized, manage database state, or handle specific business domain functions.

#### A. Core Platform Daemons (Base 14 Platform — `is_core: true`)
* **config-server** — Ports `3306` (SafeSocket TCP) / `3307` (gRPC) / `3308` (REST)
  * *Role*: Centralized configuration store and live sync broadcast server.
* **log-server** — Ports `9020` (SafeSocket TCP) / `9021` (gRPC)
  * *Role*: Centralized log ingestion and stream aggregation server.
* **notif-server** — Ports `1026` (SafeSocket TCP) / `1027` (gRPC) / `1029` (REST)
  * *Role*: Centralized notification dispatch server (Discord, Telegram, Webhooks).
* **tele-remote** — Port `1863` (gRPC/Telegram)
  * *Role*: Telegram-based remote administration, command execution, and gRPC gateway.
* **watchdog-agent** — Port `9095` (REST/OpenMFE)
  * *Role*: System health supervisor, heartbeat monitor, and process restarter daemon.
* **web-interface** — Port `5000` (HTTP)
  * *Role*: Central web UI dashboard, system health monitor, and OpenMFE host.

#### B. Domain Microservices (Trading & Analytics — `is_core: false`)
These domain-specific services are developed and deployed on top of the base platform:
* **ontime-scheduler** — Port `8080` (HTTP) — Cron job scheduler and task runner daemon.
* **data-ingestor** — Market & trade data ingestion daemon (NATS).
* **orderbook-aggregator** — L2/L3 depth orderbook aggregation engine (NATS).
* **technical-analysis** — Technical indicator computation engine (SQLite/NATS).
* **fundamental-analysis** — Fundamental market data processor (REST).
* **market-observer** — Real-time market surveillance daemon (NATS).
* **enhanced-backtesting** — Quantitative strategy backtesting engine (REST).
* **mt5-gateway** — MetaTrader 5 terminal gateway interface (gRPC).
* **demo-surface-vol** — Volatility surface demo service (REST).

---

### Tier 3: Supporting & Orchestration Repositories
* **sandbox-testing** — E2E test scenarios, chaos testing, and integration runner.
* **docker-deployment** — Master Docker Compose manifests and deployment scripts.
* **obsidian-brain** — System documentation, agent factory, and fleet orchestration hub.

---

## 3. Rules for AI Agents & Developers

1. **Do NOT add server entrypoints to Libraries**:
   * Libraries (`microservice-toolbox`, `universal-logger`, `distributed-config`, `safe-socket`, `flexible-logger`) must remain pure reusable packages. Do not add standalone server main daemons or port listeners into library repositories.

2. **Do NOT embed library implementations directly into Microservices**:
   * Level 1 Microservices must import shared functionality via library packages (`github.com/Bastien-Antigravity/<library>`), relying on standard interfaces.

3. **Registry Awareness**:
   * Refer to `00-Repo-Control/service-registry.json` and `00-Repo-Control/inventory.json` for exact port mappings, image names, and classification metadata (`repo_type`).
