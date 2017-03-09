#!/usr/bin/env python
#coding:utf8

import os
import hashlib, time
from app import app
from . import editor
from flask import request, redirect, url_for, send_from_directory
from werkzeug import secure_filename


# 服务端创建一个路由，用来分别匹配客户端传回来的请求，请求信息（一般在js代码段里）里面包含URL
UPLOAD_FOLDER = app.static_folder + '\\avatar'  # 通过访问app里的static_folder变量设置保存文件夹
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# upload、post上传  get获取数据
@editor.route('/upload/avatar', methods=['GET', 'POST'])
def upload_file(projectId):
    if request.method == 'POST':
        file = request.files['file']    # 请求取出file数据，赋值给变量file
        if file and allowed_file(file.filename):    # 判断file后缀是否符合标准
            # filename = secure_filename(file.filename)   # 获取一个安全的文件名 不支持中文
            filename = hashlib.md5(str(time.time())).hexdigest() + '.jpg'   # 为了安全使用哈希函数生成一个随机的文件名，而不是用原来的文件名也能防止重名
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # 保存文件，指明绝对路径地址
            avatar_url = url_for('static', filename='%s/%s' % ('avatar', filename))     # 获取文件的相对路径static-avatar里面
            return avatar_url
    return 'Error'


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS     # 分离出图片名字.后面的部分，进行检验