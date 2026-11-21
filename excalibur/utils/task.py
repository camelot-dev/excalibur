import os

import cv2
import playa
from camelot.utils import (
    get_image_char_and_text_objects,
    get_page_layout,
    get_rotation,
)
from pypdf import PdfReader, PdfWriter


def _reader(source):
    """Open a PDF with the lenient parser used by current and older pypdf."""
    return PdfReader(source, strict=False)


def _text_rotation(filepath):
    """Return '', 'clockwise', or 'anticlockwise' for the first page.

    Camelot 2's layout helpers take a playa page, not a filesystem path.
    """
    with playa.open(filepath, space="page") as pdf:
        layout, _dimensions = get_page_layout(pdf.pages[0])
        _images, chars, horizontal_text, vertical_text = (
            get_image_char_and_text_objects(layout)
        )
        return get_rotation(chars, horizontal_text, vertical_text)


def get_pages(filename, pages, password=""):
    """Converts pages string to list of ints.

    Parameters
    ----------
    filename : str
        Path to PDF file.
    pages : str, optional (default: '1')
        Comma-separated page numbers.
        Example: 1,3,4 or 1,4-end.

    Returns
    -------
    N : int
        Total pages.
    P : list
        List of int page numbers.

    """
    page_numbers = []
    infile = _reader(filename)
    if infile.is_encrypted:
        infile.decrypt(password)
    N = len(infile.pages)
    if pages == "1":
        page_numbers.append({"start": 1, "end": 1})
    else:
        if pages == "all":
            page_numbers.append({"start": 1, "end": N})
        else:
            for r in pages.split(","):
                if "-" in r:
                    a, b = r.split("-")
                    if b == "end":
                        b = N
                    page_numbers.append({"start": int(a), "end": int(b)})
                else:
                    page_numbers.append({"start": int(r), "end": int(r)})
    P = []
    for p in page_numbers:
        P.extend(range(p["start"], p["end"] + 1))
    return sorted(set(P)), N


def save_page(filepath, page_number):
    infile = _reader(filepath)
    page = infile.pages[page_number - 1]
    outfile = PdfWriter()
    outfile.add_page(page)
    outpath = os.path.join(os.path.dirname(filepath), f"page-{page_number}.pdf")
    with open(outpath, "wb") as f:
        outfile.write(f)
    froot, fext = os.path.splitext(outpath)
    # fix rotated PDF. pypdf 5+ removed rotateClockwise / rotateCounterClockwise.
    rotation = _text_rotation(outpath)
    if rotation != "":
        outpath_new = "".join([froot.replace("page", "p"), "_rotated", fext])
        os.rename(outpath, outpath_new)
        infile = _reader(outpath_new)
        if infile.is_encrypted:
            infile.decrypt("")
        outfile = PdfWriter()
        p = infile.pages[0]
        if rotation == "anticlockwise":
            p.rotate(90)
        elif rotation == "clockwise":
            p.rotate(-90)
        outfile.add_page(p)
        with open(outpath, "wb") as f:
            outfile.write(f)


def get_file_dim(filepath):
    with playa.open(filepath, space="page") as pdf:
        _layout, dimensions = get_page_layout(pdf.pages[0])
    return [float(dimensions[0]), float(dimensions[1])]


def get_image_dim(imagepath):
    image = cv2.imread(imagepath)
    return [image.shape[1], image.shape[0]]
