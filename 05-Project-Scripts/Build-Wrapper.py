#!/usr/bin/env python
# coding:utf-8
# cli:allow-print
"""
ESSENTIAL PROCESS:
Modular build wrapper that detects the programming language of a repository
and runs the appropriate build, test, or lint command.

DATA FLOW:
1. Detects presence of Cargo.toml (Rust), go.mod (Go), or Python markers.
2. Applies optional standalone Go workspace isolation (GOWORK=off).
3. Executes build, test, or lint action via subprocess and fails fast on error.

KEY PARAMETERS:
- target_action: build | test | lint
- root_dir: Path to the repository root.
- standalone: If True, forces GOWORK=off for standalone Go module verification.
"""

from argparse import ArgumentParser as argparseArgumentParser
from importlib.util import find_spec as importlibUtilFindSpec
from os import environ as osEnviron, execl as osExecl, name as osName
from os.path import abspath as osPathAbspath, dirname as osPathDirname, exists as osPathExists, join as osPathJoin, samefile as osPathSamefile
from pathlib import Path as pathlibPath
from subprocess import run as subprocessRun
from sys import argv as sysArgv, executable as sysExecutable, exit as sysExit
from typing import Dict as typeDict, List as typeList, Optional as typeOptional, Tuple as typeTuple

_venv_dir = osPathDirname(osPathAbspath(__file__))
while _venv_dir and _venv_dir != "/" and not osPathExists(osPathJoin(_venv_dir, ".venv")):
    _parent = osPathDirname(_venv_dir)
    if _parent == _venv_dir:
        break
    _venv_dir = _parent
_venv_python = (
    osPathJoin(_venv_dir, ".venv", "Scripts", "python.exe")
    if osName == "nt"
    else osPathJoin(_venv_dir, ".venv", "bin", "python3")
)
if osPathExists(_venv_python):
    try:
        if not osPathSamefile(sysExecutable, _venv_python):
            osExecl(_venv_python, _venv_python, *sysArgv)
    except OSError as exc:
        print(f"Warning: Unable to verify virtualenv executable ({_venv_python}): {exc}")

# -----------------------------------------------------------------------------------------------

def run_cmd(
    cmd: typeList[str],
    *,
    cwd: str,
    env: typeOptional[typeDict[str, str]] = None,
    allowed_exit_codes: typeTuple[int, ...] = (0,),
) -> None:
    """
    Helper to run a shell command and exit on failure.
    """
    print(f"[{cwd}] Running: {' '.join(cmd)}")
    result = subprocessRun(cmd, cwd=cwd, env=env)
    if result.returncode not in allowed_exit_codes:
        print(f"Error: Command failed with exit code {result.returncode}")
        sysExit(result.returncode)

# -----------------------------------------------------------------------------------------------

def detect_and_run(*, target_action: str, root_dir: str, standalone: bool = False) -> None:
    """
    Detects language and runs the requested action.
    """
    root_path = pathlibPath(root_dir).resolve()
    if not root_path.exists():
        print(f"Error: Directory {root_dir} does not exist.")
        sysExit(1)

    print(f"=== Build-Wrapper: {target_action} on {root_path.name} ===")

    # 1. Rust Detection
    if (root_path / "Cargo.toml").exists() or (root_path / "rust" / "Cargo.toml").exists():
        rust_dir = root_path / "rust" if (root_path / "rust").exists() else root_path
        if target_action == "build":
            run_cmd(["cargo", "build"], cwd=str(rust_dir))
        elif target_action == "test":
            run_cmd(["cargo", "test"], cwd=str(rust_dir))
        elif target_action == "lint":
            run_cmd(["cargo", "clippy", "--", "-D", "warnings"], cwd=str(rust_dir))

    # 2. Go Detection
    if (root_path / "go.mod").exists() or (root_path / "go" / "go.mod").exists():
        go_dir = root_path / "go" if (root_path / "go").exists() else root_path
        go_env = None
        if standalone:
            go_env = osEnviron.copy()
            go_env["GOWORK"] = "off"
        if target_action == "build":
            run_cmd(["go", "build", "./..."], cwd=str(go_dir), env=go_env)
        elif target_action == "test":
            run_cmd(["go", "test", "./..."], cwd=str(go_dir), env=go_env)
        elif target_action == "lint":
            run_cmd(["golangci-lint", "run"], cwd=str(go_dir), env=go_env)

    # 3. Python Detection
    if (root_path / "requirements.txt").exists() or (root_path / "pyproject.toml").exists() or (root_path / "python").exists():
        py_dir = root_path / "python" if (root_path / "python").exists() else root_path
        if target_action == "build":
            run_cmd([sysExecutable, "-m", "compileall", "."], cwd=str(py_dir))
        elif target_action == "test":
            if importlibUtilFindSpec("pytest") is not None:
                run_cmd([sysExecutable, "-m", "pytest"], cwd=str(py_dir), allowed_exit_codes=(0, 5))
            else:
                run_cmd([sysExecutable, "-m", "unittest", "discover"], cwd=str(py_dir))
        elif target_action == "lint":
            if importlibUtilFindSpec("ruff") is not None:
                run_cmd([sysExecutable, "-m", "ruff", "check", "."], cwd=str(py_dir))
            elif importlibUtilFindSpec("flake8") is not None:
                run_cmd([sysExecutable, "-m", "flake8", "."], cwd=str(py_dir))
            else:
                print(f"Error: Neither ruff nor flake8 is installed for linting {py_dir}")
                sysExit(1)

    print(f"=== {target_action} completed ===")

# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparseArgumentParser(description="Modular polyglot build, test, and lint wrapper.")
    parser.add_argument("action", choices=["build", "test", "lint"], help="Action to run.")
    parser.add_argument("repo_dir", help="Path to repository root.")
    parser.add_argument(
        "--standalone",
        action="store_true",
        help="Run Go builds and tests with GOWORK=off.",
    )
    parsed_args = parser.parse_args()
    detect_and_run(
        target_action=parsed_args.action,
        root_dir=parsed_args.repo_dir,
        standalone=parsed_args.standalone,
    )
