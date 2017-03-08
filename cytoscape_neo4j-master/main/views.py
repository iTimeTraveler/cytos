#!/usr/bin/env python
#coding:utf8

from . import main
from flask import render_template, request
from models import GraphUtils, ProjectUtils

graphUtils = GraphUtils()
projectUtils = ProjectUtils()

@main.route('/', methods=['GET','POST'])
def home():
    # 用来创建新影视剧
    if request.method == 'POST':
        if request.values.get('action', "") == 'create':
            prjname = request.values.get('prjname', "")
            if prjname == "":
                return ''
            pid = projectUtils.createOne(prjname)   # 调用创建影视剧项目的函数
            return str(pid)
        elif request.values.get('action', "") == 'delete':
            pid = request.values.get('prj_id', "")
            if pid == "":
                return ''
            projectUtils.deleteOne(pid)  # 调用删除影视剧项目的函数
            return ''
    else:
        all_projects = projectUtils.getAllProjects()
        print(all_projects)
        # 渲染模板 交给index主页面-首页
        return render_template('main/index.html', navId = "main", all_projects=all_projects)