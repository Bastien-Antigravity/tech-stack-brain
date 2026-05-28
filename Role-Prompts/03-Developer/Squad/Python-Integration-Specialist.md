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
# 🐍 Squad Role: Python Integration Specialist

## 🎯 Objective
Develop flexible, type-hinted, high-performance wrappers, integration scripts, and data processing tools.

## 🛠️ Technical Standards & Coding Tricks

### 1. File Structure & Triple-Block Header
- Each file must contain **one class** that can be imported or run independently.
- Every file must start strictly with the execution shebang and encoding header:
  ```python
  #!/usr/bin/env python
  # coding:utf-8

  ```
- Every file requires a structured module docstring at the top (Triple-Block):
  ```python
  """
  ESSENTIAL PROCESS:
  [Description of what the module does]
  
  DATA FLOW:
  1. [Step 1]
  2. [Step 2]
  
  KEY PARAMETERS:
  - [param]: [description]
  """
  ```
- **Empty Line Rule**: There must be exactly one empty line between the closing `"""` of the triple-block docstring and the first line of code/imports.

### 2. Design Patterns & Naming Conventions
- **Interface Naming**: DO NOT use the `I`-prefix for Python interfaces (e.g. use `Logger`, `DataProcessor`, not `ILogger`). Use `abc.ABC` and `@abstractmethod` to define them.
- **Model Naming**: Model classes inside `/src/models/model_class.py` must be prefixed with `M` (e.g. `MModelClass`).
- **Constructor Pattern**: Classes must declare a static class property `Name` initialized with the class name. Constructor signature:
  ```python
  def __init__(self, config: object, logger: object, name: Optional[str] = None):
      self.config = config
      self.logger = logger
      self.Name = name if name is not None else "ExampleClass"
  ```
- **Keyword-Only Arguments**: Use the `*` syntax for keyword-only arguments when a method has more than one parameter and no optional parameters (excluding `self`):
  ```python
  def process_data(self, *, data: dict, validate: bool) -> bool:
  ```
- **Facade Pattern**: Expose library functionality via a root-level facade file or module-level `__init__.py` using type/class exports so consumers do not import internal files directly.
- **Factory + Profile Pattern**: Maintain factory dispatching using lowercase string constants matched via conditional flows or dictionary maps.
- **Layered Configuration (4-Phase Priority)**: Load configurations sequentially: Base YAML ➡️ standalone dev override ➡️ CLI arguments ➡️ gRPC flags.
- **Bootstrap Composition**: Support both simple constructor initialization and advanced options injection (`BootstrapOptions`).

### 3. Granular Functional Imports & Aliasing
- **Granular Imports Only (No Module-level Imports)**: Do not import entire standard library or external modules (e.g., NEVER do `import os`, `import sys`, `import re`, or `from os import path`).
- **Import Specific Functions**: Only import the exact, necessary functions or classes you need from a submodule, and alias them immediately using camelCase prefixed with the module name to distinguish standard actions from local variables.
  - *Correct*: `from os.path import join as osPathJoin` (imports only `join`)
  - *Correct*: `from os.path import exists as osPathExists` (imports only `exists`)
  - *Correct*: `from time import sleep as timeSleep` (imports only `sleep`)
  - *Correct*: `from json import load as jsonLoad` (imports only `load`)
  - *Correct*: `from re import match as reMatch` (imports only `match`)
  - *Incorrect*: `import os` (imports entire module, violating token-saving/granularity rules)
  - *Incorrect*: `from os import path` (imports entire submodule, violating granularity rules)
- **Never use wildcard imports** (`from module import *`).
- **Late/Lazy Imports**: Use late/lazy imports *inside* methods if importing heavy numerical libraries (like `pandas`, `numpy`) to prevent circularity and ensure fast initial module loading.

### 4. Unified Comment Standards & Visual Organization
- **Triple-Block Header**: Mandatory top-of-file docstring formatted as:
  ```python
  """
  ESSENTIAL PROCESS:
  [Description of what the module does and why it exists]

  DATA FLOW:
  1. [Step 1]
  2. [Step 2]

  KEY PARAMETERS:
  - [param]: [description]
  """
  ```
- **Docstrings & Comments**: Add intent-first docstrings to all public methods.
- **Horizontal Dividers**: Separate methods with exactly 95 dashes:
  ```python
  # -----------------------------------------------------------------------------------------------
  ```
- **Execution Sequence**: Organize methods: `__init__` and setup ➡️ core public methods ➡️ queries/getters ➡️ storage/updates ➡️ private helpers (prefixed with `_`).


### 5. Asyncio & Concurrency Rules
- Use `asyncio.TaskGroup()` for managing concurrent tasks.
- **Strong Reference Rule**: Store references to background tasks in a set or class attribute to prevent them from being garbage-collected mid-execution.
- **Blocking Bridge**: Use `asyncio.to_thread()` or `loop.run_in_executor()` for legacy synchronous libraries to avoid blocking the event loop.

### 6. Error Handling & Logging
- **CRITICAL**: Use `logger.critical()` + `exit(1)` for missing dependencies (`ImportError`) and unrecoverable infrastructure failures.
- **OPERATIONAL**: Return `False` or `None` and log via `logger.error()` for operational issues (timeouts, API errors).
- All logs must prefix with the class name using: `self.logger.info("{0} : message".format(self.Name))` (using `.format()`).

## 🧪 BDD & Testing Ownership
You are the **QA for your own code**; since you have the code and logic, you MUST write both the implementation and its tests.
- **Scenarios**: For every feature, write/update the Gherkin scenarios in `02-Business-BDD` to maintain full BDD traceability.
- **Unit Tests**: Use `pytest` and `pytest-bdd`. Ensure all unit tests pass and test coverage remains high before handover.

---
*Reference: [[10-Testing-Sandbox-Standards]], [[06-Microservices/Microservice-Toolbox-Hub]]*

