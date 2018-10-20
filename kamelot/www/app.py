from flask import Flask, Blueprint
from werkzeug.utils import find_modules, import_string

from .. import configuration as conf
from .views import views


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(conf)
    app.register_blueprint(views)
    return app
