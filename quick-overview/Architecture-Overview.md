---
microservice: tech-stack-brain
type: architecture
status: active
tags:
- '#zone/3-fleet'
- '#ai/ignore'
- '#service/tech-stack-brain'
- '#type/architecture'
---
# Architecture Overview: Tech Stack Brain

## 🏛️ Role in the Ecosystem
The **Tech Stack Brain** is Tier 2 of the 3-Tier AI-KMS Architecture. While Tier 1 (Strategic Nexus) handles global vision and Tier 3 (Business BDD) handles specific behaviors, Tier 2 defines the **Engineering Standards** and **Shared Infrastructure** for the entire Bastien-Antigravity fleet.

## 📂 Directory Structure

### `02-Project-Architecture/`
Contains the "Laws of the System".
- **Global Rules**: The master prompt for AI architects.
- **Patterns**: Documentation for the Facade and Decoupling patterns.
- **Infrastructure**: In-depth records for the Log Server, Configuration Standards, and Networking Protocols.
- **ADRs**: Architectural Decision Records documenting the "Why" behind core system choices.

### `03-Project-Coding/`
The language-specific "How-To" guide.
- **Idioms**: Specific guides for Go (Primary), Rust (High-Perf), and Python (Analysis).
- **Naming**: Unified naming conventions across all languages.
- **Gotchas**: A critical collection of known pitfalls and FFI safety rules.

### `04-Project-Deployment/`
Infrastructure and Lifecycle standards.
- **Docker**: Registry and containerization standards.
- **CI/CD**: Delegated workflows and image promotion rules.
- **Health**: Monitoring and self-healing protocols.

### `05-Project-Scripts/`
The automation toolbox.
- **Multi-Repo-Validator**: Orchestrates builds and tests across the fleet.
- **Build-Wrapper**: Detects language and triggers appropriate toolchains.

---
*Last Updated: 2026-05-16*
