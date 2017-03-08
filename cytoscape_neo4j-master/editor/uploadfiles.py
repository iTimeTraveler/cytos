#!/usr/bin/env python
#coding:utf8

import os
from app import app
from . import editor
from flask import request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

# 没懂
UPLOAD_FOLDER = app.static_folder + '\\avatar'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# upload、post上传  get获取数据
@editor.route('/upload/avatar', methods=['GET', 'POST'])
def upload_file(projectId):
    if request.method == 'POST':
        file = request.files['file']    # 请求取出file数据，赋值给变量file
        if file and allowed_file(file.filename):    # 判断file后缀是否符合标准
            filename = secure_filename(file.filename)   # 获取一个安全的文件名 不支持中文
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # 保存文件
            avatar_url = url_for('static', filename='%s/%s' % ('avatar', filename))     # 获取文件的保存路径static-avatar里面
            return avatar_url
    return 'hello'


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS