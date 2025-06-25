"""Example test fixture for generated project."""

import pytest


@pytest.fixture
def sample_data():
    """Provide sample data for tests.
    
    Returns:
        Sample test data that can be used in tests
        
    """
    return {"test_key": "test_value", "numbers": [1, 2, 3]}
