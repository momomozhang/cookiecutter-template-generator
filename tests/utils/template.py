"""Template discovery and analysis utilities."""

from pathlib import Path
from typing import List

from tests.consts import PROJECT_DIR


def find_template_files() -> List[Path]:
    """Find all template files containing cookiecutter variables.

    Returns:
        List of Path objects for files containing cookiecutter variables
    """
    template_dir = PROJECT_DIR / "{{cookiecutter.repo_name}}"
    template_files = []

    for file_path in template_dir.rglob("*"):
        if file_path.is_file():
            try:
                content = file_path.read_text(encoding="utf-8")
                if "{{cookiecutter." in content:
                    template_files.append(file_path)
            except (UnicodeDecodeError, PermissionError):
                continue

    return template_files
