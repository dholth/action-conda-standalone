#!/usr/bin/env python
"""
Setup a conda environment using conda-standalone.
"""

# See also https://github.com/lestex/action-pygithubactions

import json
import os
import subprocess
import pprint
from pathlib import Path

# pass in env: section; not automatic from github actions
REPOSITORY = os.environ.get("INPUT_REPOSITORY")

# ...

def list_runs(repository):
    runs = subprocess.run(
        [
            "gh",
            "run",
            "-R",
            repository,
            "ls",
            "--json",
            "status,conclusion,databaseId,workflowName,headBranch",
        ],
        check=True,
        capture_output=True,
    )
    return json.loads(runs.stdout)


def main():
    print("Environment is")
    pprint.pprint(os.environ)

    output_path = Path("~", "conda-standalone", "conda.exe").expanduser()
    output_path.mkdir()

    print("Ensure", output_path)

    if not output_path.exists():
        subprocess.run(
            f"curl -o {output_path} -L https://github.com/conda/conda-standalone/releases/download/24.5.0/conda-standalone-24.5.0-Windows-x86_64.exe".split(),
            check=True,
            capture_output=False
        )


if __name__ == "__main__":
    main()
