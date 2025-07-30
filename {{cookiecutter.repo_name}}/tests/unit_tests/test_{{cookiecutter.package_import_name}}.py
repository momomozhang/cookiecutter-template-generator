"""Test the {{cookiecutter.package_import_name}} package functionality."""

import {{cookiecutter.package_import_name}}


def test_package_version():
    """Test that package has a version attribute."""
    assert hasattr({{cookiecutter.package_import_name}}, '__version__')
    assert {{cookiecutter.package_import_name}}.__version__ is not None