# Documentation Standards: Diagrams, Schemas & Records

## Architectural Documentation
We maintain high-level topological records inside the `/doc` directory of every microservice.

### 1. ASCII Diagrams
- **Role**: Every repository must contain an architectural overview in ASCII format within the `/doc` directory (e.g., `doc/architecture.txt` or `ARCHITECTURE.md`).
- **Explanation**: This diagram must detail the Data Flow schemas and OHLCV Data Models whenever the architecture evolves.
- **Tools**: Use `monodraw` or standard text-based diagram tools for consistent layout.

### 2. ARCHITECTURE.md
- **Role**: Each shared library (`universal-logger`, `distributed-config`, `safe-socket`, `flexible-logger`, `microservice-toolbox`) MUST have an `ARCHITECTURE.md` at its root.
- **Content**: Overview of internal package structure, key interfaces, dependency chain, and design decisions.

### 3. Protocol Schemas
- **Cap'n Proto**: Fast serialization schemas are stored in the `/capnp` directory at the root (used by `data-ingestor`, `log-server`, `safe-socket`).
- **Protobuf**: gRPC protocol definitions are stored in `src/grpc_control/` (Go) or `proto/` (Rust/other).
- **JSON**: Data models must always provide clear `json` tags (Go) or `serde` derive macros (Rust) for consistent REST/WebSocket serialization.

### 4. README.md
- **Every repository** should have a README.md explaining:
  - What the service does
  - How to build and run it
  - Dependencies on other ecosystem services
  - Environment variables required

### 5. TESTING.md
- Shared libraries should include a `TESTING.md` documenting:
  - How to run unit tests
  - Integration test setup requirements
  - Known test fixtures or mocks

### 6. Change Logs & TODOs
- **File**: `todo/` directory or `README.md` must be maintained at the root to track in-progress features or issues.
- **Status Reporting**: All major architectural changes MUST be documented in the repository's `ARCHITECTURE.md` file.

### 7. Technical Walkthroughs
- Use **Walkthrough** documents for any major features or integrations that require manual verification.
- **Recordings**: Screenshots or recordings of the UI/Terminal behavior are encouraged for documentation.

### 8. Prompt Directory
- The `prompt/` repository contains modular AI system prompts for coding assistants.
- These prompts document the ecosystem's architecture, coding conventions, and library APIs.
- **Update Rule**: When a library API changes or a new service is added, update the relevant prompt files in `prompt/`.

---

## Standardized Repository File Structure
Every repository in the ecosystem MUST contain:

| File | Purpose |
|------|---------|
| `README.md` | User-facing documentation |
| `ARCHITECTURE.md` | System design deep-dive |
| `AI-Session-State.md` | AI context persistence (at root) |
| `AI-Init.md` | AI onboarding beacon (at root) |
| `.github/` | CI/CD workflows |
| `.gitignore` | Git exclusions |

Optional but recommended:
| File | Purpose |
|------|---------|
| `TESTING.md` | Test instructions |
| `TODO.md` | Pending tasks |
| `Makefile` | Build automation (Go repos) |
| `Dockerfile` | Container build (server repos) |
| `.dockerignore` | Docker build exclusions |

## Commit Conventions
- **Format**: Conventional Commits: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`
- **Scoping**: `feat(config-server): add gRPC support`
- **Branch Strategy**: `develop` → `main` (merge, never rebase)
- **Protected Branches**: Both `develop` and `main` are protected against force push and deletion.

## Dataview YAML Frontmatter
All Obsidian-visible docs must include standardized YAML:
```yaml
---
title: "Document Title"
type: {architecture|repository|session-state}
status: active
microservice: {repo-name|ecosystem-wide}
---
```
