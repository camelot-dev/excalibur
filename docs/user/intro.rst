.. _intro:

Introduction
============

Excalibur is a web interface built on top of `Camelot`_, which is a Python library to extract tabular data from PDFs.

.. _Camelot: https://camelot-py.readthedocs.io/

What's in a name?
-----------------

Camelot was named after `The Camelot Project`_ (also the name of a castle in the `Arthurian legend`_). To follow the same theme, this project was named `Excalibur`_, which is the legendary sword of King Arthur.

.. _The Camelot Project: http://www.planetpdf.com/planetpdf/pdfs/warnock_camelot.pdf
.. _Arthurian legend: https://en.wikipedia.org/wiki/King_Arthur
.. _Excalibur: https://en.wikipedia.org/wiki/Excalibur

Why another tool?
-----------------

There are both open (`Tabula`_, `pdfplumber`_) and closed-source (`Smallpdf`_, `Docparser`_) tools that are widely used to extract data tables from PDFs. They either give a nice output or fail miserably. There is no in between. This is not helpful since everything in the real world, including PDF table extraction, is fuzzy. This leads to the creation of ad-hoc table extraction scripts for each type of PDF table.

Excalibur uses Camelot under the hood, which was created to offer users complete control over table extraction. If you can't get your desired output with the default settings, you can tweak them and get the job done!

Here is a `comparison`_ of Camelot's output with outputs from other open-source PDF parsing libraries and tools.

.. _Tabula: http://tabula.technology
.. _pdfplumber: https://github.com/jsvine/pdfplumber
.. _Smallpdf: https://smallpdf.com
.. _Docparser: https://docparser.com
.. _comparison: https://github.com/socialcopsdev/camelot/wiki/Comparison-with-other-PDF-Table-Extraction-libraries-and-tools

Excalibur LICENSE
-----------------

    .. include:: ../../LICENSE
