# -*- coding: utf-8 -*-

import atexit

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool

from . import configuration as conf


engine = None
Session = None


def configure_orm():
    global engine
    global Session

    engine_args = {
        'poolclass': NullPool
    }
    engine = create_engine(conf.SQL_ALCHEMY_CONN, **engine_args)
    Session = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=engine, expire_on_commit=False))


def dispose_orm():
    global engine
    global Session

    if Session is not None:
        Session.remove()
        Session = None
    if engine is not None:
        engine.dispose()
        engine = None


configure_orm()
atexit.register(dispose_orm)
