"""Functions for creating a cookiecut project to be used in tests."""

import json
import subprocess
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

from tests.consts import PROJECT_DIR


def initialize_git_repo(repo_dir: Path):
    """Run git commands to make a directory into a valid git repository."""
    git_commands = [
        (["git", "init"], "Failed to initialize git repository"),
        (["git", "config", "user.name", "Test User"], "Failed to set git user name"),
        (["git", "config", "user.email", "test@example.com"], "Failed to set git email"),
        (["git", "branch", "-M", "main"], "Failed to create main branch"),
        (["git", "add", "--all"], "Failed to stage files"),
        (["git", "commit", "-m", "feat: initial commit by pytest"], "Failed to commit files"),
    ]

    for cmd, error_msg in git_commands:
        try:
            subprocess.run(cmd, cwd=repo_dir, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"{error_msg}: {e.stderr}") from e


def generate_project(template_values: dict[str, str], test_session_id: str):
    """Generate a boilerplate project that we can use to test the template.

    :param template_values: jinja context used when populating template
    :param test_session_id: potentially randomly generated string used to
        ensure uniqueness of generated file names.
    """
    template_values: dict[str, str] = deepcopy(template_values)
    cookiecutter_config = {"default_context": template_values}
    cookiecutter_config_fpath = PROJECT_DIR / f"tests/cookiecutter-{test_session_id}.json"
    cookiecutter_config_fpath.write_text(json.dumps(cookiecutter_config))

    cmd = [
        "cookiecutter",
        str(PROJECT_DIR),
        "--output-dir",
        str(PROJECT_DIR / "sample"),
        "--no-input",
        "--config-file",
        str(cookiecutter_config_fpath),
        "--verbose",
    ]
    print("COMMAND:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    generated_repo_dir = PROJECT_DIR / "sample" / template_values["repo_name"]
    return generated_repo_dir


def generate_test_project(repo_name: str, package_name: str) -> Path:
    """Generate a test project using standard pattern.

    Args:
        repo_name: Repository name for the project
        package_name: Python package import name

    Returns:
        Path to the generated project directory
    """
    test_session_id = str(uuid4())
    template_values = {"repo_name": repo_name, "package_import_name": package_name}

    project_path = generate_project(template_values, test_session_id)
    initialize_git_repo(project_path)

    # Run initial lint to fix any auto-fixable issues
    subprocess.run(["make", "lint-ci"], cwd=project_path, check=False, timeout=300)

    return project_path


def validate_project_structure(project_path: Path, package_name: str):
    """Validate that generated project has correct structure.

    Args:
        project_path: Path to the generated project
        package_name: Expected package name
    """
    # Verify package structure
    src_package_dir = project_path / "src" / package_name
    assert src_package_dir.exists(), f"Package directory should exist: {src_package_dir}"

    init_file = src_package_dir / "__init__.py"
    assert init_file.exists(), "Package should have __init__.py file"
