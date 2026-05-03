---
title: "CI/CD and Lifecycle"
type: architecture
status: active
microservice: ecosystem-wide
---

## 📐 CI/CD and Lifecycle

### 🏛️ Definition Layer
This document defines the high-level architectural requirements for CI/CD. For the **execution** protocols and stage-by-stage implementation details, see **[[fleet-operation-brain/05-Fleet-Strategy/02-CI-Protocols|📡 Fleet CI Protocols]]**.

## Architectural Rule
Container images are published to **GitHub Container Registry**. `Watchtower` is used to poll for new images and auto-update containers.

## Motivation (Why?)
- Continuous Delivery: Automates the deployment process.
- Reliability: Testing sandbox validates resilience before production updates.

## Examples
- **Watchtower**: Polls every 300s. Labels allow opting out (e.g., `timescale-db`).
- **Testing**: `testing-sandbox` contains integration scenarios and `run_resilience_test.sh`.
