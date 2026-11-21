import os
from threading import Timer

import click

from . import __version__
from . import configuration as conf
from .operators.python_operator import PythonOperator
from .tasks import extract
from .tasks import split
from .utils.database import initialize_database
from .utils.database import reset_database
from .www.app import create_app


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


def _run(task_name, task_id):
    task_bag = {"split": split, "extract": extract}
    python_callable = task_bag[task_name]
    task = PythonOperator(python_callable, op_args=[task_id])
    task.execute()


@click.group()
@click.version_option(version=__version__)
def cli(*args, **kwargs):
    pass


@cli.command("initdb")
def initdb(*args, **kwargs):
    initialize_database()


@cli.command("resetdb")
def resetdb(*args, **kwargs):
    click.confirm("This will drop existing tables if they exist. Proceed?", abort=True)

    reset_database()
    initialize_database()


@cli.command("webserver")
def webserver(*args, **kwargs):
    # Idempotent: creates missing tables and upgrades older databases.
    initialize_database()

    port = int(
        os.environ.get("EXCALIBUR_WEB_PORT", conf.get("webserver", "web_server_port"))
    )
    host = os.environ.get(
        "EXCALIBUR_WEB_HOST", conf.get("webserver", "web_server_host")
    )

    # https://stackoverflow.com/a/54235461/2780127
    def open_browser():
        click.launch(f"http://127.0.0.1:{port}")

    if host in ("127.0.0.1", "localhost", "::1"):
        Timer(1, open_browser).start()

    app = create_app(conf)
    app.run(port=port, host=host, use_reloader=False)


@cli.command("worker")
def worker(*args, **kwargs):
    from celery.bin import worker

    from .executors.celery_executor import app as celery_app

    worker = worker.worker(app=celery_app)
    options = {
        "concurrency": int(conf.get("celery", "WORKER_CONCURRENCY")),
        "loglevel": conf.get("core", "LOGGING_LEVEL"),
    }
    worker.run(**options)


@cli.command("run")
@click.option("-t", "--task")
@click.option("-id", "--uuid")
def run(*args, **kwargs):
    _run(kwargs["task"], kwargs["uuid"])
