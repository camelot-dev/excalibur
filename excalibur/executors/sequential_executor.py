# -*- coding: utf-8 -*-

from concurrent.futures import ProcessPoolExecutor

from .base_executor import BaseExecutor


class SequentialExecutor(BaseExecutor):
    def __init__(self):
        self.start()

    def start(self):
        self.pool = ProcessPoolExecutor(1)

    def execute_async(self, task, *args, **kwargs):
        self.pool.submit(task, *args, **kwargs)

    def stop(self):
        self.pool.shutdown(wait=True)
