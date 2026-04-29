#!/usr/bin/env python
# coding:utf-8
"""
ESSENTIAL PROCESS:
Ecosystem orchestrator that discovers all microservice repositories and triggers their build or test cycles.

DATA FLOW:
1. Scans the root directory for folders containing Go, Rust, or Python markers.
2. For each discovered repository, executes the Build-Wrapper.py script with the requested action.
3. Collects and summarizes results.

KEY PARAMETERS:
- action: build | test
"""

from sys import argv as sysArgv, exit as sysExit, executable as sysExecutable
from subprocess import (
    run as subprocessRun,
    CalledProcessError as subprocessCalledProcessError,
)
from pathlib import Path as pathlibPath
from typing import List

# -----------------------------------------------------------------------------------------------


def get_repos(root_dir: str) -> List[pathlibPath]:
    """Finds all root-level directories that look like they contain microservices."""
    repos = []
    for item in pathlibPath(root_dir).iterdir():
        if item.is_dir() and not item.name.startswith(".") and item.name != "prompt":
            # Just simple check: does it have a language folder or target config?
            if (
                (item / "go.mod").exists()
                or (item / "go").exists()
                or (item / "Cargo.toml").exists()
                or (item / "rust").exists()
                or (item / "requirements.txt").exists()
                or (item / "python").exists()
            ):
                repos.append(item)
    return repos


# -----------------------------------------------------------------------------------------------


def run_all(action: str, root_dir: str) -> None:
    """Orchestrates the build or test action across all discovered repositories."""
    repos = get_repos(root_dir)
    print(f"=== Bastien Orchestrator: Discovered {len(repos)} repositories ===")

    make_script = pathlibPath(__file__).parent / "Build-Wrapper.py"
    if not make_script.exists():
        print("Error: Build-Wrapper.py engine missing from .scripts/")
        sysExit(1)

    failures = []

    for repo in repos:
        print(f"\n--- Processing {repo.name} ---")
        try:
            # We call the Build-Wrapper script to handle the cross-platform stuff
            subprocessRun(
                [sysExecutable, str(make_script), action, str(repo)], check=True
            )
        except subprocessCalledProcessError:
            failures.append(repo.name)

    print("\n=== Orchestration Summary ===")
    if not failures:
        print(f"SUCCESS: All {len(repos)} repositories passed '{action}' phase.")
    else:
        print(
            f"FAILURE: The following repos failed during '{action}': {', '.join(failures)}"
        )
        sysExit(1)


# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sysArgv) < 2:
        print("Usage: python Multi-Repo-Validator.py <build|test>")
        sysExit(1)

    action = sysArgv[1]

    # Run from the root workspace directory
    current_dir = pathlibPath(__file__).resolve().parent.parent
    run_all(action, str(current_dir))
