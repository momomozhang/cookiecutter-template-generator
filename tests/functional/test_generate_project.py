from pathlib import Path


def test_can_generate_project(project_dir: Path):
    assert project_dir.exists()
