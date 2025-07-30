"""Test package structure and basic functionality."""

import {{cookiecutter.package_import_name}}


def test_package_can_be_imported():
    """Test that the package can be imported without errors."""
    # Package should have the expected structure
    assert hasattr({{cookiecutter.package_import_name}}, '__version__')