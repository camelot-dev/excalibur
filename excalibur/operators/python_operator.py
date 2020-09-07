from .base_operator import BaseOperator


class PythonOperator(BaseOperator):
    def __init__(self, python_callable, op_args=None, op_kwargs=None):
        self.python_callable = python_callable
        self.op_args = op_args or []
        self.op_kwargs = op_kwargs or {}

    def execute(self):
        self.execute_callable()

    def execute_callable(self):
        self.python_callable(*self.op_args, **self.op_kwargs)
