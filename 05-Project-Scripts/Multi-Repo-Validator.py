#!/usr/bin/env python
# coding:utf-8
"""
ESSENTIAL PROCESS:
Ecosystem orchestrator that discovers all microservice repositories and 
triggers their build or test cycles.

DATA FLOW:
1. Scans the root directory for folders containing Go, Rust, or Python markers.
2. For each discovered repository, executes the Build-Wrapper.py script 
   with the requested action.
3. Collects and summarizes results.

KEY PARAMETERS:
- action: build | test
"""

from sys import argv as sysArgv, exit as sysExit, executable as sysExecutable
from subprocess import run as subprocessRun, CalledProcessError as subprocessCalledProcessError
from pathlib import Path
from typing import List

# -----------------------------------------------------------------------------------------------

def get_repos(root_dir: str) -> List[Path]:
    """
    Finds all root-level directories that look like they contain microservices.
    """
    repos = []
    for item in Path(root_dir).iterdir():
        if item.is_dir() and not item.name.startswith(".") and item.name != "prompt":
            # Check for language markers
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
    """
    Orchestrates the build or test action across all discovered repositories.
    """
    repos = get_repos(root_dir)
    print("=== Bastien Orchestrator: Discovered {0} repositories ===".format(len(repos)))

    make_script = Path(__file__).parent / "Build-Wrapper.py"
    if not make_script.exists():
        print("Error: Build-Wrapper.py engine missing from scripts/")
        sysExit(1)

    failures = []

    for repo in repos:
        print("\n--- Processing {0} ---".format(repo.name))
        try:
            # We call the Build-Wrapper script to handle the cross-platform stuff
            subprocessRun(
                [sysExecutable, str(make_script), action, str(repo)], check=True
            )
        except subprocessCalledProcessError:
            failures.append(repo.name)

    print("\n=== Orchestration Summary ===")
    if not failures:
        print("SUCCESS: All {0} repositories passed '{1}' phase.".format(len(repos), action))
    else:
        print(
            "FAILURE: The following repos failed during '{0}': {1}".format(action, ', '.join(failures))
        )
        sysExit(1)

# -----------------------------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sysArgv) < 2:
        print("Usage: python Multi-Repo-Validator.py <build|test>")
        sysExit(1)

    action_param = sysArgv[1]

    # Run from the root workspace directory (parent of tech-stack-brain)
    script_dir = Path(__file__).resolve().parent
    workspace_root = script_dir.parents[1]
    
    run_all(action_param, str(workspace_root))
