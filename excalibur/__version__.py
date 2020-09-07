VERSION = (0, 4, 3)
PRERELEASE = None  # alpha, beta or rc
REVISION = None


def generate_version(version, prerelease=None, revision=None):
    version_parts = [".".join(map(str, version))]
    if prerelease is not None:
        version_parts.append(f"-{prerelease}")
    if revision is not None:
        version_parts.append(f".{revision}")
    return "".join(version_parts)


__title__ = "excalibur-py"
__description__ = "A web interface to extract tabular data from PDFs."
__url__ = "https://excalibur-py.readthedocs.io/"
__version__ = ".".join(map(str, VERSION))
__author__ = "Vinayak Mehta"
__author_email__ = "vmehta94@gmail.com"
__license__ = "MIT License"
