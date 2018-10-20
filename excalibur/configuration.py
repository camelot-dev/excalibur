# -*- coding: utf-8 -*-

import os


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# for excalibur
PDFS_FOLDER = os.path.join(PROJECT_ROOT, 'www/static/uploads')
ALLOWED_EXTENSIONS = ['pdf']
EXECUTOR = 'SequentialExecutor'

# for flask
SECRET_KEY = 'secret_key'

# for sqlalchemy
SQL_ALCHEMY_CONN = 'sqlite:///{}/{}'.format(PROJECT_ROOT, 'excalibur.db')
