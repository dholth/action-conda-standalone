#!/usr/bin/env python
"""
Setup a conda environment using conda-standalone.
"""

# See also https://github.com/lestex/action-pygithubactions

import json
import os
import stat
import subprocess
import platform
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
    # print("Environment is")
    # pprint.pprint(dict(os.environ))

    output_path = Path(os.environ["RUNNER_TEMP"], "conda-standalone", "conda.exe")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Ensure", output_path)

    uname = platform.uname()

    version = "24.9.2"
    system = {"Darwin": "MacOS"}.get(uname.system, uname.system)
    machine = {"AMD64": "x86_64"}.get(uname.machine, uname.machine)
    conda_standalone = f"conda-standalone-{version}-{system}-{machine}.exe"
    conda_standalone_base = "https://github.com/conda/conda-standalone/releases/download"
    conda_standalone_url = f"{conda_standalone_base}/{version}/{conda_standalone}"
    print("Fetch", conda_standalone_url)
    if not output_path.exists():
        subprocess.run(
            f"curl -o {output_path} -L {conda_standalone_url}".split(),
            check=True,
            capture_output=False,
        )

        if system != "Windows": # +x may be permissable on Windows
            os.chmod(output_path, os.stat(output_path).st_mode | stat.S_IEXEC)


if __name__ == "__main__":
    main()
