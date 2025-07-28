# Cookiecutter Python Package Generator

> A Cookiecutter template for creating modern Python packages with pre-configured CI/CD, testing, and release automation.

This template provides a standardized, production-ready foundation for Python projects. It includes a `src/` layout, `pyproject.toml` configuration, pre-commit hooks, GitHub Actions workflows, and automated publishing to PyPI.

[![CI](https://github.com/momomozhang/cookiecutter-template-generator/workflows/CI/badge.svg)](https://github.com/momomozhang/cookiecutter-template-generator/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Modern Package Structure**: `src/` layout, `pyproject.toml` (PEP 621), and dynamic versioning
- **CI/CD Pipeline**: GitHub Actions for linting, testing, building, and publishing
- **Code Quality**: Pre-configured with `ruff`, `pylint`, `pre-commit`, and `pytest`
- **GitHub Integration**: Automated repo creation, branch protection, secret management
- **PyPI Publishing**: Automated test and production publishing workflows
- **Sensible Defaults**: Pre-configured for most use cases with minimal setup required

## Generated Project Structure

```
your-repo-name/
├── src/your_package_name/          # Your Python package
│   ├── __init__.py
│   ├── cities.json                 # Sample data
│   └── states_info.py              # Sample module
├── tests/                          # Comprehensive test suite
│   ├── conftest.py
│   └── unit_tests/
├── pyproject.toml                  # Complete build configuration
├── version.txt                     # Dynamic versioning
├── run.sh                         # Automation scripts
├── Makefile                       # Convenient commands
├── .github/workflows/             # Complete CI/CD pipeline
│   └── build-test-publish.yaml
└── .pre-commit-config.yaml        # Code quality hooks
```

## Quick Start

### Prerequisites

- Python 3.10+
- Git configured with user name/email
- GitHub CLI (`gh`) authenticated (for automation)

### Installation

```bash
pip install cookiecutter pytest pre-commit pytest-cov
```

### Generate Your First Project

```bash
# 1. Clone this repository
git clone https://github.com/momomozhang/cookiecutter-template-generator.git
cd cookiecutter-template-generator

# 2. Generate project with default values
make generate-project
cd sample/repo-name/

# 3. Install and test the generated project
make install    # Install in editable mode with dev dependencies
make test       # Run all tests with coverage
make lint       # Run pre-commit hooks
make build      # Build wheel and sdist
```

### GitHub Repository Automation (Optional)

```bash
# Set environment variables
export REPO_NAME="your-repo-name"
export PACKAGE_IMPORT_NAME="your_package_name"
export GITHUB_USERNAME=""
export TEST_PYPI_TOKEN="your-test-token"
export PROD_PYPI_TOKEN="your-prod-token"

# Automated GitHub setup
bash run.sh create-repo-if-not-exists    # Creates GitHub repo
bash run.sh configure-repo                # Sets up secrets & protection
bash run.sh open-pr-with-generated-project # Creates PR with template
```

## Use Cases

### When to Use This Template

- New Python packages that need professional setup
- Team standardization across multiple projects
- Open source projects requiring comprehensive CI/CD
- Packages with quality gates and automation requirements
- Learning modern Python packaging standards

### When NOT to Use This Template

- Simple scripts or single-file projects
- Projects where Python isn't the main language
- Existing codebases without major restructuring plans
- Quick prototypes where setup overhead exceeds value
- Very simple packages with no dependencies

## How It Works

This template creates two things:
1. **The template itself** - manages cookiecutter variables and automation scripts
2. **Your Python package** - the actual project with all the bells and whistles

Once you generate a project, you get a complete CI/CD pipeline that:
- Checks your code quality with ruff and pylint
- Runs your tests automatically  
- Builds your package
- Publishes to PyPI when you're ready

Plus some nice GitHub integration that can create repos, set up secrets, and even open pull requests for you.


## Common Commands

Once you've generated a project, here's what you'll use most:

```bash
make install        # Set up your dev environment
make test          # Run your tests
make lint          # Check code quality
make build         # Build your package
make publish-test  # Publish to test PyPI first
make publish-prod  # Publish to real PyPI
```

## Extra Features

**Security stuff:**
- Keeps your PyPI tokens safe in GitHub Actions
- Sets up branch protection so bad code doesn't slip through
- Pre-commit hooks catch issues before you commit
- Dependabot watches for vulnerable dependencies

**For teams:**
- Scripts to create multiple repos at once
- Works with private PyPI servers
- Consistent structure across all your projects

## Troubleshooting

**Something broke?** Here are the usual suspects:

- Make sure you have `cookiecutter` installed: `pip install cookiecutter`
- Python version issues? You need 3.10 or newer
- GitHub CLI acting up? Try `gh auth logout` then `gh auth login`
- Tests failing? Run `make test-quick` to skip the slow ones
- Can't publish? Test it first with `make publish-test`

Still stuck? Check the [GitHub issues](https://github.com/momomozhang/cookiecutter-template-generator/issues) or open a new one.

## Contributing

Want to help out? Great! Check the issues page or open a new one to chat about what you'd like to work on.

To get started:
```bash
git clone https://github.com/momomozhang/cookiecutter-template-generator.git
cd cookiecutter-template-generator
make install && make test
```

## Similar Tools

- [Cookiecutter](https://github.com/cookiecutter/cookiecutter) - The engine that powers this
- [PyScaffold](https://github.com/pyscaffold/pyscaffold) - Another Python project generator
- [Poetry](https://github.com/python-poetry/poetry) - Modern Python dependency management

---

Ready to try it out?

```bash
git clone https://github.com/momomozhang/cookiecutter-template-generator.git
cd cookiecutter-template-generator
make generate-project
```
