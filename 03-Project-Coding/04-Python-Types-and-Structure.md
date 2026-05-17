---
title: Python Types and Structure
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#service/ecosystem-wide'
- '#state/active'
- '#type/architecture'
---
# 📐 Python Types and Structure

## Architectural Rule

- **Headers**: Every file must start with a Shebang and UTF-8 declaration:
  ```python
  #!/usr/bin/env python
  # coding:utf-8

  ```
- **Structure**: Use `abc.ABC` for interfaces.
- **Interface Naming**: do not name Python interfaces with `I`-prefix: `Logger`, `DataProcessor`. 
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

## 🎨 Visual Formatting & Documentation

All Python code MUST adhere to the **[[11-Unified-Comment-Standards|Unified Comment Standards]]**. This includes:
- The **Triple-Block Header** (Essential Process, Data Flow, Key Parameters).
- **Horizontal Dividers** for method and section separation.
- **Intent-First Docstrings**.

## ⚡ Asyncio & Concurrency

Python 3.12+ services requiring high-concurrency MUST follow these asyncio patterns:

- **Entry Point**: Use `asyncio.run(main())` for the script's entry point. Never manage loops manually.
- **Structured Concurrency**: Prefer `asyncio.TaskGroup()` for managing multiple concurrent tasks. It ensures that if one task fails, all other tasks in the group are cancelled.
- **Strong Task References**: To prevent background tasks from being garbage collected mid-execution, MUST store a reference to the task (e.g., in a `set` or as a class attribute).
- **Non-Blocking I/O**:
  - **Network**: Use `aiohttp` or `httpx` for HTTP requests.
  - **Subprocess**: Use `asyncio.create_subprocess_exec` instead of `subprocess.run`.
- **Graceful Shutdown**: Use an `asyncio.Event` (e.g., `self._shutdown_event`) to signal termination to background loops.
- **Blocking Bridge**: For legacy synchronous libraries that do not support async, use `asyncio.to_thread()` or `loop.run_in_executor()` to prevent blocking the event loop.

## 🏗 Component Architecture

All ecosystem components follow a strict initialization pattern:

- **Dependency Injection**: Always pass `config` and `logger` objects to constructors.
- **Static Identify**: Every class must have a `Name` static property.
- **Logging Prefix**: Use the `Name` property in all logs:
  ```python
  self.logger.info("{0} : starting process...".format(self.Name))
  ```


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

class DataProcessor(ABC):
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

## 🚀 Async Microservice Pattern

```python
import asyncio
from microservice_toolbox.utils.logger import ensure_safe_logger

async def main():
    config = load_config("standalone")
    logger = ensure_safe_logger(None)
    
    # Mandatory background task tracking (Strong Reference Rule)
    background_tasks = set()
    
    async with asyncio.TaskGroup() as tg:
        # Start core service
        srv = AsyncService(config, logger)
        task = tg.create_task(srv.run())
        
        # Keep reference until done
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

class AsyncService:
    Name = "AsyncService"
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self._stop_event = asyncio.Event()

    async def run(self):
        self.logger.info(f"{self.Name} : Starting async loop")
        while not self._stop_event.is_set():
            await self._do_work()
            await asyncio.sleep(1.0)
            
    async def _do_work(self):
        # Always use non-blocking calls (e.g., aiohttp, create_subprocess_exec)
        pass
```
