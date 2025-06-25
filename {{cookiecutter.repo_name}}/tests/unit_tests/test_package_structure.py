"""Test package structure and basic functionality."""

from pathlib import Path

import {{cookiecutter.package_import_name}}
import {{cookiecutter.package_import_name}}.states_info


def test_package_can_be_imported():
    """Test that the package can be imported without errors."""
    # Package should have the expected structure
    assert hasattr({{cookiecutter.package_import_name}}, '__version__')


def test_package_has_required_modules():
    """Test that the package contains expected modules."""
    # Module should have expected functions
    assert hasattr({{cookiecutter.package_import_name}}.states_info, 'is_city_capitol_of_state')
    assert hasattr({{cookiecutter.package_import_name}}.states_info, 'slow_add')


def test_package_data_files_exist():
    """Test that package data files are included."""
    package_dir = Path({{cookiecutter.package_import_name}}.__file__).parent
    cities_json = package_dir / "cities.json"
    
    assert cities_json.exists(), "cities.json data file should be included"
    assert cities_json.stat().st_size > 0, "cities.json should not be empty"