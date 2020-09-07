import os
from threading import Timer

import click

from . import settings, __version__
from . import configuration as conf
from .tasks import split, extract
from .www.app import create_app
from .utils.database import reset_database, initialize_database
from .operators.python_operator import PythonOperator


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
    if conf.USING_SQLITE:
        sqlite_path = settings.SQL_ALCHEMY_CONN.replace("sqlite:///", "")
        if not os.path.isfile(sqlite_path):
            initialize_database()

    # https://stackoverflow.com/a/54235461/2780127
    def open_browser():
        click.launch("http://localhost:5000")

    Timer(1, open_browser).start()

    app = create_app(conf)
    app.run(
        port=conf.get("webserver", "web_server_port"),
        host=conf.get("webserver", "web_server_host"),
        use_reloader=False,
    )


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
