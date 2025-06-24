"""Shared cleanup utilities for test projects."""

import shutil
from pathlib import Path

from tests.consts import PROJECT_DIR


def cleanup_generated_project(project_path: Path, test_session_id: str = None):
    """Clean up generated test project and associated files.

    Args:
        project_path: Path to the generated project directory
        test_session_id: Optional test session ID for cleaning up config files
    """
    # Remove project directory
    if project_path.exists():
        shutil.rmtree(project_path)

    # Clean up cookiecutter config file if test_session_id provided
    if test_session_id:
        config_file = PROJECT_DIR / f"tests/cookiecutter-{test_session_id}.json"
        if config_file.exists():
            config_file.unlink()


def cleanup_sample_directory():
    """Clean up the sample/ directory used for test projects."""
    sample_dir = PROJECT_DIR / "sample"
    if sample_dir.exists():
        shutil.rmtree(sample_dir)


def cleanup_cookiecutter_configs():
    """Clean up all cookiecutter config files from tests."""
    for config_file in PROJECT_DIR.glob("tests/cookiecutter-*.json"):
        config_file.unlink()


def extract_test_session_id(project_path: Path) -> str:
    """Extract test session ID from project path for cleanup.

    Args:
        project_path: Path to the generated project

    Returns:
        Test session ID if found in path, None otherwise
    """
    path_parts = project_path.name.split("-")
    # Look for UUID-like patterns in the path
    for part in reversed(path_parts):
        if len(part) >= 8:  # UUID parts are longer
            return part
    return None
