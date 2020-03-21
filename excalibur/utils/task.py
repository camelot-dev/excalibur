import os

import cv2
from PyPDF2 import PdfFileReader, PdfFileWriter
from camelot.utils import get_page_layout, get_text_objects, get_rotation


def get_pages(filename, pages):
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
    infile = PdfFileReader(inputstream, strict=False)
    N = infile.getNumPages()
    if pages == "1":
        page_numbers.append({"start": 1, "end": 1})
    else:
        if infile.isEncrypted:
            infile.decrypt(self.password)
        if pages == "all":
            page_numbers.append({"start": 1, "end": infile.getNumPages()})
        else:
            for r in pages.split(","):
                if "-" in r:
                    a, b = r.split("-")
                    if b == "end":
                        b = infile.getNumPages()
                    page_numbers.append({"start": int(a), "end": int(b)})
                else:
                    page_numbers.append({"start": int(r), "end": int(r)})
    inputstream.close()
    P = []
    for p in page_numbers:
        P.extend(range(p["start"], p["end"] + 1))
    return sorted(set(P)), N


def save_page(filepath, page_number):
    infile = PdfFileReader(open(filepath, "rb"), strict=False)
    page = infile.getPage(page_number - 1)
    outfile = PdfFileWriter()
    outfile.addPage(page)
    outpath = os.path.join(os.path.dirname(filepath), "page-{}.pdf".format(page_number))
    with open(outpath, "wb") as f:
        outfile.write(f)
    froot, fext = os.path.splitext(outpath)
    layout, __ = get_page_layout(outpath)
    # fix rotated PDF
    chars = get_text_objects(layout, ltype="char")
    horizontal_text = get_text_objects(layout, ltype="horizontal_text")
    vertical_text = get_text_objects(layout, ltype="vertical_text")
    rotation = get_rotation(chars, horizontal_text, vertical_text)
    if rotation != "":
        outpath_new = "".join([froot.replace("page", "p"), "_rotated", fext])
        os.rename(outpath, outpath_new)
        infile = PdfFileReader(open(outpath_new, "rb"), strict=False)
        if infile.isEncrypted:
            infile.decrypt("")
        outfile = PdfFileWriter()
        p = infile.getPage(0)
        if rotation == "anticlockwise":
            p.rotateClockwise(90)
        elif rotation == "clockwise":
            p.rotateCounterClockwise(90)
        outfile.addPage(p)
        with open(outpath, "wb") as f:
            outfile.write(f)


def get_file_dim(filepath):
    layout, dimensions = get_page_layout(filepath)
    return list(dimensions)


def get_image_dim(imagepath):
    image = cv2.imread(imagepath)
    return [image.shape[1], image.shape[0]]
