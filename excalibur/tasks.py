# -*- coding: utf-8 -*-

import os
import glob
import json
import logging
import subprocess
import datetime as dt

import camelot

from . import configuration as conf
from .models import File, Rule, Job
from .settings import Session
from .utils.file import mkdirs
from .utils.task import (save_page, get_page_layout, get_file_dimensions,
                         get_image_dimensions)


def split(file_id):
    try:
        def get_executable():
            import platform
            from distutils.spawn import find_executable

            class GhostscriptNotFound(Exception): pass

            gs = None
            system = platform.system().lower()
            try:
                if system == 'windows':
                    if find_executable('gswin32c.exe'):
                        gs = 'gswin32c.exe'
                    elif find_executable('gswin64c.exe'):
                        gs = 'gswin64c.exe'
                    else:
                        raise ValueError
                else:
                    if find_executable('gs'):
                        gs = 'gs'
                    elif find_executable('gsc'):
                        gs = 'gsc'
                    else:
                        raise ValueError
                if 'ghostscript' not in subprocess.check_output(
                        [gs, '-version']).decode('utf-8').lower():
                    raise ValueError
            except ValueError:
                raise GhostscriptNotFound(
                    'Please make sure that Ghostscript is installed'
                    ' and available on the PATH environment variable')

            return gs

        session = Session()
        file = session.query(File).filter(File.file_id == file_id).first()
        save_page(file.filepath, file.page_number)

        filename = 'page-{}.pdf'.format(file.page_number)
        filepath = os.path.join(conf.PDFS_FOLDER, file_id, filename)
        imagename = ''.join([filename.replace('.pdf', ''), '.png'])
        imagepath = os.path.join(conf.PDFS_FOLDER, file_id, imagename)

        gs_call = [
            '-q',
            '-sDEVICE=png16m',
            '-o',
            imagepath,
            '-r600',
            filepath
        ]
        gs = get_executable()
        gs_call.insert(0, gs)
        process = subprocess.Popen(gs_call)
        out = process.communicate()[0]
        ret = process.wait()

        file.has_image = True
        file.imagename = imagename
        file.imagepath = imagepath

        file_dimensions = get_file_dimensions(filepath)
        image_dimensions = get_image_dimensions(imagepath)
        pdf_width_scaler = image_dimensions[0] / float(file_dimensions[0])
        pdf_height_scaler = image_dimensions[1] / float(file_dimensions[1])

        file.file_dimensions = json.dumps(file_dimensions)
        file.image_dimensions = json.dumps(image_dimensions)

        lattice_areas, stream_areas = [None] * 2
        # lattice
        tables = camelot.read_pdf(filepath, flavor='lattice')
        if len(tables):
            lattice_areas = []
            for table in tables:
                x1, y1, x2, y2 = tables[0]._bbox
                lattice_areas.append((x1, y2, x2, y1))
        # stream
        tables = camelot.read_pdf(filepath, flavor='stream')
        if len(tables):
            stream_areas = []
            for table in tables:
                x1, y1, x2, y2 = tables[0]._bbox
                stream_areas.append((x1, y2, x2, y1))

        detected_areas = {
            'lattice': lattice_areas,
            'stream': stream_areas
        }
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
        flavor = rule_options.pop('flavor')
        tables = camelot.read_pdf(file.filepath, pages=job.page_numbers, flavor=flavor.lower(), **rule_options)

        froot, fext = os.path.splitext(file.filename)
        datapath = os.path.dirname(file.filepath)
        for f in ['csv', 'excel', 'json', 'html']:
            f_datapath = os.path.join(datapath, f)
            mkdirs(f_datapath)
            ext = f if f != 'excel' else 'xlsx'
            f_datapath = os.path.join(f_datapath, '{}.{}'.format(froot, ext))
            tables.export(f_datapath, f=f, compress=True)

        # for render
        jsonpath = os.path.join(datapath, 'json')
        jsonpath = os.path.join(jsonpath, '{}.json'.format(froot))
        tables.export(jsonpath, f='json')
        render_files = {os.path.splitext(os.path.basename(f))[0]: f
            for f in glob.glob(os.path.join(datapath, 'json/*.json'))}

        job.datapath = datapath
        job.render_files = json.dumps(render_files)
        job.is_finished = True
        job.finished_at = dt.datetime.now()

        session.commit()
        session.close()
    except Exception as e:
        logging.exception(e)
