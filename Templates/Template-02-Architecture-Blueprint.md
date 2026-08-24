---
microservice: 08-Base-Scripts
type: note
status: active
tags:
- '#service/08-Base-Scripts'
- '#type/note'
- '#state/active'
- '#zone/3-fleet'
---
# Architecture Blueprint: [Feature/Bug Name]

## 1. Context Injection
> **Mandatory Check**: I have verified this design against `03-Tech-Stack/02-Project-Architecture/Global-Architecture-Rules.md`.

## 2. Research Findings
*Summary of how the current codebase handles this area (e.g., "Currently, config-server uses a hardcoded map for X").*

## 3. Proposed Interfaces & Models (The Facade Law)
*Define the Go interfaces, Rust traits, or Python protocols here. Do NOT write business logic. If this is a cross-repo boundary, it MUST be registered.*
```go
// Example
type IFeature interface {
    DoThing() error
}
```

## 4. Ecosystem Impact
*Does this change require NATS event changes? Safe-socket protocol changes? If yes, list them here and remind the Fleet Architect to update `00-Interface-Registry.md`.*

## 5. Next Step
Pass this document to the **Developer**.
