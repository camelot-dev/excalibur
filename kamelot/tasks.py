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
from .utils.task import save_page, get_page_layout, get_file_dimensions, get_image_dimensions


def split(file_id):
    try:
        def get_platform():
            import platform

            info = {
                'system': platform.system().lower(),
                'machine': platform.machine().lower()
            }
            return info

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
        info = get_platform()
        if info['system'] == 'windows':
            bit = info['machine'][-2:]
            gs_call.insert(0, 'gswin{}c.exe'.format(bit))
        else:
            if 'ghostscript' in subprocess.check_output(['gs', '-version']).decode('utf-8').lower():
                gs_call.insert(0, 'gs')
            else:
                gs_call.insert(0, "gsc")
        process = subprocess.Popen(gs_call)
        out = process.communicate()[0]
        ret = process.wait()

        file.has_image = True
        file.imagename = imagename
        file.imagepath = imagepath
        file.file_dimensions = json.dumps(get_file_dimensions(filepath))
        file.image_dimensions = json.dumps(get_image_dimensions(imagepath))

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
