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
            pid = projectUtils.createOne(prjname)
            return str(pid)
        elif request.values.get('action', "") == 'delete':
            pid = request.values.get('prj_id', "")
            if pid == "":
                return ''
            projectUtils.deleteOne(pid)
            return ''
    else:
        all_projects = projectUtils.getAllProjects()
        print(all_projects)
        return render_template('main/index.html', navId = "main", all_projects=all_projects)