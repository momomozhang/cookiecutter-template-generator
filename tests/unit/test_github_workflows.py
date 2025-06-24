"""Test GitHub Actions workflow structure and validation."""

import pytest
import yaml

from tests.consts import PROJECT_DIR


class TestWorkflowStructure:
    """Test basic GitHub Actions CI workflow structure."""

    @pytest.fixture
    def ci_workflow_path(self):
        """Path to CI workflow file."""
        return PROJECT_DIR / ".github" / "workflows" / "ci.yaml"

    def test_ci_workflow_file_exists(self, ci_workflow_path):
        """Test that CI workflow file exists."""
        assert ci_workflow_path.exists(), f"CI workflow not found at {ci_workflow_path}"

    def test_ci_workflow_has_valid_yaml_syntax(self, ci_workflow_path):
        """Test that CI workflow has valid YAML syntax."""
        with open(ci_workflow_path, encoding="utf-8") as f:
            workflow = yaml.safe_load(f)
        assert workflow is not None, "Workflow YAML is empty or invalid"
        assert isinstance(workflow, dict), "Workflow must be a YAML dictionary"

    def test_ci_workflow_has_required_structure(self, ci_workflow_path):
        """Test that CI workflow has required GitHub Actions structure."""
        with open(ci_workflow_path, encoding="utf-8") as f:
            workflow = yaml.safe_load(f)

        # Required top-level keys
        assert "name" in workflow, "Workflow must have a name"
        # YAML parses 'on:' as True, so check for boolean key or string key
        assert True in workflow or "on" in workflow, "Workflow must have trigger conditions"
        assert "jobs" in workflow, "Workflow must have jobs"

        # Required job structure
        jobs = workflow["jobs"]
        assert len(jobs) > 0, "Workflow must have at least one job"

        # Each job must have required keys
        for job_name, job_config in jobs.items():
            assert "runs-on" in job_config, f"Job {job_name} must specify runs-on"
            assert "steps" in job_config, f"Job {job_name} must have steps"
