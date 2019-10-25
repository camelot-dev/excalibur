.. _howto:

How-to Guides
=============

Excalibur's architecture is heavily inspired from Airflow, so you may experience déjà vu while reading this page of the documentation. `Airflow LICENSE`_.

.. _Airflow LICENSE: https://github.com/apache/incubator-airflow/blob/master/LICENSE

Setting Configuration Options
-----------------------------

The first time you run Excalibur, it will create a file called ``excalibur.cfg`` in your ``$EXCALIBUR_HOME`` directory (``~/excalibur`` by default). This file contains Excalibur’s configuration and you can edit it to change any of the settings.

For example, the metadata database connection string can be set in ``excalibur.cfg`` like this::

    [core]
    sql_alchemy_conn = my_conn_string

Resetting the Metadata Database
-------------------------------

.. warning:: The following command will wipe your Excalibur metadata database, removing all information about uploaded files, saved settings and finished/in-progress jobs.

You can reset the metadata database using::

    $ excalibur resetdb

Using the MySQL Database Backend
--------------------------------

Excalibur uses SqlAlchemy to connect to a database backend. By default, a sqlite database is used. To use MySQL, you need to first install MySQL and then create a database and a user.

Installing MySQL
^^^^^^^^^^^^^^^^

To use the MySQL database backend, you need to install Excalibur using::

    $ pip install excalibur-py[mysql]

You can install MySQL using your system's package manager. For Ubuntu::

    $ sudo apt update
    $ sudo apt install mysql-server libmysqlclient-dev

And then set it up using::

    $ sudo mysql_secure_installation

Setup
^^^^^

Now you can create the a database and a user for Excalibur::

    > CREATE DATABASE excalibur CHARACTER SET utf8 COLLATE utf8_unicode_ci;
    > GRANT ALL ON excalibur.* TO 'excalibur'@'%' IDENTIFIED BY '1234';

Finally, you need to change the ``sql_alchemy_conn`` in ``excalibur.cfg`` to::

    [core]
    sql_alchemy_conn = mysql://excalibur:1234@localhost:3306/excalibur

And initialize the metadata database using::

    $ excalibur initdb

Scaling Out with Celery
-----------------------

``CeleryExecutor`` is one of the ways you can scale out the number of workers. For this to work, you need to setup a Celery backend (RabbitMQ, Redis, …) and change your excalibur.cfg to point the executor parameter to ``CeleryExecutor`` and provide the related Celery settings.

For more information about setting up a Celery broker, refer to the exhaustive `Celery documentation on the topic`_.

.. _Celery documentation on the topic: http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html

To kick off a worker, you need to setup Excalibur and kick off the worker subcommand::

    $ excalibur worker

Your worker should start picking up tasks as soon as they get fired in its direction.
