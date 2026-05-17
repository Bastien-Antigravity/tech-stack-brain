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
# General & Misc

Philosophy and general guidelines for the Bastien-Antigravity Tech Stack.

## 🌟 Philosophy
- **Go is the Source of Truth**: When in doubt about a pattern or API, refer to the Go implementation in the `microservice-toolbox`.
- **Polyglot Parity**: We treat Rust and Python as first-class citizens. They must have matching semantics for configuration, logging, and networking.
- **Documentation First**: An undocumented feature is a broken feature. All major decisions must be captured in ADRs or the `02-Project-Architecture` series.

## ⚙️ Optimization Tips
- **Socket Health**: Always follow the **2.5x Rule** for heartbeats. If your timeout is 5s, your heartbeat must be 2s or faster.
- **FFI Stability**: Never unload a Go shared library. Let it live for the life of the process.

## 🛠 Terminal Standards
- **Standard Program Name**: Always use `GetServiceName()` from the toolbox.
- **Logging Path**: Trim source paths to `filepath.Base()` in logs to maximize horizontal terminal space.
- **ASCII Art**: Maintain ASCII topological diagrams in `/doc` for quick visual mental mapping.

---
*Status: Production Standard v1.1*
