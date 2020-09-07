import json
import datetime as dt
from typing import Any  # noqa

from sqlalchemy import (
    Text,
    Column,
    String,
    Boolean,
    Integer,
    DateTime,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # type: Any
ID_LEN = 100
STR_LEN = 500


class File(Base):
    __tablename__ = "files"

    file_id = Column(String(ID_LEN), primary_key=True)
    uploaded_at = Column(DateTime)
    pages = Column(String(STR_LEN))
    total_pages = Column(Integer)
    extract_pages = Column(Text)
    filename = Column(String(STR_LEN))
    filepath = Column(String(STR_LEN))
    has_image = Column(Boolean, default=False)
    filenames = Column(Text)
    filepaths = Column(Text)
    imagenames = Column(Text)
    imagepaths = Column(Text)
    filedims = Column(Text)
    imagedims = Column(Text)
    detected_areas = Column(Text)


class Rule(Base):
    __tablename__ = "rules"

    rule_id = Column(String(ID_LEN), primary_key=True)
    created_at = Column(DateTime)
    rule_name = Column(String(STR_LEN))
    rule_options = Column(Text)


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(String(ID_LEN), primary_key=True)
    datapath = Column(String(STR_LEN), default=None)
    render_files = Column(Text, default=json.dumps([]))
    is_finished = Column(Boolean, default=False)
    started_at = Column(DateTime)
    finished_at = Column(DateTime, default=dt.datetime.now())
    file_id = Column(String(ID_LEN), ForeignKey("files.file_id"))
    rule_id = Column(String(ID_LEN), ForeignKey("rules.rule_id"))
