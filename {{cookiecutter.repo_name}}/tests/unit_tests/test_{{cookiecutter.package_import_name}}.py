"""Test the {{cookiecutter.package_import_name}} package functionality."""

from {{cookiecutter.package_import_name}} import states_info


def test_is_city_capitol_of_state():
    """Test that is_city_capitol_of_state works correctly."""
    # Test a known capital
    assert states_info.is_city_capitol_of_state("Denver", "Colorado")
    
    # Test a non-capital city
    assert not states_info.is_city_capitol_of_state("Chicago", "Illinois")
    
    # Test with incorrect state
    assert not states_info.is_city_capitol_of_state("Denver", "California")


def test_slow_add():
    """Test the slow_add function."""
    result = states_info.slow_add(2, 3)
    assert result == 5
    
    result = states_info.slow_add(0, 0)
    assert result == 0
    
    result = states_info.slow_add(-1, 1)
    assert result == 0