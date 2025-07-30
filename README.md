![alt text](cookiecutter_repo_readme_demo.png)

# My Python Project Starter

My personal tool to bootstrap a new Python project, all done through a GitHub Action.
It's the final project from `Taking Python to Production Course` by @phitoduck

## 👉 [Check a generated repo here](https://github.com/momomozhang/example_20250730_01_generated_repo) 👈

## 🎉 What I learned:
- CI/CD principles and Github Actions
- Pytest testing and coverage
- Bash scripting and shell automation
- Pre-commit hooks and automated code quality
- Pyproject.toml configuration
- Setuptools and PyPI publishing workflows
- Repository automation
- Cookiecutter templating


## What I Get

Each new project comes with:
- A modern `pyproject.toml` setup.
- `pytest` for testing.
- `ruff` and `pylint` for code quality.
- A basic CI workflow that runs tests.
- **Automatic PyPI publishing** - users can `pip install` my package once published.
- Automatically includes non-Python files (JSON, YAML, etc.) in the PyPI distributions with proper `pyproject.toml` configuration

## Setup Note

This requires three secrets to be set up in *this* template repo:
- `PERSONAL_GITHUB_TOKEN` - for creating and configuring repos
- `TEST_PYPI_TOKEN` - for publishing to test PyPI
- `PROD_PYPI_TOKEN` - for publishing to production PyPI

## Stey by step guide

1. Go to this repo's **Actions** tab.
2. Find the **"Create New Python Repository"** workflow.
3. Click **"Run workflow"**.
4. Type in the new `repo_name` (e.g., `my-cool-app`).
5. Type in the `package_import_name` (e.g., `my_cool_app`).
6. Click the green "Run workflow" button.

That's it. The action will build the new repo, push the code, and open a PR for final setup.
