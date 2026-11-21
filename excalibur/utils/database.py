from sqlalchemy import inspect
from sqlalchemy import text

from ..settings import engine

# Columns added after the first release. create_all() does not alter
# existing tables, so add them to databases created by older versions.
_ADDED_COLUMNS = {
    "files": {"error": "TEXT"},
    "jobs": {"error": "TEXT"},
}


def _add_missing_columns():
    inspector = inspect(engine)
    with engine.begin() as connection:
        for table, columns in _ADDED_COLUMNS.items():
            existing = {column["name"] for column in inspector.get_columns(table)}
            for name, sql_type in columns.items():
                if name not in existing:
                    connection.execute(
                        text(f"ALTER TABLE {table} ADD COLUMN {name} {sql_type}")  # noqa: S608
                    )


def initialize_database():
    from ..models import Base

    Base.metadata.create_all(engine)
    _add_missing_columns()


def reset_database():
    from ..models import Base

    Base.metadata.drop_all(engine)
    initialize_database()
