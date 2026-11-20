#!/usr/bin/env python
# coding:utf-8
# cli:allow-print
"""
ESSENTIAL PROCESS:
Ecosystem orchestrator that discovers all microservice repositories (including
selected obsidian-brain services) and triggers their build, test, or lint cycles.

DATA FLOW:
1. Scans the root directory and designated obsidian-brain sub-repositories for
   Go, Rust, or Python markers.
2. Executes Build-Wrapper.py for each discovered repository with optional
   --standalone Go workspace isolation.
3. Collects failures and reports a fail-fast orchestration summary.

KEY PARAMETERS:
- action: build | test | lint
- standalone: If True, forwards --standalone (GOWORK=off) to Build-Wrapper.py.
"""

from argparse import ArgumentParser as argparseArgumentParser
from os import execl as osExecl, name as osName
from os.path import abspath as osPathAbspath, dirname as osPathDirname, exists as osPathExists, join as osPathJoin, samefile as osPathSamefile
from pathlib import Path as pathlibPath
from subprocess import CalledProcessError as subprocessCalledProcessError, run as subprocessRun
from sys import argv as sysArgv, executable as sysExecutable, exit as sysExit
from typing import List as typeList

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

OBSIDIAN_SERVICE_REPOS = (
    "01-Strategic-Nexus",
    "08-Squad-Agent",
    "09-RAG-Engine",
)

# -----------------------------------------------------------------------------------------------

def _has_language_marker(repo_path: pathlibPath) -> bool:
    """Returns True if the directory contains a supported Go, Rust, or Python marker."""
    return (
        (repo_path / "go.mod").exists()
        or (repo_path / "go").exists()
        or (repo_path / "Cargo.toml").exists()
        or (repo_path / "rust").exists()
        or (repo_path / "requirements.txt").exists()
        or (repo_path / "pyproject.toml").exists()
        or (repo_path / "python").exists()
    )

# -----------------------------------------------------------------------------------------------

def get_repos(root_dir: str) -> typeList[pathlibPath]:
    """
    Finds all root-level and designated obsidian-brain directories containing microservices.
    """
    root_path = pathlibPath(root_dir)
    repos: typeList[pathlibPath] = []
    for item in root_path.iterdir():
        if item.is_dir() and not item.name.startswith(".") and item.name not in ("prompt", "obsidian-brain"):
            if _has_language_marker(item):
                repos.append(item)

    obsidian_root = root_path / "obsidian-brain"
    for sub_name in OBSIDIAN_SERVICE_REPOS:
        candidate = obsidian_root / sub_name
        if candidate.is_dir() and _has_language_marker(candidate):
            repos.append(candidate)

    return sorted(repos, key=lambda p: p.as_posix())

# -----------------------------------------------------------------------------------------------

def run_all(*, action: str, root_dir: str, standalone: bool = False) -> None:
    """
    Orchestrates the build, test, or lint action across all discovered repositories.
    """
    repos = get_repos(root_dir)
    print(f"=== Bastien Orchestrator: Discovered {len(repos)} repositories ===")

    make_script = pathlibPath(__file__).parent / "Build-Wrapper.py"
    if not make_script.exists():
        print(f"Error: Build-Wrapper.py engine missing from {make_script.parent}")
        sysExit(1)

    failures: typeList[str] = []

    for repo in repos:
        print(f"\n--- Processing {repo.name} ---")
        cmd = [sysExecutable, str(make_script), action, str(repo)]
        if standalone:
            cmd.append("--standalone")
        try:
            subprocessRun(cmd, check=True)
        except subprocessCalledProcessError:
            failures.append(repo.name)

    print("\n=== Orchestration Summary ===")
    if not failures:
        print(f"SUCCESS: All {len(repos)} repositories passed '{action}' phase.")
    else:
        print(f"FAILURE: The following repos failed during '{action}': {', '.join(failures)}")
        sysExit(1)

# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparseArgumentParser(description="Orchestrate polyglot build, test, or lint across repositories.")
    parser.add_argument("action", choices=["build", "test", "lint"], help="Action to run across repositories.")
    parser.add_argument(
        "--standalone",
        action="store_true",
        help="Forward --standalone (GOWORK=off) to Build-Wrapper.py.",
    )
    parsed_args = parser.parse_args()

    script_dir = pathlibPath(__file__).resolve().parent
    workspace_root = script_dir.parents[2]

    run_all(action=parsed_args.action, root_dir=str(workspace_root), standalone=parsed_args.standalone)
