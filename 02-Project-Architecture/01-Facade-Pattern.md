---
type: architecture
status: active
microservice: ecosystem-wide
title: "The Facade Pattern"
---

# 01 - The Facade Pattern (SystemFacade)

## Architectural Philosophy
Our microservices are designed for high throughput and long-term maintainability using **Clean Architecture** principles and the **Facade Pattern**.

## Rules
- Every microservice must have a central orchestrator, usually named `SystemFacade` or a domain-specific equivalent (e.g., `Ingestor`, `Manager`).
- **Location**: `src/facade/` or `src/<domain>/`.
- **Responsibility**: It is the ONLY component that coordinates between different sub-packages. Lower-level packages (storage, network, serializers) must NEVER talk to each other directly; they must communicate via the Facade or through interfaces.

## Dependencies
This core pattern relies strictly on [[02-Decoupling-and-Interfaces]].
