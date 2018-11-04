# -*- coding: utf-8 -*-

import logging
import traceback
import subprocess

from celery import Celery

from .base_executor import BaseExecutor
from .. import configuration as conf


app = Celery()
app.config_from_object('excalibur.configuration')


@app.task
def execute_command(command):
    try:
        subprocess.check_call(command, stderr=subprocess.STDOUT, close_fds=True)
    except Exception as e:
        traceback.print_exc()


class CeleryExecutor(BaseExecutor):
    def __init__(self):
        pass

    def start(self):
        pass

    def execute_async(self, command):
        execute_command.apply_async(args=[command])

    def stop(self):
        pass
