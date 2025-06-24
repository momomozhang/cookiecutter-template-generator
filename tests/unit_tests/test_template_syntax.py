import pytest
from jinja2 import Environment, TemplateSyntaxError

from tests.consts import PROJECT_DIR


class TestJinja2SyntaxValidation:
    """Test that all template files have valid Jinja2 syntax."""

    @pytest.fixture
    def template_files(self):
        """Find all files containing cookiecutter template syntax."""
        template_dir = PROJECT_DIR / "{{cookiecutter.repo_name}}"
        template_files = []

        # Find files with {{cookiecutter.*}} syntax
        for file_path in template_dir.rglob("*"):
            if file_path.is_file():
                try:
                    content = file_path.read_text(encoding="utf-8")
                    if "{{cookiecutter." in content:
                        template_files.append(file_path)
                except (UnicodeDecodeError, PermissionError):
                    continue

        return template_files

    def test_template_files_found(self, template_files):
        """Verify we found template files to validate."""
        assert len(template_files) > 0, "No template files found for validation"

    def test_all_template_files_have_valid_jinja2_syntax(self, template_files):
        """Test that each template file has valid Jinja2 syntax."""
        jinja_env = Environment()
        syntax_errors = []

        for file_path in template_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                jinja_env.parse(content)  # This will raise TemplateSyntaxError if invalid
            except (TemplateSyntaxError, UnicodeDecodeError) as e:
                relative_path = file_path.relative_to(PROJECT_DIR)
                syntax_errors.append(f"{relative_path}: {str(e)}")

        assert not syntax_errors, "Jinja2 syntax errors found:\n" + "\n".join(syntax_errors)

    def test_template_files_render_with_sample_values(self, template_files):
        """Test that template files render successfully with sample cookiecutter values."""
        jinja_env = Environment()
        sample_context = {"cookiecutter": {"repo_name": "test-project", "package_import_name": "test_package"}}

        render_errors = []
        for file_path in template_files:
            try:
                content = file_path.read_text(encoding="utf-8")
                template = jinja_env.from_string(content)
                rendered = template.render(sample_context)
                assert rendered  # Ensure something was rendered
            except (TemplateSyntaxError, UnicodeDecodeError) as e:
                relative_path = file_path.relative_to(PROJECT_DIR)
                render_errors.append(f"{relative_path}: {str(e)}")

        assert not render_errors, "Template rendering errors:\n" + "\n".join(render_errors)
