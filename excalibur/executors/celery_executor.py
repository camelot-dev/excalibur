import traceback
import subprocess
import sys

from celery import Celery

from .. import configuration as conf
from .base_executor import BaseExecutor
from ..utils.module_loading import import_string
from ..config_templates.default_celery import DEFAULT_CELERY_CONFIG

if conf.has_option("celery", "celery_config_options"):
    celery_configuration = import_string(conf.get("celery", "celery_config_options"))
else:
    celery_configuration = DEFAULT_CELERY_CONFIG


app = Celery(
    conf.get("celery", "CELERY_APP_NAME"), config_source=celery_configuration, fixups=[]
)


@app.task
def execute_command(command):
    try:
        subprocess.check_call(command, stderr=subprocess.STDOUT, close_fds=(sys.platform != 'win32'))
    except Exception as e:
        traceback.print_exc(e)


class CeleryExecutor(BaseExecutor):
    def __init__(self):
        pass

    def start(self):
        pass

    def execute_async(self, command):
        execute_command.apply_async(args=[command])

    def stop(self):
        pass
