from pypdf import PdfWriter

from excalibur.utils.file import allowed_filename
from excalibur.utils.task import get_file_dim
from excalibur.utils.task import get_pages


def test_allowed_filename():
    assert not allowed_filename("foo.bar")
    assert allowed_filename("foo.pdf")


def test_get_pages_and_dimensions(tmp_path):
    pdf = tmp_path / "blank.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    with pdf.open("wb") as handle:
        writer.write(handle)

    pages, total = get_pages(str(pdf), "1")
    assert pages == [1]
    assert total == 1

    width, height = get_file_dim(str(pdf))
    assert width == 612
    assert height == 792


def test_initialize_database_adds_error_column_to_old_tables(tmp_path, monkeypatch):
    from sqlalchemy import create_engine
    from sqlalchemy import inspect
    from sqlalchemy import text

    from excalibur.utils import database

    engine = create_engine(f"sqlite:///{tmp_path / 'old.db'}")
    with engine.begin() as connection:
        connection.execute(
            text("CREATE TABLE files (file_id VARCHAR(100) PRIMARY KEY)")
        )
        connection.execute(text("CREATE TABLE jobs (job_id VARCHAR(100) PRIMARY KEY)"))
    monkeypatch.setattr(database, "engine", engine)

    database.initialize_database()
    database.initialize_database()  # idempotent

    inspector = inspect(engine)
    for table in ("files", "jobs"):
        names = {column["name"] for column in inspector.get_columns(table)}
        assert "error" in names
