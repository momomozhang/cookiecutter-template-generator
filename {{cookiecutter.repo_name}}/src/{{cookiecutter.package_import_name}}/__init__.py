"""{{cookiecutter.repo_name}} package."""

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # Python < 3.8 fallback
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("{{cookiecutter.repo_name}}")
except PackageNotFoundError:
    # Package not installed, fallback to development version
    __version__ = "dev"

__all__ = ["__version__"]
