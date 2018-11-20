.. Excalibur documentation master file, created by
   sphinx-quickstart on Tue Oct 16 18:31:41 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Excalibur: PDF Table Extraction for Humans
==========================================

Release v\ |version|. (:ref:`Installation <install>`)

.. image:: https://readthedocs.org/projects/excalibur-py/badge/?version=master
    :target: https://excalibur-py.readthedocs.io/en/master/
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/excalibur-py.svg
    :target: https://pypi.org/project/excalibur-py/

.. image:: https://img.shields.io/pypi/l/excalibur-py.svg
    :target: https://pypi.org/project/excalibur-py/

.. image:: https://img.shields.io/pypi/pyversions/excalibur-py.svg
    :target: https://pypi.org/project/excalibur-py/

.. image:: https://badges.gitter.im/camelot-dev/Lobby.png
    :target: https://gitter.im/camelot-dev/Lobby

**Excalibur** is a web interface to extract data tables from PDFs, written in **Python 3**! It powered by `Camelot <https://camelot-py.readthedocs.io/>`_.

.. note:: Excalibur only works with text-based PDFs and not scanned documents. (As Tabula `explains`_, "If you can click and drag to select text in your table in a PDF viewer, then your PDF is text-based".)

.. _explains: https://github.com/tabulapdf/tabula#why-tabula

Using Excalibur
---------------

After :ref:`installation with pip <install>`, you can initialize the metadata database using::

    $ excalibur initdb

And then start the webserver using::

    $ excalibur webserver

That's it! Now you can go to http://localhost:5000 and extract data tables from your PDFs using the interface! Check out the `usage section`_ for step-by-step instructions.

.. note:: You can also download executables for Windows and Linux from the `releases page`_!

.. _usage section: https://excalibur-py.readthedocs.io/en/master/user/usage.html
.. _releases page: https://github.com/camelot-dev/excalibur/releases

.. image:: _static/usage.gif

Why Excalibur?
--------------

- **Excalibur gives you complete control over your data**. All file storage and processing happens on your own local or remote machine.
- Excalibur can be configured with **MySQL and Celery** for parallel and distributed workloads. By default, sqlite and multiprocessing are used for sequential workloads.
- You can save table extraction :ref:`rules <concepts>` as **presets** and apply them on different PDFs to extract tables with similar structures.
- Excalibur uses `Camelot <https://camelot-py.readthedocs.io/>`_ under the hood, which can detect and extract tables better than other open-source libraries and tools. You can check out a `comparison with other libraries and tools here`_.

.. _comparison with other libraries and tools here: https://github.com/socialcopsdev/camelot/wiki/Comparison-with-other-PDF-Table-Extraction-libraries-and-tools

Support us on OpenCollective
----------------------------

If Excalibur solves your PDF table extraction needs, please consider supporting its development by `becoming a backer or a sponsor on OpenCollective`_!

.. _becoming a backer or a sponsor on OpenCollective: https://opencollective.com/excalibur

The User Guide
--------------

This part of the documentation focuses on instructions to get you up and running with Excalibur.

.. toctree::
   :maxdepth: 2

   user/intro
   user/install
   user/howto
   user/concepts
   user/usage

The Contributor Guide
---------------------

If you want to contribute to the project, this part of the documentation is for
you.

.. toctree::
   :maxdepth: 2

   dev/contributing
