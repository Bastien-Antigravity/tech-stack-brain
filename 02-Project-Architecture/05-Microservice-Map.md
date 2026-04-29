---
type: reference
status: active
microservice: ecosystem-wide
title: "Ecosystem Service Map"
---

# 05 - Ecosystem Service Map

The platform consists of the following services and libraries:

| Repository | Language | Role |
|---|---|---|
| `config-server` | Go | Centralized config distribution via gRPC |
| `data-ingestor` | Go | Market data ingestion from exchanges |
| `market-observer` | Go | Real-time market analysis and monitoring |
| `orderbook-aggregator` | Go | Order book aggregation and scalping signals |
| `technical-analysis` | Go | Technical indicator computation engine |
| `tele-remote` | Go | Telegram bot interface for remote control |
| `notif-server` | Go | Notification routing (Telegram, email) |
| `web-interface` | Go | Web dashboard and PostgreSQL browser |
| `log-server` | Rust | Centralized logging server (TCP + gRPC) |
| `enhanced-backtesting` | Python | Strategy backtesting engine |
| `fundamental-analysis` | Python | Stock fundamental analysis & scoring |
| `microservice-toolbox` | Go/Rust/Python | Shared config, CLI, networking primitives |
| `universal-logger` | Go/C++ | Standardized logging facade and bootstrap |
| `distributed-config` | Go | Configuration loading, env expansion, sync |
| `safe-socket` | Go/Python | Cap'n Proto transport for log messages |
| `flexible-logger` | Go | Legacy log processing engine / log routing |
| `docker-deployment` | Docker | Production docker-compose orchestration |
| `testing-sandbox` | Shell | Integration and resilience testing harness |
