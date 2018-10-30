.. Excalibur documentation master file, created by
   sphinx-quickstart on Tue Oct 16 18:31:41 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Excalibur: A web interface for Camelot
======================================

(PDF Table Extraction for Humans)
---------------------------------

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

**Excalibur** is a web interface to extract data tables from PDFs, written in **Python 3**! It powered by `Camelot <https://camelot-py.readthedocs.io/>`_.

.. note:: Excalibur only works with text-based PDFs and not scanned documents. (As Tabula `explains`_, "If you can click and drag to select text in your table in a PDF viewer, then your PDF is text-based".)

.. _explains: https://github.com/tabulapdf/tabula#why-tabula

Using Excalibur
---------------

After :ref:`installation <install>`, you can start the webserver using::

    $ excalibur webserver

That's it! Now you can go to http://localhost:5000 and extract data tables from your PDFs using the interface! Check out the `usage section`_ for step-by-step instructions.

.. note:: You can also download executables for Windows and Linux from the `releases page`_!

.. _usage section: https://excalibur-py.readthedocs.io/en/master/user/usage.html
.. _releases page: https://github.com/camelot-dev/excalibur/releases

.. image:: _static/usage.gif

Why Excalibur?
--------------

- **Excalibur gives you complete control over your data**. All file storage and processing happens on your own local or remote machine.
- Table extraction :ref:`rules <concepts>` can be **saved as presets** which can then be applied on different PDFs to extract tables with similar structures. (*in v0.2.0*)
- Extract tables from **multiple PDFs in one go** using an extraction rule, by starting :ref:`jobs <concepts>`. (*in v0.2.0*)
- Excalibur **can be configured with MySQL and Celery** for parallel and distributed workloads. (*in v0.2.0*) By default, sqlite and multiprocessing are used for sequential workloads.

Excalibur uses `Camelot <https://camelot-py.readthedocs.io/>`_ under the hood. You can check out its `comparison with other PDF table extraction libraries and tools`_.

.. _comparison with other PDF table extraction libraries and tools: https://github.com/socialcopsdev/camelot/wiki/Comparison-with-other-PDF-Table-Extraction-libraries-and-tools

Support us on Patreon
---------------------

If Excalibur solves your PDF table extraction needs, please consider supporting its development by `becoming a patron`_!

.. _becoming a patron: https://www.patreon.com/vinayakmehta

The User Guide
--------------

This part of the documentation focuses on instructions to get you up and running with Excalibur.

.. toctree::
   :maxdepth: 2

   user/intro
   user/install
   user/concepts
   user/usage

The Contributor Guide
---------------------

If you want to contribute to the project, this part of the documentation is for
you.

.. toctree::
   :maxdepth: 2

   dev/contributing
