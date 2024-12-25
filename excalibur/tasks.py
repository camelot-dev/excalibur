import datetime as dt
import glob
import json
import logging
import os
import subprocess

import camelot
import pandas as pd
from camelot.backends.ghostscript_backend import GhostscriptBackend
from camelot.core import TableList
from camelot.parsers import Lattice, Stream

from . import configuration as conf
from .models import File, Job, Rule
from .settings import Session
from .utils.file import mkdirs
from .utils.task import get_file_dim, get_image_dim, get_pages, save_page


def split(file_id):
    try:
        session = Session()
        file = session.query(File).filter(File.file_id == file_id).first()
        extract_pages, total_pages = get_pages(file.filepath, file.pages)

        (
            filenames,
            filepaths,
            imagenames,
            imagepaths,
            filedims,
            imagedims,
            detected_areas,
        ) = ({} for i in range(7))
        for page in extract_pages:
            # extract into single-page PDF
            save_page(file.filepath, page)

            filename = f"page-{page}.pdf"
            filepath = os.path.join(conf.PDFS_FOLDER, file_id, filename)
            imagename = "".join([filename.replace(".pdf", ""), ".png"])
            imagepath = os.path.join(conf.PDFS_FOLDER, file_id, imagename)

            # convert single-page PDF to PNG
            try:
                backend = GhostscriptBackend()
                backend.convert(filepath, imagepath, 300)
            except OSError:
                gs_command = [
                    "gs",
                    "-q",
                    "-sDEVICE=png16m",
                    f"-o{imagepath}",
                    "-r300",
                    filepath,
                ]
                try:
                    subprocess.run(gs_command, check=True, capture_output=True)
                except subprocess.CalledProcessError as e:
                    logging.error(f"Ghostscript conversion failed: {e.stderr.decode()}")
                    raise

            filenames[page] = filename
            filepaths[page] = filepath
            imagenames[page] = imagename
            imagepaths[page] = imagepath
            filedims[page] = get_file_dim(filepath)
            imagedims[page] = get_image_dim(imagepath)

            lattice_areas, stream_areas = (None for i in range(2))
            # lattice
            tables = camelot.read_pdf(filepath, flavor="lattice")
            if len(tables):
                lattice_areas = []
                for table in tables:
                    x1, y1, x2, y2 = table._bbox
                    lattice_areas.append((x1, y2, x2, y1))
            # stream
            tables = camelot.read_pdf(filepath, flavor="stream")
            if len(tables):
                stream_areas = []
                for table in tables:
                    x1, y1, x2, y2 = table._bbox
                    stream_areas.append((x1, y2, x2, y1))

            detected_areas[page] = {"lattice": lattice_areas, "stream": stream_areas}

        file.extract_pages = json.dumps(extract_pages)
        file.total_pages = total_pages
        file.has_image = True
        file.filenames = json.dumps(filenames)
        file.filepaths = json.dumps(filepaths)
        file.imagenames = json.dumps(imagenames)
        file.imagepaths = json.dumps(imagepaths)
        file.filedims = json.dumps(filedims)
        file.imagedims = json.dumps(imagedims)
        file.detected_areas = json.dumps(detected_areas)

        session.commit()
        session.close()
    except Exception as e:
        logging.exception(e)


def extract(job_id):
    try:
        session = Session()
        job = session.query(Job).filter(Job.job_id == job_id).first()
        rule = session.query(Rule).filter(Rule.rule_id == job.rule_id).first()
        file = session.query(File).filter(File.file_id == job.file_id).first()

        rule_options = json.loads(rule.rule_options)
        flavor = rule_options.pop("flavor")
        pages = rule_options.pop("pages")

        tables = []
        filepaths = json.loads(file.filepaths)
        for p in pages:
            kwargs = pages[p]
            kwargs.update(rule_options)
            kwargs["flavor"] = flavor.lower()
            if flavor.lower() == "lattice":
                kwargs.pop("columns", None)

            t = camelot.read_pdf(filepaths[p], **kwargs, backend="poppler")
            for _t in t:
                _t.page = int(p)
            tables.extend(t)
        tables = TableList(tables)

        froot, fext = os.path.splitext(file.filename)
        datapath = os.path.dirname(file.filepath)
        for f in ["csv", "excel", "json", "html"]:
            f_datapath = os.path.join(datapath, f)
            mkdirs(f_datapath)
            ext = f if f != "excel" else "xlsx"
            f_datapath = os.path.join(f_datapath, f"{froot}.{ext}")

            if f == "excel":
                with pd.ExcelWriter(f_datapath) as writer:
                    for i, table in enumerate(tables):
                        sheet_name = f"Table_{i + 1}"
                        table.df.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                tables.export(f_datapath, f=f, compress=True)

        # for render
        jsonpath = os.path.join(datapath, "json")
        jsonpath = os.path.join(jsonpath, f"{froot}.json")
        tables.export(jsonpath, f="json")
        render_files = {
            os.path.splitext(os.path.basename(f))[0]: f
            for f in glob.glob(os.path.join(datapath, "json/*.json"))
        }

        job.datapath = datapath
        job.render_files = json.dumps(render_files)
        job.is_finished = True
        job.finished_at = dt.datetime.now()

        session.commit()
        session.close()
    except Exception as e:
        logging.exception(e)
