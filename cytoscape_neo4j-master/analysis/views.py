#!/usr/bin/env python
#coding:utf8

from . import analysis
from analyse import *
from models import NodeUtils, LinkUtils, graph
from flask import render_template, jsonify


@analysis.route('/demo_force',methods=['GET','POST'])
def demo_force():
    calculate_communities()
    return render_template('analysis_pages/demo_force.html', navId = "demoforce")

@analysis.route('/demo_image',methods=['GET','POST'])
def demo_image():
    return render_template('analysis_pages/demo_image.html', navId = "demoimage")


@analysis.route('/degree_distribute',methods=['GET','POST'])
def degree():
    matrix = degree_distribution()
    dl = degree_of_people()
    return render_template('analysis_pages/degree_distribute.html', navId = "degreedistribute", matrix = matrix, degreedict = dl)


# 提供一个动态路由地址，供前端网页调用
@analysis.route('/peoplelist', methods=['GET', 'POST'])
def get_graph():
    global count
    count = 0
    graph.run('MATCH (n) RETURN n,ID(n) as id').data()
    nodes = map(wrapNodes, graph.run('MATCH (n) RETURN n,ID(n) as id').data())  # 从数据库里取出所有节点，交给buildNodes函数加工处理
    # edges = map(MyLink.wrapEdges, graph.run('MATCH ()-[r]->() RETURN r,ID(r) as id').data())  # 从数据库里取出所有关系，交给buildEdges加工处理

    return render_template('analysis_pages/peoplelist.html', nodes = nodes, navId = "peoplelist")




# 对数据库里取出来的节点进行包装（这里是规范一下数据的格式）
def wrapNodes(nodeRecord):
    global count
    data = {"id": nodeRecord['id'], "temp_index": count, "label": next(iter(nodeRecord['n'].labels()))}  # 对每一个节点都构造包装成一个这样的格式
    data.update(nodeRecord['n'].properties)
    count += 1
    return data
