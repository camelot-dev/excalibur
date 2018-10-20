# -*- coding: utf-8 -*-

import atexit

from .sequential_executor import SequentialExecutor
from .. import configuration as conf


DEFAULT_EXECUTOR = None


class Executors:
    SequentialExecutor = "SequentialExecutor"


def configure_executor(executor_name):
    global DEFAULT_EXECUTOR

    if DEFAULT_EXECUTOR is None:
        if executor_name == Executors.SequentialExecutor:
            DEFAULT_EXECUTOR = SequentialExecutor()
        else:
            raise NotImplementedError('Unknown executor')


def dispose_executor():
    global DEFAULT_EXECUTOR

    if DEFAULT_EXECUTOR is not None:
        DEFAULT_EXECUTOR.stop()


configure_executor(conf.EXECUTOR)
atexit.register(dispose_executor)
