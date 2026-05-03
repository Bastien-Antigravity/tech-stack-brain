# 💻 Developer Wisdom Log

## 🐍 Python Patterns
- Use strict type hinting (`mypy` compliant) as per the ecosystem standard.
- Use `pathlib` for all file operations to ensure cross-OS compatibility (Mac/Linux/Windows).

## 🐹 Go Patterns
- Ensure `CGO_ENABLED=1` for libraries using the Super-Bridge pattern.
- Always handle errors from `Close()` calls in defer blocks.

## 🦀 Rust Patterns
- Use `#[repr(C)]` for all FFI-facing structures.

## ⚠️ Language-Specific Gotchas
- **VBA**: Strings returned from DLLs must be BSTR compatible or carefully managed via `CoTaskMemAlloc`.
