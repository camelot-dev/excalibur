# -*- coding: utf-8 -*-

import os
import json
import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
ID_LEN = 100
STR_LEN = 500


class File(Base):
    __tablename__ = "files"

    file_id = Column(String(ID_LEN), primary_key=True)
    uploaded_at = Column(DateTime)
    page_number = Column(Integer)
    filename = Column(String(STR_LEN))
    filepath = Column(String(STR_LEN))
    has_image = Column(Boolean, default=False)
    imagename = Column(String(STR_LEN))
    imagepath = Column(String(STR_LEN))
    file_dimensions = Column(Text)
    image_dimensions = Column(Text)


class Rule(Base):
    __tablename__ = "rules"

    rule_id = Column(String(ID_LEN), primary_key=True)
    rule_name = Column(String(STR_LEN), primary_key=True)
    rule_options = Column(Text)


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(String(ID_LEN), primary_key=True)
    page_numbers = Column(Text)
    datapath = Column(String(STR_LEN), default=None)
    render_files = Column(Text, default=json.dumps([]))
    is_finished = Column(Boolean, default=False)
    started_at = Column(DateTime)
    finished_at = Column(DateTime, default=dt.datetime.now())
    file_id = Column(String(ID_LEN), ForeignKey('files.file_id'))
    rule_id = Column(String(ID_LEN), ForeignKey('rules.rule_id'))
