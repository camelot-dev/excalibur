# -*- coding: utf-8 -*-

import atexit

import click

from . import __version__
from . import configuration as conf
from .utils.database import initialize_database, reset_database
from .www.app import create_app
from .executors import DEFAULT_EXECUTOR


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.group()
@click.version_option(version=__version__)
def cli(*args, **kwargs):
    pass


@cli.command()
def webserver(*args, **kwargs):
    app = create_app(conf)
    app.run(use_reloader=False)


@cli.command()
def initdb(*args, **kwargs):
    initialize_database()


@cli.command()
def resetdb(*args, **kwargs):
    click.confirm(
        "This will drop existing tables if they exist. Proceed?", abort=True)

    reset_database()
    initialize_database()
