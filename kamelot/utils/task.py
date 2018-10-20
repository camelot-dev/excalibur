import os

import cv2
from PyPDF2 import PdfFileReader, PdfFileWriter
from camelot.utils import get_page_layout, get_text_objects, get_rotation


def save_page(filepath, page_number):
    infile = PdfFileReader(open(filepath, 'rb'), strict=False)
    page = infile.getPage(page_number - 1)
    outfile = PdfFileWriter()
    outfile.addPage(page)
    outpath = os.path.join(os.path.dirname(filepath), 'page-{}.pdf'.format(page_number))
    with open(outpath, 'wb') as f:
        outfile.write(f)
    froot, fext = os.path.splitext(outpath)
    layout, __ = get_page_layout(outpath)
    # fix rotated PDF
    lttextlh = get_text_objects(layout, ltype="lh")
    lttextlv = get_text_objects(layout, ltype="lv")
    ltchar = get_text_objects(layout, ltype="char")
    rotation = get_rotation(lttextlh, lttextlv, ltchar)
    if rotation != '':
        outpath_new = ''.join([froot.replace('page', 'p'), '_rotated', fext])
        os.rename(outpath, outpath_new)
        infile = PdfFileReader(open(outpath_new, 'rb'), strict=False)
        if infile.isEncrypted:
            infile.decrypt('')
        outfile = PdfFileWriter()
        p = infile.getPage(0)
        if rotation == 'anticlockwise':
            p.rotateClockwise(90)
        elif rotation == 'clockwise':
            p.rotateCounterClockwise(90)
        outfile.addPage(p)
        with open(outpath, 'wb') as f:
            outfile.write(f)


def get_file_dimensions(filepath):
    layout, dimensions = get_page_layout(filepath)
    return list(dimensions)


def get_image_dimensions(imagepath):
    image = cv2.imread(imagepath)
    return [image.shape[1], image.shape[0]]
