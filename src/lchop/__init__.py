import importlib
import os
import sys

# Then get /tasks
task_directory = os.path.join(os.path.dirname(__file__), "tasks")

# List all files in the current directory
all_files = os.listdir(task_directory)

# Filter the files to get only Python module files (ending with .py)
module_files = [
    file[:-3] for file in all_files if file.endswith(".py") and file != "__init__.py"
]

# Dynamically import all modules
for module_name in module_files:
    module = importlib.import_module(f".tasks.{module_name}", package=__name__)


if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError  # pragma: no cover
    from importlib.metadata import version
else:
    from importlib_metadata import PackageNotFoundError  # pragma: no cover
    from importlib_metadata import version

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
