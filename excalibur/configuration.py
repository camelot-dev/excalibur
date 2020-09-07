import os

import six
from backports.configparser import ConfigParser


def _read_default_config_file(file_name):
    """
    https://github.com/apache/incubator-airflow/blob/master/airflow/configuration.py
    https://github.com/apache/incubator-airflow/blob/master/LICENSE
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "config_templates")
    file_path = os.path.join(templates_dir, file_name)
    with open(file_path, encoding="utf-8") as f:
        return f.read()


def expand_env_var(env_var):
    """
    https://github.com/apache/incubator-airflow/blob/master/airflow/configuration.py
    https://github.com/apache/incubator-airflow/blob/master/LICENSE

    Expands (potentially nested) env vars by repeatedly applying
    `expandvars` and `expanduser` until interpolation stops having
    any effect.
    """
    if not env_var:
        return env_var
    while True:
        interpolated = os.path.expanduser(os.path.expandvars(str(env_var)))
        if interpolated == env_var:
            return interpolated
        else:
            env_var = interpolated


DEFAULT_CONFIG = _read_default_config_file("default_excalibur.cfg")


class ExcaliburConfigParser(ConfigParser):
    def __init__(self, default_config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.excalibur_defaults = ConfigParser(*args, **kwargs)
        if default_config is not None:
            self.excalibur_defaults.read_string(default_config)

        self.is_validated = False

    def _validate(self):
        if self.get(
            "core", "executor"
        ) != "SequentialExecutor" and "sqlite" in self.get("core", "sql_alchemy_conn"):
            raise ValueError(
                "Cannot use sqlite with the {}".format(self.get("core", "executor"))
            )

        self.is_validated = True

    def get(self, section, key, **kwargs):
        section = str(section).lower()
        key = str(key).lower()

        if super().has_option(section, key):
            return expand_env_var(super().get(section, key, **kwargs))

        if self.excalibur_defaults.has_option(section, key):
            return expand_env_var(self.excalibur_defaults.get(section, key, **kwargs))

        else:
            raise ValueError(
                "section/key [{section}/{key}] not found in"
                " config".format(**locals())
            )

    def read(self, filename):
        super().read(filename)
        self._validate()


def mkdirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)


if "EXCALIBUR_HOME" not in os.environ:
    EXCALIBUR_HOME = expand_env_var("~/excalibur")
else:
    EXCALIBUR_HOME = expand_env_var(os.environ["EXCALIBUR_HOME"])

mkdirs(EXCALIBUR_HOME)

if "EXCALIBUR_CONFIG" not in os.environ:
    EXCALIBUR_CONFIG = EXCALIBUR_HOME + "/excalibur.cfg"
else:
    EXCALIBUR_CONFIG = expand_env_var(os.environ["EXCALIBUR_CONFIG"])


def parameterized_config(template):
    """
    https://github.com/apache/incubator-airflow/blob/master/airflow/configuration.py
    https://github.com/apache/incubator-airflow/blob/master/LICENSE

    Generates a configuration from the provided template + variables defined in
    current scope
    :param template: a config content templated with {{variables}}
    """
    all_vars = {k: v for d in [globals(), locals()] for k, v in d.items()}
    return template.format(**all_vars)


if not os.path.isfile(EXCALIBUR_CONFIG):
    print(f"Creating new Excalibur configuration file in: {EXCALIBUR_CONFIG}")
    with open(EXCALIBUR_CONFIG, "w") as f:
        cfg = parameterized_config(DEFAULT_CONFIG)
        if six.PY2:
            cfg = cfg.encode("utf8")
        f.write(cfg)


conf = ExcaliburConfigParser(default_config=parameterized_config(DEFAULT_CONFIG))

conf.read(EXCALIBUR_CONFIG)

# for Flask
ALLOWED_EXTENSIONS = ["pdf", "json"]
SECRET_KEY = conf.get("webserver", "SECRET_KEY")
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PDFS_FOLDER = os.path.join(PROJECT_ROOT, "www/static/uploads")
USING_SQLITE = (
    True if conf.get("core", "SQL_ALCHEMY_CONN").startswith("sqlite") else False
)

get = conf.get
has_option = conf.has_option
