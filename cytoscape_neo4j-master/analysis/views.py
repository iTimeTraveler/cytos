#!/usr/bin/env python
#coding:utf8

from . import analysis
from models import NodeUtils, LinkUtils, graph
from flask import render_template, jsonify


@analysis.route('/demo_force',methods=['GET','POST'])
def demo_force():
    return render_template('analysis_pages/demo_force.html')

@analysis.route('/demo_image',methods=['GET','POST'])
def demo_image():
    return render_template('analysis_pages/demo_image.html')


# 提供一个动态路由地址，供前端网页调用
@analysis.route('/poeplelist', methods=['GET', 'POST'])
def get_graph():
    global count
    count = 0
    graph.run('MATCH (n) RETURN n,ID(n) as id').data()
    nodes = map(wrapNodes, graph.run('MATCH (n) RETURN n,ID(n) as id').data())  # 从数据库里取出所有节点，交给buildNodes函数加工处理
    # edges = map(MyLink.wrapEdges, graph.run('MATCH ()-[r]->() RETURN r,ID(r) as id').data())  # 从数据库里取出所有关系，交给buildEdges加工处理

    return render_template('analysis_pages/peoplelist.html', nodes = nodes)




# 对数据库里取出来的节点进行包装（这里是规范一下数据的格式）
def wrapNodes(nodeRecord):
    global count
    data = {"id": nodeRecord['id'], "temp_index": count, "label": next(iter(nodeRecord['n'].labels()))}  # 对每一个节点都构造包装成一个这样的格式
    data.update(nodeRecord['n'].properties)
    count += 1
    return data
