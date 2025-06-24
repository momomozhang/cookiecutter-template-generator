import json
import re

import pytest

from tests.consts import PROJECT_DIR
from tests.utils.template import find_template_files


class TestTemplateVariableConsistency:
    """Test that cookiecutter variables are used consistently across template files."""

    @pytest.fixture
    def template_files(self):
        """Find all template files containing cookiecutter variables."""
        return find_template_files()

    @pytest.fixture
    def expected_variables(self):
        """Define expected cookiecutter variables from cookiecutter.json."""
        cookiecutter_json = PROJECT_DIR / "cookiecutter.json"
        with open(cookiecutter_json, encoding="utf-8") as f:
            config = json.load(f)
        return set(config.keys())

    def test_all_template_variables_are_defined(self, template_files, expected_variables):
        """Test that all {{cookiecutter.*}} variables used in templates are defined in cookiecutter.json."""
        undefined_vars = []

        for file_path in template_files:
            content = file_path.read_text(encoding="utf-8")
            # Find all {{cookiecutter.variable_name}} patterns
            found_vars = re.findall(r"\{\{cookiecutter\.([^}]+)\}\}", content)

            for var in found_vars:
                if var not in expected_variables:
                    relative_path = file_path.relative_to(PROJECT_DIR)
                    undefined_vars.append(f"{relative_path}: {{{{cookiecutter.{var}}}}}")

        assert not undefined_vars, "Undefined cookiecutter variables found:\n" + "\n".join(undefined_vars)

    def test_required_variables_are_used(self, template_files, expected_variables):
        """Test that all defined cookiecutter variables are actually used in templates."""
        # Extract all used variables
        used_vars = set()
        for file_path in template_files:
            content = file_path.read_text(encoding="utf-8")
            found_vars = re.findall(r"\{\{cookiecutter\.([^}]+)\}\}", content)
            used_vars.update(found_vars)

        unused_vars = expected_variables - used_vars
        assert not unused_vars, f"Unused cookiecutter variables in cookiecutter.json: {sorted(unused_vars)}"

    def test_repo_name_consistency(self, template_files):
        """Test that repo_name is used consistently (no typos like repo-name, reponame)."""
        inconsistent_usage = []

        for file_path in template_files:
            content = file_path.read_text(encoding="utf-8")
            # Look for variations that might be typos
            suspicious_patterns = [
                r"\{\{cookiecutter\.repo[_-]?name[s]?\}\}",  # repo_names, repo-name, etc.
                r"\{\{cookiecutter\.repository[_-]?name\}\}",  # repository_name
            ]

            for pattern in suspicious_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if match != "{{cookiecutter.repo_name}}":
                        relative_path = file_path.relative_to(PROJECT_DIR)
                        inconsistent_usage.append(f"{relative_path}: {match}")

        assert not inconsistent_usage, "Inconsistent repo_name usage:\n" + "\n".join(inconsistent_usage)

    def test_package_import_name_consistency(self, template_files):
        """Test that package_import_name is used consistently."""
        inconsistent_usage = []

        for file_path in template_files:
            content = file_path.read_text(encoding="utf-8")
            # Look for variations
            suspicious_patterns = [
                r"\{\{cookiecutter\.package[_-]?import[_-]?name[s]?\}\}",
                r"\{\{cookiecutter\.import[_-]?name\}\}",
                r"\{\{cookiecutter\.package[_-]?name\}\}",
            ]

            for pattern in suspicious_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if match != "{{cookiecutter.package_import_name}}":
                        relative_path = file_path.relative_to(PROJECT_DIR)
                        inconsistent_usage.append(f"{relative_path}: {match}")

        assert not inconsistent_usage, "Inconsistent package_import_name usage:\n" + "\n".join(inconsistent_usage)
