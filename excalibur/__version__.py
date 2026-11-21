from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

__title__ = "excalibur-py"
__description__ = "A web interface to extract tabular data from PDFs."
__url__ = "https://excalibur-py.readthedocs.io/"
try:
    # Single source of truth: the version in pyproject.toml.
    __version__ = version("excalibur-py")
except PackageNotFoundError:  # running from a source tree without install
    __version__ = "0+unknown"
__author__ = "Vinayak Mehta"
__author_email__ = "vmehta94@gmail.com"
__license__ = "MIT License"
