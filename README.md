<p align="center">
   <img src="https://raw.githubusercontent.com/camelot-dev/excalibur/master/docs/_static/excalibur-logo.png" width="200">
</p>

# Excalibur: A web interface to extract tabular data from PDFs

[![Documentation Status](https://readthedocs.org/projects/excalibur-py/badge/?version=master)](https://excalibur-py.readthedocs.io/en/master/) [![image](https://img.shields.io/pypi/v/excalibur-py.svg)](https://pypi.org/project/excalibur-py/) [![image](https://img.shields.io/pypi/l/excalibur-py.svg)](https://pypi.org/project/excalibur-py/) [![image](https://img.shields.io/pypi/pyversions/excalibur-py.svg)](https://pypi.org/project/excalibur-py/) [![Gitter chat](https://badges.gitter.im/camelot-dev/Lobby.png)](https://gitter.im/camelot-dev/Lobby) [![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![image](https://img.shields.io/badge/continous%20quality-deepsource-lightgrey)](https://deepsource.io/gh/camelot-dev/excalibur/?ref=repository-badge)

**Excalibur** is a web interface to extract tabular data from PDFs, written in **Python 3**! It is powered by [Camelot](https://camelot-py.readthedocs.io/).

**Note:** Excalibur only works with text-based PDFs and not scanned documents. (As Tabula [explains](https://github.com/tabulapdf/tabula#why-tabula), "If you can click and drag to select text in your table in a PDF viewer, then your PDF is text-based".)

## Using Excalibur

**Note:** You need to [install ghostscript](https://camelot-py.readthedocs.io/en/master/user/install-deps.html) before moving forward.

After [installing Excalibur with pip](https://excalibur-py.readthedocs.io/en/master/user/install.html), you need to initialize the metadata database using:

<pre>
$ excalibur initdb
</pre>

And then start the webserver using:

<pre>
$ excalibur webserver
</pre>

That's it! Now you can go to http://localhost:5000 and start extracting tabular data from your PDFs.


1. **Upload** a PDF and enter the page numbers you want to extract tables from.

2. Go to each page and select the table by drawing a box around it. (You can choose to skip this step since Excalibur can automatically detect tables on its own. Click on "**Autodetect tables**" to see what Excalibur sees.)

3. Choose a flavor (Lattice or Stream) from "**Advanced**".

    a. **Lattice**: For tables formed with lines.

    b. **Stream**: For tables formed with whitespaces.

4. Click on "**View and download data**" to see the extracted tables.

5. Select your favorite format (CSV/Excel/JSON/HTML) and click on "**Download**"!

**Note:** You can also download executables for Windows and Linux from the [releases page](https://github.com/camelot-dev/excalibur/releases) and run them directly!

![usage.gif](https://excalibur-py.readthedocs.io/en/master/_images/usage.gif)

## Why Excalibur?

- Extracting tables from PDFs is hard. A simple copy-and-paste from a PDF into an Excel doesn't preserve table structure. **Excalibur makes PDF table extraction very easy**, by automatically detecting tables in PDFs and letting you save them into CSVs and Excel files.
- Excalibur uses [Camelot](https://camelot-py.readthedocs.io/) under the hood, which gives you additional settings to tweak table extraction and get the best results. You can see how it performs better than other open-source tools and libraries [in this comparison](https://github.com/socialcopsdev/camelot/wiki/Comparison-with-other-PDF-Table-Extraction-libraries-and-tools).
- You can save table extraction [settings](https://excalibur-py.readthedocs.io/en/master/user/faq.html#faq) (like table areas) for a PDF once, and apply them on new PDFs to extract tables with similar structures.
- You get complete control over your data. All file storage and processing happens on your own local or remote machine.
- Excalibur can be configured with MySQL and Celery for parallel and distributed workloads. By default, sqlite and multiprocessing are used for sequential workloads.

## Installation

### Using pip

After installing [ghostscript](https://www.ghostscript.com/), which is one of the requirements for Camelot (See [install instructions](https://camelot-py.readthedocs.io/en/master/user/install-deps.html)), you can simply use pip to install Excalibur:

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

Fantastic documentation is available at [http://excalibur-py.readthedocs.io/](http://excalibur-py.readthedocs.io/).

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

## Support the development

You can support our work on Excalibur with a one-time or monthly donation [on OpenCollective](https://opencollective.com/excalibur). Organizations who use Excalibur can also sponsor the project for an acknowledgement on [our official site](https://www.tryexcalibur.com/) and this README.

Special thanks to all the users and organizations that support Excalibur!

<a href="https://opencollective.com/excalibur/backer/0/website" target="_blank"><img src="https://opencollective.com/excalibur/backer/0/avatar.svg"></a>
<a href="https://opencollective.com/excalibur/sponsor/0/website" target="_blank"><img src="https://opencollective.com/excalibur/sponsor/0/avatar.svg"></a>
<a href="https://opencollective.com/excalibur/backer/1/website" target="_blank"><img src="https://opencollective.com/excalibur/backer/1/avatar.svg"></a>
