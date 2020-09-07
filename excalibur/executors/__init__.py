import atexit

from .. import configuration as conf
from .celery_executor import CeleryExecutor
from .sequential_executor import SequentialExecutor

DEFAULT_EXECUTOR = None


class Executors:
    CeleryExecutor = "CeleryExecutor"
    SequentialExecutor = "SequentialExecutor"


def get_default_executor():
    global DEFAULT_EXECUTOR

    if DEFAULT_EXECUTOR is not None:
        return DEFAULT_EXECUTOR

    configure_executor(conf.get("core", "EXECUTOR"))

    return DEFAULT_EXECUTOR


def configure_executor(executor_name):
    global DEFAULT_EXECUTOR

    if DEFAULT_EXECUTOR is None:
        if executor_name == Executors.CeleryExecutor:
            DEFAULT_EXECUTOR = CeleryExecutor()
        elif executor_name == Executors.SequentialExecutor:
            DEFAULT_EXECUTOR = SequentialExecutor()
        else:
            raise NotImplementedError("Unknown executor")


def dispose_executor():
    global DEFAULT_EXECUTOR

    if DEFAULT_EXECUTOR is not None:
        DEFAULT_EXECUTOR.stop()


configure_executor(conf.get("core", "EXECUTOR"))
atexit.register(dispose_executor)
