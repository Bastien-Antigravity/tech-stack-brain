---
type: architecture
status: active
microservice: ecosystem-wide
title: "Component Decoupling via Interfaces"
---

# 02 - Component Decoupling via Interfaces

## Rules
- **Strict Interface Usage**: Business logic must NEVER depend on concrete implementations (drivers).
- **Location**: All core interfaces must reside in `src/interfaces/`.
- **Naming Convention**: All interfaces MUST be prefixed with a capital `I` (e.g., `IBroker`, `IStorage`, `IPublisher`).
- **Dependency Injection**: Concrete types must be injected into the Facade/Engine using Factory patterns (`src/factories/`).

## Relationship
This enables the [[01-Facade-Pattern]] to swap dependencies without breaking core domain logic.
