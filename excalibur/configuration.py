# -*- coding: utf-8 -*-

import os


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# for excalibur
PDFS_FOLDER = os.path.join(PROJECT_ROOT, 'www/static/uploads')
ALLOWED_EXTENSIONS = ['pdf']
EXECUTOR = 'SequentialExecutor'

# for flask
SECRET_KEY = 'secret_key'

# for celery
BROKER_URL = 'amqp://guest@localhost:5672//'
CELERY_CREATE_MISSING_QUEUES = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_ACKS_LATE = True


# for sqlalchemy
DB = 'excalibur.db'
SQL_ALCHEMY_CONN = 'sqlite:///{}/{}'.format(PROJECT_ROOT, DB)
