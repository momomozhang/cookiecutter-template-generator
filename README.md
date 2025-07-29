# My Python Project Starter

This is my personal tool to bootstrap a new Python project. It's all done through a GitHub Action.

## How to Create a New Project

1. Go to this repo's **Actions** tab.
2. Find the **"Create New Python Repository"** workflow.
3. Click **"Run workflow"**.
4. Type in the new `repo_name` (e.g., `my-cool-app`).
5. Type in the `package_import_name` (e.g., `my_cool_app`).
6. Click the green "Run workflow" button.

That's it. The action will build the new repo, push the code, and open a PR for final setup.

## What I Get

Each new project comes with:
- A modern `pyproject.toml` setup.
- `pytest` for testing.
- `ruff` and `pylint` for code quality.
- A basic CI workflow that runs tests.
- **Automatic PyPI publishing** - users can `pip install` your package once published.

## Setup Note

This requires three secrets to be set up in *this* template repo:
- `PERSONAL_GITHUB_TOKEN` - for creating and configuring repos
- `TEST_PYPI_TOKEN` - for publishing to test PyPI
- `PROD_PYPI_TOKEN` - for publishing to production PyPI
