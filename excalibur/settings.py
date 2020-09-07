import os
import atexit

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool

from . import configuration as conf

EXCALIBUR_HOME = None
SQL_ALCHEMY_CONN = None

engine = None
Session = None


def configure_vars():
    global EXCALIBUR_HOME
    global SQL_ALCHEMY_CONN
    EXCALIBUR_HOME = os.path.expanduser(conf.get("core", "EXCALIBUR_HOME"))
    SQL_ALCHEMY_CONN = conf.get("core", "SQL_ALCHEMY_CONN")


def configure_orm():
    global engine
    global Session

    engine_args = {"poolclass": NullPool}
    engine = create_engine(SQL_ALCHEMY_CONN, **engine_args)
    Session = scoped_session(
        sessionmaker(
            autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
        )
    )


def dispose_orm():
    global engine
    global Session

    if Session is not None:
        Session.remove()
        Session = None
    if engine is not None:
        engine.dispose()
        engine = None


configure_vars()
configure_orm()
atexit.register(dispose_orm)
