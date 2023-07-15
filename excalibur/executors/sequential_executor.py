import traceback
import subprocess
from concurrent.futures import ProcessPoolExecutor
import sys

from .base_executor import BaseExecutor


def execute_command(command):
    try:
        subprocess.check_call(command, stderr=subprocess.STDOUT, close_fds=(sys.platform != 'win32'))
    except FileNotFoundError:
        # TODO: PyInstaller does not package console_scripts
        # https://github.com/pyinstaller/pyinstaller/issues/305
        from ..cli import _run

        task_name = command[-3]
        task_id = command[-1]
        _run(task_name, task_id)
    except Exception as e:
        traceback.print_exc(e)


class SequentialExecutor(BaseExecutor):
    def __init__(self):
        self.start()

    def start(self):
        self.pool = ProcessPoolExecutor(1)

    def execute_async(self, command):
        self.pool.submit(execute_command, command)

    def stop(self):
        self.pool.shutdown(wait=True)
