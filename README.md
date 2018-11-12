<p align="center">
   <img src="https://raw.githubusercontent.com/camelot-dev/excalibur/master/docs/_static/excalibur-logo.png" width="200">
</p>

# Excalibur: A web interface to extract tabular data from PDFs

## (PDF Table Extraction for Humans)

[![Documentation Status](https://readthedocs.org/projects/excalibur-py/badge/?version=master)](https://excalibur-py.readthedocs.io/en/master/) [![image](https://img.shields.io/pypi/v/excalibur-py.svg)](https://pypi.org/project/excalibur-py/) [![image](https://img.shields.io/pypi/l/excalibur-py.svg)](https://pypi.org/project/excalibur-py/) [![image](https://img.shields.io/pypi/pyversions/excalibur-py.svg)](https://pypi.org/project/excalibur-py/) [![Gitter chat](https://badges.gitter.im/camelot-dev/Lobby.png)](https://gitter.im/camelot-dev/Lobby)

**Excalibur** is a web interface to extract tabular data from PDFs, written in **Python 3**! It is powered by [Camelot](https://camelot-py.readthedocs.io/).

**Note:** Excalibur only works with text-based PDFs and not scanned documents. (As Tabula [explains](https://github.com/tabulapdf/tabula#why-tabula), "If you can click and drag to select text in your table in a PDF viewer, then your PDF is text-based".)

## Using Excalibur

After [installation with pip](https://excalibur-py.readthedocs.io/en/master/user/install.html), you can initialize the metadata database using:

<pre>
$ excalibur initdb
</pre>

And then start the webserver using:

<pre>
$ excalibur webserver
</pre>

That's it! Now you can go to http://localhost:5000 and extract data tables from your PDFs using the web interface! Check out the [usage section](https://excalibur-py.readthedocs.io/en/master/user/usage.html) of the documentation for step-by-step instructions.

**Note:** You can also download executables for Windows and Linux from the [releases page](https://github.com/camelot-dev/excalibur/releases)!

![usage.gif](https://excalibur-py.readthedocs.io/en/master/_images/usage.gif)

## Why Excalibur?

- **Excalibur gives you complete control over your data**. All file storage and processing happens on your own local or remote machine.
- Excalibur can be configured with **MySQL and Celery** for parallel and distributed workloads. By default, sqlite and multiprocessing are used for sequential workloads.
- You can save table extraction [rules](https://excalibur-py.readthedocs.io/en/master/user/concepts.html#rule) as **presets** and apply them on different PDFs to extract tables with similar structures.
- You can extract tables from **multiple PDFs in one go** using an extraction rule by starting [jobs](https://excalibur-py.readthedocs.io/en/master/user/concepts.html#job). (*in v0.4.0*)

Excalibur uses [Camelot](https://camelot-py.readthedocs.io/) under the hood. You can check out its [comparison with other PDF table extraction libraries and tools](https://github.com/socialcopsdev/camelot/wiki/Comparison-with-other-PDF-Table-Extraction-libraries-and-tools).

## Support us on Patreon

If Excalibur solves your PDF table extraction needs, please consider supporting its development by [becoming a patron](https://www.patreon.com/vinayakmehta)!

## Installation

### Using pip

After installing [ghostscript](https://www.ghostscript.com/), which is one of the requirements for Camelot (See [install instructions](https://camelot-py.readthedocs.io/en/master/user/install.html#using-pip)), you can simply use pip to install Excalibur:

<pre>
$ pip install excalibur-py
</pre>

### From the source code

After installing ghostscript, clone the repo using:

<pre>
$ git clone https://www.github.com/camelot-dev/excalibur
</pre>

and install Excalibur using pip:

<pre>
$ cd excalibur
$ pip install .
</pre>

## Documentation

Great documentation is available at [http://excalibur-py.readthedocs.io/](http://excalibur-py.readthedocs.io/).

## Development

The [Contributor's Guide](https://excalibur-py.readthedocs.io/en/master/dev/contributing.html) has detailed information about contributing code, documentation, tests and more. We've included some basic information in this README.

### Source code

You can check the latest sources with:

<pre>
$ git clone https://www.github.com/camelot-dev/excalibur
</pre>

### Setting up a development environment

You can install the development dependencies easily, using pip:

<pre>
$ pip install excalibur-py[dev]
</pre>

### Testing (soon)

After installation, you can run tests using:

<pre>
$ python setup.py test
</pre>

## Versioning

Excalibur uses [Semantic Versioning](https://semver.org/). For the available versions, see the tags on this repository. For the changelog, you can check out [HISTORY.md](https://github.com/camelot-dev/excalibur/blob/master/HISTORY.md).

## License

This project is licensed under the MIT License, see the [LICENSE](https://github.com/camelot-dev/excalibur/blob/master/LICENSE) file for details.
