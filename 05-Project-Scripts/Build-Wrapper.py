#!/usr/bin/env python
# coding:utf-8
"""
ESSENTIAL PROCESS:
Modular build wrapper that detects the programming language of a repository and runs the appropriate build or test command.

DATA FLOW:
1. Detects Presence of Cargo.toml (Rust), go.mod (Go), or requirements.txt/python folder (Python).
2. Executes build or test action via subprocess.

KEY PARAMETERS:
- target_action: build | test
- root_dir: Path to the repository root.
"""

from sys import exit as sysExit, executable as sysExecutable, argv as sysArgv
from subprocess import run as subprocessRun
from pathlib import Path as pathlibPath
from typing import List

# -----------------------------------------------------------------------------------------------


def run_cmd(cmd: List[str], cwd: str) -> None:
    """Helper to run a shell command and exit on failure."""
    print(f"[{cwd}] Running: {' '.join(cmd)}")
    result = subprocessRun(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"Error: Command failed with exit code {result.returncode}")
        sysExit(result.returncode)


# -----------------------------------------------------------------------------------------------


def detect_and_run(target_action: str, root_dir: str) -> None:
    """Detects language and runs the requested action."""
    root_path = pathlibPath(root_dir).resolve()
    if not root_path.exists():
        print(f"Error: Directory {root_dir} does not exist.")
        sysExit(1)

    print(f"=== Build-Wrapper: {target_action} on {root_path.name} ===")

    # 1. Rust Detection
    if (root_path / "Cargo.toml").exists() or (
        root_path / "rust" / "Cargo.toml"
    ).exists():
        rust_dir = root_path / "rust" if (root_path / "rust").exists() else root_path
        if target_action == "build":
            run_cmd(["cargo", "build"], str(rust_dir))
        elif target_action == "test":
            run_cmd(["cargo", "test"], str(rust_dir))

    # 2. Go Detection
    if (root_path / "go.mod").exists() or (root_path / "go" / "go.mod").exists():
        go_dir = root_path / "go" if (root_path / "go").exists() else root_path
        if target_action == "build":
            run_cmd(["go", "build", "./..."], str(go_dir))
        elif target_action == "test":
            run_cmd(["go", "test", "./..."], str(go_dir))

    # 3. Python Detection
    if (root_path / "requirements.txt").exists() or (root_path / "python").exists():
        py_dir = root_path / "python" if (root_path / "python").exists() else root_path
        if target_action == "build":
            # Just do a compile syntax check for Python "builds"
            run_cmd([sysExecutable, "-m", "compileall", "."], str(py_dir))
        elif target_action == "test":
            # Default to pytest if it exists, else just unittest
            try:
                run_cmd([sysExecutable, "-m", "pytest"], str(py_dir))
            except Exception:
                run_cmd([sysExecutable, "-m", "unittest", "discover"], str(py_dir))

    print(f"=== {target_action} completed ===")


# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sysArgv) < 3:
        print("Usage: python Build-Wrapper.py <build|test> <repo_dir>")
        sysExit(1)

    action = sysArgv[1]
    target = sysArgv[2]

    if action not in ["build", "test"]:
        print("Unsupported action. Use build or test.")
        sysExit(1)

    detect_and_run(action, target)
