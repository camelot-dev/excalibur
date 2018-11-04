# -*- coding: utf-8 -*-

from .base_executor import BaseExecutor


class CeleryExecutor(BaseExecutor):
    def __init__(self):
        pass

    def start(self):
        pass

    def execute_async(self, task, *args, **kwargs):
        pass

    def stop(self):
        pass
