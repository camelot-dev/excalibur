import json
import os
import shutil
from io import BytesIO

import pytest
from pypdf import PdfWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from excalibur import configuration as conf
from excalibur.executors import get_default_executor
from excalibur.utils.database import initialize_database
from excalibur.www.app import create_app


@pytest.fixture
def client(monkeypatch):
    initialize_database()
    executor = get_default_executor()

    def execute_async(command):
        from excalibur.cli import _run

        _run(command[-3], command[-1])

    monkeypatch.setattr(executor, "execute_async", execute_async)
    application = create_app(conf)
    application.config["TESTING"] = True
    return application.test_client()


def _table_pdf():
    buffer = BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=letter)
    rows = [
        ["Item", "Qty", "Price"],
        ["Apples", "2", "1.50"],
        ["Pears", "5", "2.00"],
        ["Total", "", "11.50"],
    ]
    table = Table(rows, colWidths=[200, 80, 80])
    table.setStyle(
        TableStyle([("GRID", (0, 0), (-1, -1), 1, colors.black)])
    )
    document.build([table])
    return buffer.getvalue()


def _blank_pdf():
    buffer = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.write(buffer)
    return buffer.getvalue()


def _upload(client, pdf_bytes, filename):
    response = client.post(
        "/files",
        data={"file-0": (BytesIO(pdf_bytes), filename), "pages": "1"},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    return response.get_json()["file_id"]


def _start_job(client, file_id, rule):
    response = client.post(
        "/jobs",
        data={
            "file_id": file_id,
            "rule_id": "",
            "rule_options": json.dumps(rule),
        },
    )
    assert response.status_code == 200
    return response.get_json()["job_id"]


def _remove_upload(file_id):
    shutil.rmtree(os.path.join(conf.PDFS_FOLDER, file_id), ignore_errors=True)


def test_lattice_extracts_ruled_table(client):
    file_id = _upload(client, _table_pdf(), "table.pdf")
    try:
        workspace = client.get(f"/workspaces/{file_id}")
        assert workspace.status_code == 200
        assert b"Workspace - table.pdf" in workspace.data
        assert b"Internal Server Error" not in workspace.data

        job_id = _start_job(
            client,
            file_id,
            {
                "flavor": "Lattice",
                "process_background": False,
                "line_scale": 15,
                "split_text": False,
                "flag_size": False,
                "pages": {"1": {"table_areas": None, "columns": None}},
            },
        )
        job = client.get(f"/jobs/{job_id}")
        assert job.status_code == 200
        assert b"Apples" in job.data
        assert b"Pears" in job.data
        assert b"11.50" in job.data
    finally:
        _remove_upload(file_id)


def test_stream_accepts_legacy_tolerance_names(client):
    file_id = _upload(client, _table_pdf(), "table.pdf")
    try:
        job_id = _start_job(
            client,
            file_id,
            {
                "flavor": "Stream",
                "row_close_tol": 2,
                "col_close_tol": 0,
                "split_text": False,
                "flag_size": False,
                "pages": {"1": {"table_areas": None, "columns": None}},
            },
        )
        job = client.get(f"/jobs/{job_id}")
        assert job.status_code == 200
        assert b"Apples" in job.data
        assert b"Please wait while the tables are extracted." not in job.data
    finally:
        _remove_upload(file_id)


def test_lattice_on_blank_pdf_finishes_with_no_tables(client):
    file_id = _upload(client, _blank_pdf(), "blank.pdf")
    try:
        job_id = _start_job(
            client,
            file_id,
            {
                "flavor": "Lattice",
                "process_background": False,
                "line_scale": 15,
                "split_text": False,
                "flag_size": False,
                "pages": {"1": {"table_areas": None, "columns": None}},
            },
        )
        job = client.get(f"/jobs/{job_id}")
        body = job.data
        assert job.status_code == 200
        assert b"No tables were found" in body
        assert b"Please wait while the tables are extracted." not in body
    finally:
        _remove_upload(file_id)
