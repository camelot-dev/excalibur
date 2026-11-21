"""Configuration file for the Sphinx documentation builder.

Builds Excalibur's documentation with sphinx-book-theme, using the same
template and brand styling as the Camelot documentation.
"""

import os
import sys
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version

sys.path.insert(0, os.path.abspath("_themes"))

# -- General configuration ------------------------------------------------

extensions = [
    "sphinx_copybutton",
    "myst_parser",
]

source_suffix = ".rst"
master_doc = "index"

project = "Excalibur"
copyright = "2026, Camelot Developers"
author = "Camelot Developers"

try:
    release = _pkg_version("excalibur-py")
except PackageNotFoundError:
    release = "unknown"
version = release

language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

pygments_style = "flask_theme_support.FlaskyStyle"

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# -- Options for HTML output ----------------------------------------------

html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_url": "https://github.com/camelot-dev/excalibur",
    "repository_branch": "master",
    "path_to_docs": "/docs",
    "use_repository_button": True,
}

html_logo = "_static/excalibur-logo.png"
html_favicon = "_static/favicon.ico"
html_static_path = ["_static"]
html_css_files = ["excalibur-theme.css"]

html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True

htmlhelp_basename = "excalibur-doc"

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {}

latex_documents = [
    (
        master_doc,
        "Excalibur.tex",
        "Excalibur Documentation",
        "Camelot Developers",
        "manual",
    ),
]

# -- Options for manual page output ---------------------------------------

man_pages = [(master_doc, "Excalibur", "Excalibur Documentation", [author], 1)]

# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
    (
        master_doc,
        "Excalibur",
        "Excalibur Documentation",
        author,
        "Excalibur",
        "A web interface to extract tabular data from PDFs.",
        "Miscellaneous",
    ),
]

# -- Options for Epub output ----------------------------------------------

epub_title = project
epub_exclude_files = ["search.html"]
