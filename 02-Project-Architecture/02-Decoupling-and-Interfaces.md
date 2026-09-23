---
type: architecture
status: active
microservice: ecosystem-wide
title: Component Decoupling via Interfaces
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# 02 - Component Decoupling via Interfaces

## Rules
- **Strict Interface Usage**: Business logic must NEVER depend on concrete implementations (drivers).
- **Location**: All core interfaces must reside in `src/interfaces/`.
- **Naming Convention**: Interfaces MUST use language-idiomatic descriptive nouns without an `I` prefix (e.g., `Broker`, `Storage`, `Publisher`). Note: Legacy interfaces such as `ILogger` in universal-logger are maintained for backwards compatibility.
- **Dependency Injection**: Concrete types must be injected into the Facade/Engine using Factory patterns (`src/factories/`).

## Relationship
This enables the [[01-Facade-Pattern]] to swap dependencies without breaking core domain logic.
