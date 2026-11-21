.. _install:

Installation of Excalibur
=========================

This part of the documentation covers the steps to install Excalibur.

Excalibur requires Python 3.11 or newer and is built on Camelot 2. Camelot 2
renders PDF pages with pypdfium2, so you no longer need to install Ghostscript
or any other system dependency.

Using pip
---------

You can simply use pip to install Excalibur::

    $ pip install excalibur-py

From the source code
--------------------

Clone the repo using::

    $ git clone https://www.github.com/camelot-dev/excalibur

and install Excalibur using pip::

    $ cd excalibur
    $ pip install .
