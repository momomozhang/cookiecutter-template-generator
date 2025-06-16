import json
import subprocess
from copy import deepcopy
from typing import Dict

from tests.consts import PROJECT_DIR


def generate_project(template_values: Dict[str, str]):
    template_values: Dict[str, str] = deepcopy(template_values)
    cookiecutter_config = {
        "default_context": template_values,
    }
    cookiecutter_config_fpath = PROJECT_DIR / "cookiecutter-test-config.json"
    cookiecutter_config_fpath.write_text(json.dumps(cookiecutter_config))

    subprocess.run(
        [
            "cookiecutter",
            str(PROJECT_DIR),
            "--output-dir",
            str(PROJECT_DIR / "sample"),
            "--no-input",
            "--config-file",
            str(cookiecutter_config_fpath),
            "--verbose",
        ],
        check=True,
    )

    generated_repo_dir = PROJECT_DIR / "sample" / cookiecutter_config["default_context"]["repo_name"]
    return generated_repo_dir
