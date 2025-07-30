"""{{cookiecutter.repo_name}} package."""

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:  # pragma: no cover
    # Python < 3.8 fallback - not covered in standard test suite
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("{{cookiecutter.repo_name}}")
except PackageNotFoundError:  # pragma: no cover
    # Package not installed, fallback to development version
    # This path is handled by the build and install process
    __version__ = "dev"

__all__ = ["__version__"]
