Release History
===============

After 1.2.1, release notes are on [GitHub Releases](https://github.com/camelot-dev/excalibur/releases).

1.2.1 (2026-11-21)
------------------

**Bugfixes**

* [#60](https://github.com/camelot-dev/excalibur/issues/60) Show errors from page conversion and table extraction on the page instead of "Processing" forever. Existing databases get the new column automatically when the webserver starts. [#228](https://github.com/camelot-dev/excalibur/pull/228)
* `excalibur --version` reported 1.0.1; it now reads the installed package version.

**Security**

* Upgrade dependencies with open security advisories: pillow 13, pypdf 7, filelock, certifi, urllib3, requests, idna, jinja2. [#229](https://github.com/camelot-dev/excalibur/pull/229)

**Removed**

* The unmaintained PyInstaller build (`arthur.py`, `make build-executable` and the "Build packages" workflow). Install from PyPI or use the Docker image instead.

1.2.0 (2026-11-21)
------------------

**Improvements**

* New look in the Camelot brand colours, favicon, and flicker-free polling of the "Processing" pages. [#224](https://github.com/camelot-dev/excalibur/pull/224)
* Documentation moved to sphinx-book-theme, matching the Camelot docs. [#221](https://github.com/camelot-dev/excalibur/pull/221)
* Dockerfile, and a public demo at https://excalibur-sh8m.onrender.com. [#225](https://github.com/camelot-dev/excalibur/pull/225), [#226](https://github.com/camelot-dev/excalibur/pull/226)
* Tooling aligned with Camelot: ruff, pre-commit, Dependabot auto-merge. [#220](https://github.com/camelot-dev/excalibur/pull/220)

**Bugfixes**

* Saved rules load again, Lattice `line_scale` is sent correctly, and Stream tolerances read their own fields. [#216](https://github.com/camelot-dev/excalibur/pull/216)

1.1.0 (2026-11-21)
------------------

* Port to Camelot 2: no Ghostscript needed, Python 3.10 to 3.13. [#203](https://github.com/camelot-dev/excalibur/pull/203) by [Nitrodist](https://github.com/Nitrodist).
* [#196](https://github.com/camelot-dev/excalibur/issues/196) Fix the Excel download returning a 500 error. [#215](https://github.com/camelot-dev/excalibur/pull/215)
* CI with tests on Python 3.10 to 3.13 and a webserver smoke test. [#204](https://github.com/camelot-dev/excalibur/pull/204)
* Excalibur is now in maintenance mode: bug fixes and Camelot compatibility only. [#219](https://github.com/camelot-dev/excalibur/pull/219)

1.0.1 (2025-01-03)
------------------

* Fix pypdf import.

1.0.0 (2025-01-03)
------------------

* Fix deprecated camelot methods.

0.4.4 (2024-12-25)
------------------

* Add GitHub Action for automated Linux, MacOS and Windows builds. [#107](https://github.com/camelot-dev/excalibur/pull/107) by [arky](https://github.com/arky).

0.4.3 (2020-03-21)
------------------

**Improvements**

* The command-line interface can now be run using `python -m excalibur`. [#97](https://github.com/camelot-dev/excalibur/pull/97).
* Excalibur now follows the Black code style! [#98](https://github.com/camelot-dev/excalibur/pull/98).

**Bugfixes**

* [#95](https://github.com/camelot-dev/excalibur/issues/95) Fix Werkzeug import error. [#96](https://github.com/camelot-dev/excalibur/pull/96).

0.4.2 (2019-01-09)
------------------

**Bugfixes**

* [#41](https://github.com/camelot-dev/excalibur/issues/41) Fix failed function call wrt to upstream changes. [#42](https://github.com/camelot-dev/excalibur/pull/42) by Vinayak Mehta.

0.4.1 (2018-11-05)
------------------

**Bugfixes**

* [#32](https://github.com/camelot-dev/excalibur/issues/32) Changing port in excalibur.cfg has no effect. [#34](https://github.com/camelot-dev/excalibur/pull/34) by Vinayak Mehta.

0.4.0 (2018-11-26)
------------------

This release adds a lot of UI enhancements (based on user feedback), and updates to the docs and website. Table autodetection is now even more awesome 🔥 since Camelot v0.4.0 adds an improved Stream table detection algorithm. To know more, check out [#206](https://github.com/camelot-dev/camelot/pull/206).

0.3.0 (2018-11-12)
------------------

This release adds enhancements to the static website, a rule manager to view, upload and download table extraction rules and an option to load a saved extraction rule on the workspace.

0.2.0 (2018-11-05)
------------------

**Improvements**

* Add MySQL and Celery support. [#8](https://github.com/camelot-dev/excalibur/pull/8) by Vinayak Mehta.
* Add table auto-detection. [#7](https://github.com/camelot-dev/excalibur/pull/7) by Vinayak Mehta.
* Add static website. [#6](https://github.com/camelot-dev/excalibur/pull/6) by Nikhil Sikka.

0.1.1 (2018-10-22)
------------------

* Add Windows and Linux executables.

0.1.0 (2018-10-20)
------------------

* Birth!
