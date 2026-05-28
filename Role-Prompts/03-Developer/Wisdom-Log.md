---
microservice: core-kms-brain
type: governance
status: active
tags:
- '#service/core-kms-brain'
- '#type/governance'
- '#state/active'
- '#zone/3-fleet'
---
# 💻 Developer Wisdom Log

## 🐍 Python Patterns
- Use strict type hinting (`mypy` compliant) as per the ecosystem standard.
- Use `pathlib` for all file operations to ensure cross-OS compatibility (Mac/Linux/Windows).

## 🐹 Go Patterns
- Ensure `CGO_ENABLED=1` for libraries using the Super-Bridge pattern.
- Always handle errors from `Close()` calls in defer blocks.

## 🦀 Rust Patterns
- Use `#[repr(C)]` for all FFI-facing structures.

## 🌐 Web / UI Patterns
- Delegate CPU-bound operations (e.g. data filtering, parsing, linkifying) to a Web Worker thread to keep the UI fluid.
- Cache DOM element references inside a single `dom` object on initialization.

## ⚠️ Language-Specific Gotchas
- **VBA**: Strings returned from DLLs must be BSTR compatible or carefully managed via `CoTaskMemAlloc`.
- **JavaScript**: Vis.js canvas requires manual resize refitting when parent containers undergo CSS Grid or Flex transitions; query computed style durations to synchronize the engine.
