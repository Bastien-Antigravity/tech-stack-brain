---
title: "Python Types and Structure"
type: architecture
status: active
microservice: ecosystem-wide
---

# 📐 Python Types and Structure

## Architectural Rule
- **Headers**: Every file must start with a Shebang and UTF-8 declaration:
  ```python
  #!/usr/bin/env python
  # coding:utf-8
  
  ```
- **Structure**: Use `abc.ABC` for interfaces.
- **Interface Naming**: Python interfaces use `I`-prefix: `ILogger`, `IDataProcessor`.
- **Type Hints**: Always use type hints for all function signatures. Use `Optional[Type]` from `typing`.
- **Private Methods**: Prefix with `_underscore`: `_load_from_file()`, `_apply_cli_overrides()`.
- **Static Methods**: Use `@staticmethod` for utility functions like `deep_merge()`.
- **Late Imports (Modular DI)**: Prefer importing specialized or heavy libraries *inside* methods (e.g., in `__init__` or setup calls) to prevent circularity and ensure fast module loading.
- **Dependency Management**: Pinned `requirements.txt`.
- **Imports**: Use relative imports within the package hierarchy.

## 📥 Import Aliasing & Visibility
To distinguish standard actions from local variables, use descriptive aliasing for common functional imports:
- **Standard Library**: Prefer aliased functional imports over module imports to distinguish standard actions from local variables.
  - Example: `from math import pow as mathPow`, `from time import sleep as timeSleep`, `from os.path import join as osPathJoin`.
- **Internal Helpers**: `from src.helpers.proxy import getHttpProxy`.

## 🎨 Visual Formatting
- **Method Separation**: Use a standard horizontal divider between all class methods:
  ```python
  # -----------------------------------------------------------------------------------------------
  ```
- **Section Dividers**: Use `# ### SECTION NAME ###` or `##### ... #####` for major logical blocks within a module.

## 🏗 Component Architecture
All ecosystem components follow a strict initialization pattern:
- **Dependency Injection**: Always pass `config` and `logger` objects to constructors.
- **Static Identify**: Every class must have a `Name` static property.
- **Logging Prefix**: Use the `Name` property in all logs:
  ```python
  self.logger.info("{0} : starting process...".format(self.Name))
  ```

## 📝 Documentation Requirements
Module docstrings must clearly outline:
1. **ESSENTIAL PROCESS**: The high-level objective.
2. **DATA FLOW**: How data enters, moves through, and leaves the component.
3. **KEY PARAMETERS**: Essential configuration fields.

## Error Handling
```python
# Descriptive exception messages with component prefix
raise FileNotFoundError(f"Toolbox (Python): Config file '{filename}' not found for profile '{profile}'")
raise ValueError(f"capability {capability} not found")
```
> ⚠️ **Note**: Python raises hard exceptions for missing config files, while Go/Rust silently skip them.

## Naming Conventions (Python-specific)
- **Functions**: `snake_case` — `load_config()`, `parse_cli_args()`, `deep_merge()`
- **Classes**: `PascalCase` — `AppConfig`
- **Private**: `_underscore_prefix` — `_load_from_file()`, `_apply_cli_overrides()`

## Motivation (Why?)
- Maintainability: Makes Python services easier to audit and refactor in a polyglot environment.
- Alignment: Matches the structural rigor of Go and Rust.

## Examples
```python
from abc import ABC, abstractmethod
from typing import Optional

class IDataProcessor(ABC):
    @abstractmethod
    def process_data(self, payload: dict) -> bool:
        pass

# Semantic helper to match Go LoadConfig()
def load_config(profile, specific_flags=None):
    return AppConfig(profile, specific_flags)

# Private method convention
class AppConfig:
    def _load_from_file(self, filename):
        ...
    def _apply_cli_overrides(self):
        ...
    @staticmethod
    def deep_merge(dst, src):
        ...
```
