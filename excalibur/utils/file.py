import os

from .. import configuration as conf


def mkdirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in conf.ALLOWED_EXTENSIONS
