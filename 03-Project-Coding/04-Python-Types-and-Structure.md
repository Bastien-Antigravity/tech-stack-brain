---
title: Python Types and Structure
type: architecture
status: active
microservice: ecosystem-wide
tags:
- '#zone/3-fleet'
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

## 📦 Dynamic Versioning (`VERSION.txt` ONLY via `AppConfig`) & Standard Toolbox Modules
- **Dedicated `AppConfig` Accessor**: Python services MUST resolve their version via `app_config.get_version()` (or `app_config.version`). Hardcoding static version strings (`"0.0.1"`, `"1.0.0"`), checking runtime `APP_VERSION` / `SERVICE_VERSION` env overrides, or writing bespoke `VERSION.txt` scanning loops is strictly prohibited (`HARDCODED_VERSION_VIOLATION`).
- **Standard Tools First**: Use `init_microservice`, `microservice_toolbox.spec` (`publish_with_lifecycle`, `build_spec_from_config`), `microservice_toolbox.contracts` (`ExchangeContract`, `ContractsEnvelope`, `extract_fastapi_operations`, `extract_proto_operations`, `extract_capnp_operations`, `build_contracts_envelope`), `microservice_toolbox.wiretap`, `microservice_toolbox.notification`, `microservice_toolbox.lifecycle`, and `microservice_toolbox.connectivity` rather than hand-rolling boilerplate.
- **Fail-Fast Cold-Path Validation**: Raise an immediate error (`RuntimeError`) if `VERSION.txt` or a required `AppConfig` capability is missing — **never** substitute silent `"0.0.1"` / `"127.0.0.1"` / `"0.0.0.0"` fallbacks. Trust pre-validated `AppConfig` strings directly on hot paths without redundant `hasattr` / `isinstance` / `try/except: pass` clutter (check optionality only on genuinely optional parameters).
- **Packaging**: `setup.py` / `pyproject.toml` builders must parse `VERSION.txt` dynamically at packaging time.

## 📥 Granular Functional Imports & camelCase Aliasing (The "Bastien" Pattern)

- **Prohibit Whole-Module Imports**: NEVER write `import os`, `import sys`, `import re`, `import json`, `import time`, `import subprocess`, or `import asyncio` outside the entrypoint `bootstrap_microservice` block.
- **Granular & camelCase Aliased (`[module][SymbolName]`)**: Import **only** the required functions, classes, or types from standard library and external packages, and alias every symbol using `[module][SymbolName]` camelCase:
  - `from math import pow as mathPow`
  - `from time import sleep as timeSleep, time as timeTime`
  - `from os.path import join as osPathJoin, exists as osPathExists`
  - `from json import dumps as jsonDumps, loads as jsonLoads`
  - `from datetime import datetime as dtDateTime, timezone as dtTimezone`
  - `from typing import Any as typeAny, Dict as typeDict, List as typeList, Optional as typeOptional`
- **Combined Single-Line Imports per Module**: When importing multiple symbols from the same module, combine them onto a **single line** (never split `from typing import ...` across multiple lines).
- **Do NOT Alias Local/Internal Libraries**: The camelCase aliasing rule applies **strictly** to external dependencies and standard libraries. Never alias internal project imports:
  - *Correct*: `from src.helpers.proxy import getHttpProxy` or `from .storage import Storage`
  - *Incorrect*: `from .storage import Storage as intStorage`
- **Never use wildcard imports** (`from module import *`).

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
  self.logger.info(f"{self.Name} : starting process...")
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
#!/usr/bin/env python
# coding:utf-8

"""
ESSENTIAL PROCESS:
Defines abstract data processor contract and configuration loader wrapper.

DATA FLOW:
1. Validates input payload dictionary via abstract contract.
2. Instantiates AppConfig from profile and optional CLI flags.

KEY PARAMETERS:
- profile: Configuration profile identifier.
"""

from abc import ABC as abcABC, abstractmethod as abcAbstractMethod
from typing import Any as typeAny, Dict as typeDict, Optional as typeOptional

# -----------------------------------------------------------------------------------------------

class DataProcessor(abcABC):
    @abcAbstractMethod
    def process_data(self, *, payload: typeDict[str, typeAny]) -> bool:
        pass

# -----------------------------------------------------------------------------------------------

def load_config(profile: str, *, specific_flags: typeOptional[typeDict[str, typeAny]] = None) -> "AppConfig":
    return AppConfig(profile=profile, specific_flags=specific_flags)

# -----------------------------------------------------------------------------------------------

class AppConfig:
    Name = "AppConfig"

    def _load_from_file(self, filename: str) -> None:
        ...

    # -----------------------------------------------------------------------------------------------
    def _apply_cli_overrides(self) -> None:
        ...

    # -----------------------------------------------------------------------------------------------
    @staticmethod
    def deep_merge(dst: typeDict[str, typeAny], src: typeDict[str, typeAny]) -> typeDict[str, typeAny]:
        ...
```

## 🚀 Async Microservice Pattern

```python
#!/usr/bin/env python
# coding:utf-8

"""
ESSENTIAL PROCESS:
Asynchronous microservice worker loop using structured TaskGroup concurrency.

DATA FLOW:
1. Bootstraps microservice configuration and UniLog logger.
2. Spawns AsyncService inside asyncio TaskGroup with strong task references.

KEY PARAMETERS:
- config: Validated AppConfig instance.
- logger: UniLog instance.
"""

from asyncio import Event as asyncioEvent, TaskGroup as asyncioTaskGroup, run as asyncioRun, sleep as asyncioSleep
from typing import Any as typeAny

from microservice_toolbox.utils.bootstrap import init_microservice

# -----------------------------------------------------------------------------------------------

async def main() -> None:
    ctx = init_microservice("async_service")
    config = ctx.config
    logger = ctx.logger

    # Mandatory background task tracking (Strong Reference Rule)
    background_tasks = set()

    async with asyncioTaskGroup() as tg:
        srv = AsyncService(config=config, logger=logger)
        task = tg.create_task(srv.run())

        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)

# -----------------------------------------------------------------------------------------------

class AsyncService:
    Name = "AsyncService"

    def __init__(self, *, config: typeAny, logger: typeAny) -> None:
        self.config = config
        self.logger = logger
        self._stop_event = asyncioEvent()

    # -----------------------------------------------------------------------------------------------
    async def run(self) -> None:
        self.logger.info(f"{self.Name} : Starting async loop")
        while not self._stop_event.is_set():
            await self._do_work()
            await asyncioSleep(1.0)

    # -----------------------------------------------------------------------------------------------
    async def _do_work(self) -> None:
        # Always use non-blocking calls (e.g., aiohttp, create_subprocess_exec)
        pass
```
