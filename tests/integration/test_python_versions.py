"""Test template generation across Python version matrix."""

import re

import pytest

from tests.utils.cleanup import cleanup_generated_project, extract_test_session_id
from tests.utils.project import generate_test_project, validate_project_structure


class TestPythonVersionMatrix:
    """Test generated projects work across Python versions."""

    SUPPORTED_PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]
    EXPERIMENTAL_VERSIONS = ["3.13"]

    @pytest.mark.parametrize("python_version", SUPPORTED_PYTHON_VERSIONS)
    def test_project_supports_python_version(self, python_version):
        """Test that generated project declares support for Python version."""
        repo_name = f"test-python-{python_version.replace('.', '-')}"
        package_name = f"test_python_{python_version.replace('.', '_')}"

        project_path = generate_test_project(repo_name, package_name)

        try:
            # Check pyproject.toml declares Python version support
            pyproject_path = project_path / "pyproject.toml"
            assert pyproject_path.exists(), "Generated project must have pyproject.toml"

            with open(pyproject_path, encoding="utf-8") as f:
                content = f.read()

            # Template currently uses >=3.7, which supports all our test versions
            # This validates that the minimum required version allows our test versions
            if "requires-python" in content:
                # Extract the minimum version from requires-python line
                match = re.search(r'requires-python\s*=\s*">=(\d+\.\d+)"', content)
                if match:
                    min_version = match.group(1)
                    # Validate that our test version meets the minimum requirement
                    test_version_tuple = tuple(map(int, python_version.split(".")))
                    min_version_tuple = tuple(map(int, min_version.split(".")))
                    assert test_version_tuple >= min_version_tuple, (
                        f"Python {python_version} should meet minimum requirement {min_version}"
                    )
        finally:
            test_session_id = extract_test_session_id(project_path)
            cleanup_generated_project(project_path, test_session_id)

    def test_experimental_python_version_handling(self):
        """Test handling of experimental Python versions."""
        repo_name = "test-experimental-python"
        package_name = "test_experimental_python"

        project_path = generate_test_project(repo_name, package_name)

        try:
            # Generated project should have flexibility for experimental versions
            pyproject_path = project_path / "pyproject.toml"
            with open(pyproject_path, encoding="utf-8") as f:
                content = f.read()

            # Should not hard-code maximum Python version that would exclude 3.13
            assert "<3.13" not in content, "Should not exclude experimental Python versions"
        finally:
            test_session_id = extract_test_session_id(project_path)
            cleanup_generated_project(project_path, test_session_id)


class TestEndToEndValidation:
    """Test complete end-to-end functionality."""

    def test_complete_workflow_simulation(self):
        """Simulate complete user workflow from generation to usage."""
        repo_name = "end-to-end-test-project"
        package_name = "end_to_end_test_project"

        # Step 1: Generate project (user runs cookiecutter)
        project_path = generate_test_project(repo_name, package_name)

        try:
            # Step 2: Verify project structure (user checks generated files)
            essential_files = ["pyproject.toml", "Makefile", "README.md", "src", "tests"]

            for file_name in essential_files:
                file_path = project_path / file_name
                assert file_path.exists(), f"Essential file/directory missing: {file_name}"

            # Step 3: Verify package is importable (user tests basic functionality)
            validate_project_structure(project_path, package_name)
        finally:
            test_session_id = extract_test_session_id(project_path)
            cleanup_generated_project(project_path, test_session_id)
