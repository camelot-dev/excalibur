from pypdf import PdfWriter

from excalibur.utils.file import allowed_filename
from excalibur.utils.task import get_file_dim, get_pages


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
