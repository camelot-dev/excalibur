import os
from typing import Any, Dict  # noqa

from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
about = {}  # type: Dict[str, Any]
with open(os.path.join(here, "excalibur", "__version__.py")) as f:
    exec(f.read(), about)

with open("README.md") as f:
    readme = f.read()

requires = [
    "camelot-py[cv]>=0.7.1",
    "celery>=4.1.1",
    "Click>=7.0",
    "configparser>=3.5.0, <3.6.0",
    "Flask>=1.0.2",
    "SQLAlchemy>=1.2.12",
    "Werkzeug<1.0.0",
]
mysql = ["mysqlclient>=1.3.6"]
all_requires = requires + mysql
dev_requires = [
    "codecov>=2.0.15",
    "pytest>=3.8.0",
    "pytest-cov>=2.6.0",
    "pytest-runner>=4.2",
    "Sphinx>=1.8.1",
]


def setup_package():
    metadata = dict(
        name=about["__title__"],
        version=about["__version__"],
        description=about["__description__"],
        long_description=readme,
        long_description_content_type="text/markdown",
        url=about["__url__"],
        author=about["__author__"],
        author_email=about["__author_email__"],
        license=about["__license__"],
        packages=find_packages(exclude=("tests",)),
        include_package_data=True,
        install_requires=requires,
        extras_require={"all": all_requires, "mysql": mysql, "dev": dev_requires},
        entry_points={
            "console_scripts": [
                "excalibur = excalibur.cli:cli",
            ],
        },
        classifiers=[
            # Trove classifiers
            # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
        ],
    )

    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup

    setup(**metadata)


if __name__ == "__main__":
    setup_package()
