# -*- coding: utf-8 -*-

import os
import re
import glob
import json
import datetime as dt

import pandas as pd
from werkzeug import secure_filename
from flask import (Blueprint, jsonify, redirect, render_template, request,
                   send_from_directory, url_for)

from .. import configuration as conf
from ..executors import DEFAULT_EXECUTOR
from ..models import File, Rule, Job
from ..settings import Session
from ..tasks import split, extract
from ..utils.file import mkdirs, allowed_filename
from ..utils.metadata import generate_uuid, random_string


views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def index():
    return redirect(url_for('views.files'))


@views.route('/files', methods=['GET', 'POST'])
def files():
    if request.method == 'GET':
        files_response = []
        session = Session()
        for file in session.query(File).order_by(File.uploaded_at.desc()).all():
            job = session.query(Job).filter(Job.file_id == file.file_id).order_by(Job.started_at.desc()).first()
            files_response.append({
                'file_id': file.file_id,
                'job_id': job.job_id,
                'uploaded_at': file.uploaded_at.strftime('%Y-%m-%dT%H:%M:%S'),
                'filename': file.filename
            })
        session.close()
        return render_template('files.html', files_response=files_response)
    file = request.files['file-0']
    if file and allowed_filename(file.filename):
        file_id = generate_uuid()
        uploaded_at = dt.datetime.now()
        page_number = request.form['page_number']
        filename = secure_filename(file.filename)
        filepath = os.path.join(conf.PDFS_FOLDER, file_id)
        mkdirs(filepath)
        filepath = os.path.join(filepath, filename)
        file.save(filepath)

        session = Session()
        f = File(
            file_id=file_id,
            uploaded_at=uploaded_at,
            page_number=page_number,
            filename=filename,
            filepath=filepath
        )
        session.add(f)
        session.commit()
        session.close()
        DEFAULT_EXECUTOR.execute_async(split, file_id)
    return jsonify(file_id=file_id)


@views.route('/workspaces/<string:file_id>', methods=['GET'])
def workspaces(file_id):
    session = Session()
    file = session.query(File).filter(File.file_id == file_id).first()
    session.close()
    imagepath, file_dimensions, image_dimensions = [None] * 3
    if file.has_image:
        imagepath = file.imagepath.replace(
            os.path.join(conf.PROJECT_ROOT, 'www'), '')
        file_dimensions = json.loads(file.file_dimensions)
        image_dimensions = json.loads(file.image_dimensions)
    return render_template('workspace.html', imagepath=imagepath,
        file_dimensions=file_dimensions, image_dimensions=image_dimensions)


@views.route('/rules', methods=['GET', 'POST'], defaults={'rule_id': None})
@views.route('/rules/<string:rule_id>', methods=['GET'])
def rules(rule_id):
    if request.method == 'GET':
        if rule_id is not None:
            return render_template('rule.html')
        return render_template('rules.html')


@views.route('/jobs', methods=['GET', 'POST'], defaults={'job_id': None})
@views.route('/jobs/<string:job_id>', methods=['GET'])
def jobs(job_id):
    if request.method == 'GET':
        if job_id is not None:
            session = Session()
            job = session.query(Job).filter(Job.job_id == job_id).first()
            session.close()

            data = []
            render_files = json.loads(job.render_files)
            regex = 'page-(\d)+-table-(\d)+'
            for k in sorted(render_files,
                    key=lambda x: (int(re.split(regex, x)[1]), int(re.split(regex, x)[2]))):
                df = pd.read_json(render_files[k])
                columns = df.columns.values
                records = df.to_dict('records')
                data.append({
                    'title': k,
                    'columns': columns,
                    'records': records
                })
            return render_template('job.html', is_finished=job.is_finished,
                started_at=job.started_at, finished_at=job.finished_at,
                datapath=job.datapath, data=data)
        return render_template('jobs.html')
    file_id = request.form['file_id']

    session = Session()
    file = session.query(File).filter(File.file_id == file_id).first()
    session.close()

    page_numbers = request.form['page_numbers']
    if page_numbers == '1':
        page_numbers = file.page_number

    rule_id = generate_uuid()
    rule_name = random_string(10)
    rule_options = request.form['rule_options']

    job_id = generate_uuid()
    started_at = dt.datetime.now()

    session = Session()
    r = Rule(
        rule_id=rule_id,
        rule_name=rule_name,
        rule_options=rule_options
    )
    session.add(r)
    j = Job(
        job_id=job_id,
        page_numbers=page_numbers,
        started_at=started_at,
        file_id=file_id,
        rule_id=rule_id
    )
    session.add(j)
    session.commit()
    session.close()
    DEFAULT_EXECUTOR.execute_async(extract, job_id)
    return jsonify(job_id=job_id)


@views.route('/download', methods=['POST'])
def download():
    job_id = request.form['job_id']
    f = request.form['format']

    session = Session()
    job = session.query(Job).filter(Job.job_id == job_id).first()
    session.close()

    datapath = os.path.join(job.datapath, f.lower())
    zipfile = glob.glob(os.path.join(datapath, '*.zip'))[0]

    directory = os.path.join(os.getcwd(), datapath)
    filename = os.path.basename(zipfile)
    return send_from_directory(
        directory=directory, filename=filename, as_attachment=True)
