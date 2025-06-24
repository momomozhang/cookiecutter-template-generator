import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pytest

from tests.utils.project import generate_project
from tests.utils.cleanup import cleanup_sample_directory, cleanup_cookiecutter_configs


@dataclass
class RepoNameTestCase:
    """Test case for repository name validation."""

    repo_name: str
    expected_package_name: str
    should_generate: bool
    should_import: bool
    description: str


class TestRepositoryNameRobustValidation:
    """Comprehensive test-first development for repository name edge cases."""

    @pytest.fixture(autouse=True)
    def cleanup_generated_projects(self):
        """Clean up generated projects after each test."""
        yield
        cleanup_sample_directory()
        cleanup_cookiecutter_configs()

    @pytest.fixture
    def repo_name_test_cases(self) -> List[RepoNameTestCase]:
        """Define comprehensive test cases for repository names."""
        return [
            # Hyphenated names - common GitHub pattern
            RepoNameTestCase(
                repo_name="my-awesome-project",
                expected_package_name="my_awesome_project",
                should_generate=True,
                should_import=True,
                description="Standard hyphenated project name",
            ),
            RepoNameTestCase(
                repo_name="data-analysis-tool",
                expected_package_name="data_analysis_tool",
                should_generate=True,
                should_import=True,
                description="Multi-hyphenated project name",
            ),
            # Underscore names - Python convention
            RepoNameTestCase(
                repo_name="my_awesome_project",
                expected_package_name="my_awesome_project",
                should_generate=True,
                should_import=True,
                description="Underscore project name",
            ),
            # Numbers - valid cases
            RepoNameTestCase(
                repo_name="project123",
                expected_package_name="project123",
                should_generate=True,
                should_import=True,
                description="Project name ending with numbers",
            ),
            RepoNameTestCase(
                repo_name="data2024analysis",
                expected_package_name="data2024analysis",
                should_generate=True,
                should_import=True,
                description="Numbers in middle of name",
            ),
            # Numbers - invalid cases
            RepoNameTestCase(
                repo_name="123project",
                expected_package_name="project_123project",  # Prefix to make valid
                should_generate=True,
                should_import=True,  # Actually valid after prefixing
                description="Project name starting with numbers",
            ),
            # Mixed patterns
            RepoNameTestCase(
                repo_name="my-project_2024",
                expected_package_name="my_project_2024",
                should_generate=True,
                should_import=True,
                description="Mixed hyphens and underscores with numbers",
            ),
            RepoNameTestCase(
                repo_name="web_scraper-v2",
                expected_package_name="web_scraper_v2",
                should_generate=True,
                should_import=True,
                description="Underscore and hyphen with version suffix",
            ),
            # Edge cases that should fail
            RepoNameTestCase(
                repo_name="",
                expected_package_name="",
                should_generate=False,
                should_import=False,
                description="Empty repository name",
            ),
            RepoNameTestCase(
                repo_name="-invalid-start",
                expected_package_name="invalid_start",
                should_generate=True,  # Cookiecutter allows this, creates directory
                should_import=True,  # Package name is valid after conversion
                description="Repository name starting with hyphen",
            ),
        ]

    def test_repo_name_conversion_logic(self, repo_name_test_cases):
        """Test repository name to package name conversion - WILL FAIL FIRST."""
        conversion_failures = []

        for test_case in repo_name_test_cases:
            if not test_case.should_generate:
                continue  # Skip invalid cases for conversion testing

            try:
                actual_package_name = convert_repo_name_to_package_name(test_case.repo_name)

                if actual_package_name != test_case.expected_package_name:
                    conversion_failures.append(
                        f"{test_case.description}: "
                        f"'{test_case.repo_name}' -> got '{actual_package_name}', "
                        f"expected '{test_case.expected_package_name}'"
                    )

            except (ValueError, TypeError, AttributeError) as e:
                conversion_failures.append(
                    f"{test_case.description}: '{test_case.repo_name}' -> "
                    f"conversion failed with {type(e).__name__}: {e}"
                )

        assert not conversion_failures, "Repository name conversion failures:\n" + "\n".join(
            f"  - {failure}" for failure in conversion_failures
        )

    def test_repo_name_project_generation(self, repo_name_test_cases):
        """Test that repository names generate valid project structures."""
        generation_failures = []

        for test_case in repo_name_test_cases:
            template_values = {
                "repo_name": test_case.repo_name,
                "package_import_name": test_case.expected_package_name,
            }

            test_id = f"gen-test-{hash(test_case.repo_name) % 10000}-{int(time.time() * 1000) % 10000}"

            if test_case.should_generate:
                try:
                    generated_dir = generate_project(template_values, test_id)

                    # Validate basic structure
                    validation_errors = self._validate_project_structure(
                        generated_dir, test_case.expected_package_name
                    )

                    if validation_errors:
                        generation_failures.append(f"{test_case.description}: {', '.join(validation_errors)}")

                except (subprocess.CalledProcessError, FileNotFoundError, PermissionError) as e:
                    generation_failures.append(
                        f"{test_case.description}: generation failed with {type(e).__name__}: {e}"
                    )
            else:
                # Should fail generation
                try:
                    generate_project(template_values, test_id)
                    generation_failures.append(
                        f"{test_case.description}: expected generation to fail but it succeeded"
                    )
                except (subprocess.CalledProcessError, FileNotFoundError, PermissionError, ValueError):
                    pass  # Expected failure

        assert not generation_failures, "Project generation failures:\n" + "\n".join(
            f"  - {failure}" for failure in generation_failures
        )

    def test_package_import_validation(self, repo_name_test_cases):
        """Test that generated packages can be properly imported."""
        import_failures = []

        for test_case in repo_name_test_cases:
            if not test_case.should_generate:
                continue

            template_values = {
                "repo_name": test_case.repo_name,
                "package_import_name": test_case.expected_package_name,
            }

            test_id = f"import-test-{hash(test_case.repo_name) % 10000}-{int(time.time() * 1000) % 10000}"

            try:
                generated_dir = generate_project(template_values, test_id)
                import_success = validate_package_import(generated_dir, test_case.expected_package_name)

                if test_case.should_import and not import_success:
                    import_failures.append(
                        f"{test_case.description}: package '{test_case.expected_package_name}' "
                        f"should be importable but import failed"
                    )
                elif not test_case.should_import and import_success:
                    import_failures.append(
                        f"{test_case.description}: package '{test_case.expected_package_name}' "
                        f"should not be importable but import succeeded"
                    )

            except (subprocess.CalledProcessError, FileNotFoundError, PermissionError) as e:
                import_failures.append(f"{test_case.description}: import test failed with {type(e).__name__}: {e}")

        assert not import_failures, "Package import validation failures:\n" + "\n".join(
            f"  - {failure}" for failure in import_failures
        )

    def _validate_project_structure(self, project_dir: Path, package_name: str) -> List[str]:
        """Validate that generated project has correct structure."""
        errors = []

        # Check basic files exist
        if not (project_dir / "pyproject.toml").exists():
            errors.append("Missing pyproject.toml")

        if not (project_dir / "src").exists():
            errors.append("Missing src directory")

        # Check package directory
        package_dir = project_dir / "src" / package_name
        if not package_dir.exists():
            errors.append(f"Missing package directory: src/{package_name}")
        elif not (package_dir / "__init__.py").exists():
            errors.append(f"Missing __init__.py in package: src/{package_name}")

        return errors


# Helper functions that will initially be missing/broken (TDD red phase)
def convert_repo_name_to_package_name(repo_name: str) -> str:
    """Convert repository name to valid Python package import name."""
    if not repo_name:
        return ""

    # Handle edge cases that should fail
    if repo_name.startswith("-") or repo_name.endswith("-"):
        return repo_name.strip("-").replace("-", "_")

    # Convert hyphens to underscores
    package_name = repo_name.replace("-", "_")

    # Handle names starting with numbers - prefix with "project_"
    if repo_name.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")):
        package_name = f"project_{package_name}"

    return package_name


def validate_package_import(project_dir: Path, package_name: str) -> bool:
    """Test if a generated package can be imported."""
    if not package_name or not package_name.isidentifier():
        return False

    # Check if package directory and __init__.py exist
    package_dir = project_dir / "src" / package_name
    if not package_dir.exists() or not (package_dir / "__init__.py").exists():
        return False

    # Test if package name is valid Python identifier
    try:
        compile(f"import {package_name}", "<string>", "exec")
        return True
    except (SyntaxError, ValueError):
        return False
