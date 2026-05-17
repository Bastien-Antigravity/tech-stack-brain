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
# Testing Playbook

Quality Assurance in the Tech Stack Brain focuses on ensuring our **standards** remain valid and our **automation** remains functional.

## 1. Fleet-Wide Validation
To verify the integrity of the entire ecosystem after an architectural change:
```bash
python 05-Project-Scripts/Multi-Repo-Validator.py test
```
This script will discover all repositories and run their respective language-specific test suites.

## 2. Unit Testing Standards
- **Go**: Use `go test ./...`. Enforce 80%+ coverage on core logic.
- **Rust**: Use `cargo test`. Ensure all `Result` types are handled.
- **Python**: Use `pytest`. Type hints must be validated via `mypy`.

## 3. The Testing Sandbox (BDD)
For integration testing, refer to `02-Project-Architecture/10-Testing-Sandbox-Standards.md`.
- **01-Specifications**: Behavioral scenarios (YAML).
- **02-Scenarios**: Technical validation (Go/Rust/Python).
- **03-Orchestration**: `scenario_orchestrator.py`.

## 4. Sentinel Audit Rules
- **Quick-Overview Check**: Every repo MUST have a populated `quick-overview/` folder with standard markdown files.
- **AI-Ignore Verification**: Ensure `.aiignore`, `.mcpignore`, and `.geminiignore` exist in `quick-overview/`.
- **Metadata Audit**: Run `Brain-Health-Audit.py` to ensure YAML frontmatter remains compliant with the `tech-stack-brain` standards.
