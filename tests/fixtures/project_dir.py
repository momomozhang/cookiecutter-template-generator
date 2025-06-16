import shutil
from pathlib import Path

import pytest

from tests.utils.project import generate_project


@pytest.fixture(scope="session")
def project_dir():
    template_values = {
        "repo_name": "test-repo",
    }
    generated_repo_dir: Path = generate_project(template_values=template_values)
    yield generated_repo_dir
    shutil.rmtree(path=generated_repo_dir)

    config_file = generated_repo_dir.parent.parent / "cookiecutter-test-config.json"
    if config_file.exists():
        config_file.unlink()
