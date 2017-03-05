#!/usr/bin/env python
#coding:utf8


from . import analysis
from analysis.analyse import AnalyseUtils
from flask import render_template
from models import graph, NodeUtils, LinkUtils


@analysis.route('/demo_force',methods=['GET','POST'])
def demo_force(projectId):
    return render_template('analysis_pages/demo_force.html', navId = "demoforce", projectId=projectId)

@analysis.route('/demo_image',methods=['GET','POST'])
def demo_image(projectId):
    return render_template('analysis_pages/demo_image.html', navId = "demoimage", projectId=projectId)


@analysis.route('/degree_distribute',methods=['GET','POST'])
def degree(projectId):
    analyse_utils = AnalyseUtils(projectId)
    matrix = analyse_utils.degree_distribution()
    cdd = analyse_utils.cumulative_degree_distribution()
    dl = analyse_utils.degree_of_people()
    nd = analyse_utils.shortest_path()

    nodes = NodeUtils.getAllNodes(projectId)
    edges = LinkUtils.getAllLinks(projectId)

    return render_template('analysis_pages/degree_distribute.html', navId = "degreedistribute", projectId=projectId,
                           matrix = matrix, cumulative_degree = cdd, degreedict = dl, networkdiameter = nd, nodes = nodes, links = edges)


# 提供一个动态路由地址，供前端网页调用
@analysis.route('/peoplelist', methods=['GET', 'POST'])
def getGraph(projectId):
    nodes = NodeUtils.getAllNodes(projectId)

    return render_template('analysis_pages/peoplelist.html', nodes = nodes, navId = "peoplelist", projectId=projectId)
