import subprocess
from pathlib import Path


def test_linting_passes(project_dir: Path):
    """Validate that the templatized project has no auto-fixable linting issues."""
    subprocess.run(["make", "lint-ci"], cwd=project_dir, check=True)


def test_tests_pass(project_dir: Path):
    subprocess.run(["make", "install"], cwd=project_dir, check=True)
    subprocess.run(["make", "test-wheel-locally"], cwd=project_dir, check=True)


def test_install_succeeds():
    pass
