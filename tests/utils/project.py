import json
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Dict

from tests.consts import PROJECT_DIR


def initialize_git_repo(repo_dir: Path):
    """Initialize a git repository with an initial commit."""
    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    subprocess.run(["git", "branch", "-M", "main"], cwd=repo_dir, check=True)
    subprocess.run(["git", "add", "--all"], cwd=repo_dir, check=True)
    subprocess.run(["git", "commit", "-m", "'initial commit by pytest'"], cwd=repo_dir, check=True)


def generate_project(template_values: Dict[str, str]):
    """Generate a cookiecutter project from template values and return the project path."""
    template_values: Dict[str, str] = deepcopy(template_values)
    cookiecutter_config = {
        "default_context": template_values,
    }
    cookiecutter_config_fpath = PROJECT_DIR / "cookiecutter-test-config.json"
    cookiecutter_config_fpath.write_text(json.dumps(cookiecutter_config))

    subprocess.run(
        [
            "cookiecutter",
            str(PROJECT_DIR),
            "--output-dir",
            str(PROJECT_DIR / "sample"),
            "--no-input",
            "--config-file",
            str(cookiecutter_config_fpath),
            "--verbose",
        ],
        check=True,
    )

    generated_repo_dir = PROJECT_DIR / "sample" / cookiecutter_config["default_context"]["repo_name"]
    return generated_repo_dir
