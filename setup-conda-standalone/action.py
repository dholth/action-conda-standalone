#!/usr/bin/env python
"""
Setup a conda environment using conda-standalone.
"""

# See also https://github.com/lestex/action-pygithubactions

import json
import os
import subprocess
import pprint

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


if __name__ == "__main__":
    main()
