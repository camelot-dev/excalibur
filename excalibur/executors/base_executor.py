# -*- coding: utf-8 -*-

class BaseExecutor(object):
    def __init__(self):
        pass

    def start(self):
        raise NotImplementedError()

    def execute_async(self, task, *args, **kwargs):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()
