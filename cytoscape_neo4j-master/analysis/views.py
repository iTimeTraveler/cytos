#!/usr/bin/env python
#coding:utf8


from . import analysis
from analysis.analyse import *
from flask import render_template, jsonify
from models import graph, NodeUtils, LinkUtils


@analysis.route('/demo_force',methods=['GET','POST'])
def demo_force():
    return render_template('analysis_pages/demo_force.html', navId = "demoforce")

@analysis.route('/demo_image',methods=['GET','POST'])
def demo_image():
    return render_template('analysis_pages/demo_image.html', navId = "demoimage")


@analysis.route('/degree_distribute',methods=['GET','POST'])
def degree():
    matrix = degree_distribution()
    cdd = cumulative_degree_distribution()
    dl = degree_of_people()
    nd = shortest_path()

    global count
    count = 0
    nodes = map(NodeUtils.wrapNodes, graph.run('MATCH (n) RETURN n,ID(n) as id').data())  # 从数据库里取出所有节点，交给buildNodes函数加工处理
    edges = map(LinkUtils.wrapEdges, graph.run('MATCH ()-[r]->() RETURN r,ID(r) as id').data())  # 从数据库里取出所有关系，交给buildEdges加工处理

    return render_template('analysis_pages/degree_distribute.html', navId = "degreedistribute",
                           matrix = matrix, cumulative_degree = cdd, degreedict = dl, networkdiameter = nd, nodes = nodes, links = edges)


# 提供一个动态路由地址，供前端网页调用
@analysis.route('/peoplelist', methods=['GET', 'POST'])
def getGraph():
    global count
    count = 0
    nodes = map(NodeUtils.wrapNodes, graph.run('MATCH (n) RETURN n,ID(n) as id').data())  # 从数据库里取出所有节点，交给buildNodes函数加工处理
    # edges = map(LinkUtils.wrapEdges, graph.run('MATCH ()-[r]->() RETURN r,ID(r) as id').data())  # 从数据库里取出所有关系，交给buildEdges加工处理

    return render_template('analysis_pages/peoplelist.html', nodes = nodes, navId = "peoplelist")
