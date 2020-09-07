# https://github.com/apache/incubator-airflow/blob/master/airflow/utils/module_loading.py
# https://github.com/apache/incubator-airflow/blob/master/LICENSE
from importlib import import_module


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError:
        raise ImportError(f"{dotted_path} doesn't look like a module path")

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError(
            'Module "{}" does not define a "{}" attribute/class'.format(
                module_path, class_name
            )
        )
