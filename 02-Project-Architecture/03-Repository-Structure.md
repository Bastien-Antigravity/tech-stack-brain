---
type: architecture
status: active
microservice: ecosystem-wide
title: Repository Structure & Microservice Creation Standard
tags:
- '#zone/3-fleet'
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# 03 - Repository Structure & Microservice Creation Standard

This document governs the mandatory folder architecture, root files, and ecosystem integration standards for all microservices across the Bastien-Antigravity fleet.

---

## 1. The 10 Mandatory Root Files Checklist

Every microservice repository in the workspace **MUST** contain the following 10 root files:

| # | File Name | Purpose & Canonical Requirement |
| :-: | :--- | :--- |
| **1** | `standalone.yaml` | **Mandatory Symlink**: Points to `../docker-deployment/modes/local/config/native.yaml`. Registered in `watchdog-agent` self-healing engine. |
| **2** | `AGENTS.md` | **Autonomous Agent Operating Guide**: Documents mission, exposed capabilities, ports, build/test commands, and forbidden anti-patterns. |
| **3** | `AI-Session-State.md` | **Agent Session Context Tracker**: Contains standard YAML frontmatter tracking active tasks, mission IDs, and known issues. |
| **4** | `Dockerfile` | **Standalone Multi-Stage Build**: Conforms to `12-Docker-Deployment-Standards.md`. Clones shared library replace directives in builder stage. |
| **5** | `docker-compose.yml` | **Local Fragment Compose**: Configured with `context: .`, port mappings using `${ENV_VAR:-fallback}`, and `teleremote-network`. |
| **6** | `VERSION.txt` | **Canonical Version Identifier**: Single-line plain text file (e.g. `0.0.1`) read dynamically by `Makefile`, CI/CD pipelines, and release workflows. |
| **7** | `.golangci.yml` | **Static Analysis Rules** *(Go services)*: Configures `govet`, `staticcheck`, `ineffassign`, and suppression rules. |
| **8** | `go.mod` / `requirements.txt` / `Cargo.toml` | **Language Dependency Manifest**: Uses approved internal ecosystem SDKs (`microservice-toolbox`, `universal-logger`, `safe-socket`). |
| **9** | `Makefile` | **Standardized CLI Automation** *(Go, Rust, C++, CGO bridges)*: Uses dynamic versioning (`VERSION := $(shell cat VERSION.txt 2>/dev/null || echo "0.0.1")`) with targets `version`, `build`, `test`, `run`, and `clean`. Pure Python services rely natively on `requirements.txt`, `pytest`, and `python main.py`. |
| **10** | `README.md` | **Project Compass**: High-level repository mission and link to `AGENTS.md`. |

---

## 2. Directory Anatomy by Language

### Go Services (Primary Language)
```text
<service-name>/
├── cmd/
│   └── <service-name>/
│       ├── main.go               # Single-call bootstrap (microservice-toolbox) & lifecycle
│       └── standalone.yaml       # (Symlink if executing directly from cmd/)
├── src/
│   ├── core/                     # Central domain logic & worker controllers
│   ├── interfaces/               # Abstract interfaces (zero direct cyclic imports)
│   ├── models/                   # Shared typed structs & telemetry payloads
│   ├── config/                   # Typed capability schemas
│   ├── rest/                     # REST HTTP handlers & OpenMFE asset host
│   └── server/                   # SafeSocket TCP or gRPC network servers
├── quick-overview/               # Mandatory human onboarding documentation (see Sec. 3)
├── standalone.yaml               # Symlink -> ../docker-deployment/modes/local/config/native.yaml
├── Dockerfile                    # Multi-stage standalone build
├── docker-compose.yml            # Local fragment compose
├── AGENTS.md                     # AI agent operational prompt
├── AI-Session-State.md           # AI session memory tracker
├── .golangci.yml                 # Static analysis config
├── VERSION.txt                   # Version identifier (e.g. 0.0.1)
├── Makefile                      # version, build, test, run, clean targets
├── go.mod / go.sum               # Go modules with replace directives
└── README.md                     # High-level overview
```

### Python Services (e.g., enhanced-backtesting, fundamental-analysis, 09-RAG-Engine)
```text
<service-name>/
├── main.py                       # Application entry point using microservice-toolbox loader
├── src/
│   ├── core/                     # Domain controllers and worker execution logic
│   ├── interfaces/               # Abstract base classes (ABCs) & typing.Protocol
│   ├── models/                   # Dataclasses and M-prefixed schemas (e.g. MStatusPayload)
│   └── lib/                      # Shared helper utilities
├── tests/                        # Pytest suite (e.g. test_basic.py)
├── quick-overview/               # Mandatory human onboarding
├── standalone.yaml               # Symlink to native.yaml
├── Dockerfile                    # Containerization manifest (Python 3.12-alpine)
├── docker-compose.yml            # Local fragment compose
├── AGENTS.md                     # AI agent operational prompt
├── AI-Session-State.md           # AI session memory tracker
├── requirements.txt              # Python dependencies (microservice-toolbox, universal-logger, pytest)
├── VERSION.txt                   # Version identifier (e.g. 0.0.1)
└── README.md
```

### Rust Services (e.g., log-server)
```text
<service-name>/
├── src/
│   ├── main.rs                   # Entry point with Tokio async runtime & config loader
│   ├── core/                     # Async engines and ring/reorder buffers
│   ├── servers/                  # Tokio SafeSocket TCP listener & gRPC handlers
│   ├── models/                   # Typed structs
│   └── protocols/                # Length-prefixed framing and Cap'n Proto schemas
├── quick-overview/               # Mandatory human onboarding
├── standalone.yaml               # Symlink to native.yaml
├── Dockerfile                    # Rust multi-stage builder (protoc + capnproto)
├── docker-compose.yml            # Local fragment compose
├── AGENTS.md                     # AI agent operational prompt
├── AI-Session-State.md           # AI session memory tracker
├── VERSION.txt                   # Version identifier (e.g. 0.0.1)
├── Cargo.toml / Cargo.lock       # Cargo dependencies
├── Makefile                      # Standard CLI automation with dynamic versioning
└── README.md
```

---

## 3. Human Onboarding (`quick-overview/` — Mandatory)

Every microservice repository MUST include a `quick-overview/` folder at the root. This folder is **exclusively for human readers** and is excluded from AI agent context:

- `quick-overview/Architecture-Overview.md`: Visual graphs and explanations of internal modules.
- `quick-overview/Features-Behavior.md`: High-level summary of features and domain behaviors.
- `quick-overview/Testing-Playbook.md`: How to test this specific service (unit, integration, sandbox).
- `quick-overview/General-Misc.md`: Philosophy, operational caveats, and optimization tips.
- `quick-overview/.geminiignore`, `quick-overview/.mcpignore`, `quick-overview/.aiignore`: Mandatory ignore files ensuring AI agents do not waste context on human onboarding notes.

> [!IMPORTANT]
> AI agents MUST ignore `quick-overview/`. The **DocMaintainer** is the only agent persona responsible for updating these files after major architectural updates.

---

## 4. The 6 Ecosystem Integration Touchpoints (The Golden Fleet Standard)

When introducing or modifying a microservice, the following 6 integration touchpoints are required:

1. **`obsidian-brain/05-Fleet-Operation/00-Repo-Control/service-registry.json`**:
   Register the service name, Docker image, canonical default port, protocol, and classification in the fleet registry.
2. **`obsidian-brain/05-Fleet-Operation/00-Repo-Control/inventory.json` (Single Source of Truth)**:
   Register the repository path, git remote URL, default branch (`develop`), repository archetype (`level1-microservice`), `is_core` boolean, and `modes` array (e.g. `["local", "docker", "production"]`).
   - `docker-deployment/modes/local/inventory.json`, `modes/docker/inventory.json`, and `modes/production/inventory.json` are **authoritative symlinks** pointing directly to this file.
   - `docker-deployment`'s orchestrator automatically filters repositories by `mode in r.get("modes", [mode])` and `WORKSPACE_REPOSITORIES`.
   - Run `python3 obsidian-brain/05-Fleet-Operation/00-Repo-Control/build-inventory.py` to auto-discover and preserve overrides.
3. **`docker-deployment/modes/local/config/native.yaml`**:
   Register the service capability block:
   ```yaml
   capabilities:
     my_service:
       ip: ${MS_IP:-127.0.0.1}
       port: "${MS_PORT:-8090}"
   ```
4. **`docker-deployment/docker-compose.yaml`**:
   Register the service container for fleet orchestration and healthchecks.
5. **`watchdog-agent/src/config/heal.go`**:
   Register the relative `standalone.yaml` path in the `targets` slice so the supervisor heals missing symlinks automatically.
6. **`web-interface` & `tele-remote` Dynamic Integration** *(if UI or remote alerts exist)*:
   - Web UI: Service exposes `/static/js/mfe-loader.js` and auto-registers at `http://127.0.0.1:5000/api/v1/register` on boot.
   - Remote C2: Service connects over gRPC on port `1863` to publish telemetry and register Telegram interactive menu trees.

---

## 5. Automated Scaffolding Tooling

Instead of manually assembling folders and boilerplate, agents and engineers **MUST** use the automated scaffolding CLI provided in `08-Base-Scripts`:

```bash
# Scaffold a new Go microservice
python3 08-Base-Scripts/main.py scaffold-microservice --name market-observer --lang go --port 8092 --desc "Real-time ticker stream ingestor"

# Scaffold a new Python microservice (generates controller, models, requirements.txt, VERSION.txt, Makefile)
python3 08-Base-Scripts/main.py scaffold-microservice --name fundamental-analysis --lang python --port 8093 --desc "Financial metrics and SEC filing parser"

# Preview fabrication without writing to disk
python3 08-Base-Scripts/main.py scaffold-microservice --name orderbook-aggregator --lang go --dry-run
```

This automated generator:
1. Fabricates the language directory skeleton (including `src/core/controller.*`, `src/interfaces/`, `src/models/`).
2. Creates all mandatory root files (`VERSION.txt`, `requirements.txt` / `go.mod`, `Makefile`, `Dockerfile`, `docker-compose.yml`, `AGENTS.md`, `AI-Session-State.md`, `README.md`).
3. Sets up standardized dynamic versioning in `Makefile` (`VERSION := $(shell cat VERSION.txt 2>/dev/null || echo "0.0.1")`).
4. Symlinks `standalone.yaml` to `../docker-deployment/modes/local/config/native.yaml`.
5. Creates `quick-overview/` with ignore files.
6. Generates the initial BDD specification note in `02-Business-BDD/02-Behavior-Specs/<name>/FEAT-001-Initialization.md`.
7. Prints the exact copy-paste registration snippets for the 6 Ecosystem Integration Touchpoints.
