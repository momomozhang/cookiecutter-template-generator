"""Test complete cookiecutter generation pipeline."""

import subprocess
from pathlib import Path

from tests.utils.project import generate_test_project, validate_project_structure
from tests.utils.cleanup import cleanup_generated_project, extract_test_session_id


class TestGenerationPipeline:
    """Test complete generation pipeline from cookiecutter to working project."""

    def test_complete_generation_pipeline(self):
        """Test full pipeline: generate → install → lint → build."""
        repo_name = "test-pipeline-project"
        package_name = "test_pipeline_project"

        # Phase 1: Generate project
        project_path = generate_test_project(repo_name, package_name)
        assert project_path.exists(), "Generated project should exist"

        try:
            # Phase 2: Install dependencies
            self._run_make_command(project_path, "install")

            # Phase 3: Run linting (second run should pass after initial cleanup)
            self._run_make_command(project_path, "lint-ci")

            # Phase 4: Build project (validates package structure is correct)
            self._run_make_command(project_path, "build")

            # Verify build artifacts exist
            dist_dir = project_path / "dist"
            assert dist_dir.exists(), "Build should create dist/ directory"

            dist_files = list(dist_dir.glob("*"))
            assert len(dist_files) > 0, "Build should create distribution files"

        finally:
            # Cleanup
            test_session_id = extract_test_session_id(project_path)
            cleanup_generated_project(project_path, test_session_id)

    def test_edge_case_repository_names_pipeline(self):
        """Test pipeline with edge case repository names."""
        test_cases = [
            ("my-awesome-project", "my_awesome_project"),
            ("data_analysis_2024", "data_analysis_2024"),
            ("web-scraper_v2", "web_scraper_v2"),
        ]

        for repo_name, expected_package_name in test_cases:
            project_path = generate_test_project(repo_name, expected_package_name)

            try:
                # Verify project generates and passes basic validation
                self._run_make_command(project_path, "install")
                self._run_make_command(project_path, "lint-ci")

                # Verify package structure is correct
                validate_project_structure(project_path, expected_package_name)

            finally:
                # Cleanup each test project
                test_session_id = extract_test_session_id(project_path)
                cleanup_generated_project(project_path, test_session_id)

    def _run_make_command(self, project_path: Path, command: str):
        """Run make command in generated project directory."""
        result = subprocess.run(
            ["make", command],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            check=False,  # We handle return code manually
        )

        assert result.returncode == 0, (
            f"Make command '{command}' failed in {project_path}:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )
