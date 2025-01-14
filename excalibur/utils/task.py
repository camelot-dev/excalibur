import os

import cv2
from camelot.utils import (
    get_image_char_and_text_objects,
    get_page_layout,
    get_rotation,
)
from pypdf import PdfReader, PdfWriter


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
    inputstream = open(filename, "rb")
    infile = PdfReader(inputstream, strict=False)
    N = len(infile.pages)
    if pages == "1":
        page_numbers.append({"start": 1, "end": 1})
    else:
        if infile.is_encrypted:
            infile.decrypt(password)
        if pages == "all":
            page_numbers.append({"start": 1, "end": len(infile.pages)})
        else:
            for r in pages.split(","):
                if "-" in r:
                    a, b = r.split("-")
                    if b == "end":
                        b = len(infile.pages)
                    page_numbers.append({"start": int(a), "end": int(b)})
                else:
                    page_numbers.append({"start": int(r), "end": int(r)})
    inputstream.close()
    P = []
    for p in page_numbers:
        P.extend(range(p["start"], p["end"] + 1))
    return sorted(set(P)), N


def save_page(filepath, page_number):
    infile = PdfReader(open(filepath, "rb"), strict=False)
    page = infile.pages[page_number - 1]
    outfile = PdfWriter()
    outfile.add_page(page)
    outpath = os.path.join(os.path.dirname(filepath), f"page-{page_number}.pdf")
    with open(outpath, "wb") as f:
        outfile.write(f)
    froot, fext = os.path.splitext(outpath)
    layout, __ = get_page_layout(outpath)
    # fix rotated PDF
    images, chars, horizontal_text, vertical_text = get_image_char_and_text_objects(
        layout
    )
    rotation = get_rotation(chars, horizontal_text, vertical_text)
    if rotation != "":
        outpath_new = "".join([froot.replace("page", "p"), "_rotated", fext])
        os.rename(outpath, outpath_new)
        infile = PdfReader(open(outpath_new, "rb"), strict=False)
        if infile.is_encrypted:
            infile.decrypt("")
        outfile = PdfWriter()
        p = infile.pages[0]
        if rotation == "anticlockwise":
            p.rotateClockwise(90)
        elif rotation == "clockwise":
            p.rotateCounterClockwise(90)
        outfile.add_page(p)
        with open(outpath, "wb") as f:
            outfile.write(f)


def get_file_dim(filepath):
    layout, dimensions = get_page_layout(filepath)
    return list(dimensions)


def get_image_dim(imagepath):
    image = cv2.imread(imagepath)
    return [image.shape[1], image.shape[0]]
