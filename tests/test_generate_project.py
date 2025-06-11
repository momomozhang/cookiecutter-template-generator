import subprocess
from pathlib import Path

THIS_DIR = Path(__file__).parent
PROJECT_DIR = THIS_DIR / "../" 

def test_can_generate_project():
    
    subprocess.run([
        "cookiecutter",
        str(PROJECT_DIR),
        "--output-dir",
        str(PROJECT_DIR / "sample"),
    ])