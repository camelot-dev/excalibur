<p align="center">
   <img src="https://raw.githubusercontent.com/camelot-dev/excalibur/master/docs/_static/excalibur-logo.png" width="200">
</p>

# Excalibur: A web interface for Camelot

## (PDF Table Extraction for Humans)

[![Documentation Status](https://readthedocs.org/projects/camelot-py/badge/?version=master)](https://camelot-py.readthedocs.io/en/master/) [![image](https://img.shields.io/pypi/v/excalibur-py.svg)](https://pypi.org/project/excalibur-py/) [![image](https://img.shields.io/pypi/l/excalibur-py.svg)](https://pypi.org/project/excalibur-py/) [![image](https://img.shields.io/pypi/pyversions/excalibur-py.svg)](https://pypi.org/project/excalibur-py/)

**Excalibur** is a web interface to extract data tables from PDFs! It is powered by [Camelot](https://camelot-py.readthedocs.io/) and works with **Python 3**.

**Note:** Excalibur only works with text-based PDFs and not scanned documents. (As Tabula [explains](https://github.com/tabulapdf/tabula#why-tabula), "If you can click and drag to select text in your table in a PDF viewer, then your PDF is text-based".)

## Using Excalibur

After [installation](https://excalibur-py.readthedocs.io/en/latest/user/install.html), you need to initialize the Excalibur metadata database using:

<pre>
$ excalibur initdb
</pre>

And then start the webserver using:

<pre>
$ excalibur webserver
</pre>

Now you can go to http://localhost:5000 and extract data tables from your PDFs using the web interface! Check out the [usage section](https://excalibur-py.readthedocs.io/en/latest/user/usage.html) of the documentation for instructions.

![usage.gif](https://excalibur-py.readthedocs.io/en/latest/_images/usage.gif)

## Why Excalibur?

- **Your data remains with you.** All file storage and processing happens on your own local or remote machine.
- Table extraction [rules](https://excalibur-py.readthedocs.io/en/latest/user/concepts.html#rule) can be **saved as presets** which can then be applied on different PDFs to extract tables with similar structures. (*in v0.2.0*)
- Execution of [jobs](https://excalibur-py.readthedocs.io/en/latest/user/concepts.html#job) which use a rule to extract tables from **multiple PDFs in one go**. (*in v0.2.0*)
- **Configurable with MySQL and Celery** for heavy workloads. (*in v0.2.0*) By default, sqlite and multiprocessing are used for light workloads.
- Job scheduling and incoming/outgoing webhooks. (*in v0.3.0*)

Excalibur uses [Camelot](https://camelot-py.readthedocs.io/) under the hood. See [comparison with other PDF table extraction libraries and tools](https://github.com/socialcopsdev/camelot/wiki/Comparison-with-other-PDF-Table-Extraction-libraries-and-tools).

## Installation

### Using pip

After [installing the dependencies for Camelot](https://camelot-py.readthedocs.io/en/master/user/install.html#using-pip) ([tk](https://packages.ubuntu.com/trusty/python-tk) and [ghostscript](https://www.ghostscript.com/)), you can simply use pip to install Excalibur:

<pre>
$ pip install excalibur-py
</pre>

### From the source code

After [installing the dependencies for Camelot](https://camelot-py.readthedocs.io/en/master/user/install.html#using-pip), clone the repo using:

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

The [Contributor's Guide](https://excalibur-py.readthedocs.io/en/latest/dev/contributing.html) has detailed information about contributing code, documentation, tests and more. We've included some basic information in this README.

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

Camelot uses [Semantic Versioning](https://semver.org/). For the available versions, see the tags on this repository. For the changelog, you can check out [HISTORY.md](https://github.com/camelot-dev/excalibur/blob/master/HISTORY.md).

## License

This project is licensed under the MIT License, see the [LICENSE](https://github.com/camelot-dev/excalibur/blob/master/LICENSE) file for details.
