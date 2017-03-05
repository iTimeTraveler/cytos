#!/usr/bin/env python
#coding:utf8

import os
from app import app
from . import editor
from flask import request, redirect, url_for, send_from_directory
from werkzeug import secure_filename


UPLOAD_FOLDER = app.static_folder + '\\avatar'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@editor.route('/upload/avatar', methods=['GET', 'POST'])
def upload_file(projectId):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            avatar_url = url_for('static', filename='%s/%s' % ('avatar', filename))
            return avatar_url
    return 'hello'


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS