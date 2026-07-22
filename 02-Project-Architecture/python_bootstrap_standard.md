---
microservice: 08-Base-Scripts
type: note
status: active
tags:
- '#service/08-Base-Scripts'
- '#type/note'
- '#state/active'
- '#zone/3-fleet'
---chroa

---
microservice: obsidian-brain
type: standard
status: active
tags:
- '#service/obsidian-brain'
- '#type/standard'
- '#state/active'
- '#zone/3-fleet'
---
# 🐍 Python Microservice Bootstrapping Standard

This document establishes the ecosystem-wide standard for bootstrapping Python microservices and scripts. It ensures reliable execution, virtualenv isolation, working directory normalization, and prevents CGO double runtime initialization panics on macOS.

---

## 🎯 The Core Objectives

Every Python process or entry point in the Bastien-Antigravity fleet must adhere to the following rules:

1. **Isolated Virtualenv**: Executables must always run inside their own local `.venv` (located at the root directory of the respective repository). If invoked with a different Python interpreter, they must automatically hot-swap and relaunch themselves inside the correct `.venv`.
2. **Normalized Directory**: The current working directory (CWD) of the process must be redirected to the root level of the microservice repository.
3. **FFI Library Path Alignment (macOS Stability)**: To prevent double Go runtime initialization panics on macOS (`cgocallback` PC mismatch), all environment variables referring to `libunilog` (`LIBUNILOG_PATH` and `LIBDISTCONF_PATH`) must be aligned to point to the exact same absolute dynamic library path before any ctypes wrapper imports.
4. **Clean Import Paths**: Standard import paths (like the project root, `src/`, and `microservice-toolbox/python` site-packages) must be inserted at the beginning of `sys.path`.

---

## 🛠️ The Unified Bootstrapper Tool

To prevent code duplication, the `microservice-toolbox` provides a single, hardened function that implements all these steps automatically:

```python
from microservice_toolbox.utils.bootstrap import bootstrap_microservice
```

### Method Signature

```python
def bootstrap_microservice(file_path: str, app_name: str = "app") -> None:
    """
    Consolidates environment setup, directory redirection, macOS path alignment,
    virtualenv checks, and python path injections.
    """
```

---

## 🚀 Usage in Microservices

All Python entry points and bootstrappers (`src/bootstrap/__init__.py`) must be structured as follows:

```python
# coding:utf-8
import sys
from pathlib import Path

# 1. Inject microservice-toolbox path dynamically so we can import the bootstrapper
_workspace_root = Path(__file__).resolve().parent.parent.parent.parent.parent
_toolbox_path = _workspace_root / "microservice-toolbox" / "python"
if _toolbox_path.exists() and str(_toolbox_path) not in sys.path:
    sys.path.insert(0, str(_toolbox_path))

# 2. Invoke the unified bootstrapper
from microservice_toolbox.utils.bootstrap import bootstrap_microservice
bootstrap_microservice(__file__, app_name="RAGEngine")

# 3. Safe to import config loaders, UniLog, and proceed with application logic
from microservice_toolbox.config.loader import load_config
from microservice_toolbox.logger import UniLog
```

### Reference Implementation Examples

- **RAG Engine**: [09-RAG-Engine/src/bootstrap/\_\_init\_\_.py](../../09-RAG-Engine/src/bootstrap/__init__.py)
- **Base Scripts**: [08-Base-Scripts/src/bootstrap/\_\_init\_\_.py](../../08-Base-Scripts/src/bootstrap/__init__.py)
- **Agent Factory**: [10-Agent-Factory/src/utils/logger.py](../../10-Agent-Factory/src/utils/logger.py)
