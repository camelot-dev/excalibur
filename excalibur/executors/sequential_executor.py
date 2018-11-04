# -*- coding: utf-8 -*-

import traceback
import subprocess
from concurrent.futures import ProcessPoolExecutor

from .base_executor import BaseExecutor


def execute_command(command):
    try:
        subprocess.check_call(command, stderr=subprocess.STDOUT, close_fds=True)
    except Exception as e:
        traceback.print_exc()


class SequentialExecutor(BaseExecutor):
    def __init__(self):
        self.start()

    def start(self):
        self.pool = ProcessPoolExecutor(1)

    def execute_async(self, command):
        self.pool.submit(execute_command, command)

    def stop(self):
        self.pool.shutdown(wait=True)
