#!/usr/bin/env python
#coding:utf8

from . import editor
from models import MyNode, MyLink, graph
from flask import render_template, request, json, jsonify


@editor.route('/',methods=['GET','POST'])
def getEditor():
    return render_template('editor_pages/demo2.html')


# 修改节点或关系
@editor.route('/post', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('editor_pages/demo2.html')

    if request.method == 'POST':
        if request.values.get('type', "") == 'node':
            nodesStr = request.values.get('node', "")
            actionStr = request.values.get('act', "")
            newNode = json.loads(nodesStr, encoding="utf-8")
            return MyNode.dispacthNode(newNode, actionStr)
        elif request.values.get('type', "") == 'link':
            linksStr = request.values.get('link', "")
            actionStr = request.values.get('act', "")
            newLink = json.loads(linksStr, encoding="utf-8")
            return MyLink.dispacthLink(newLink, actionStr)



# 提供一个动态路由地址，供前端网页调用
@editor.route('/graph', methods=['GET', 'POST'])
def get_graph():
    global count
    count = 0
    nodes = map(wrapNodes, graph.run('MATCH (n) RETURN n,ID(n) as id').data())  # 从数据库里取出所有节点，交给buildNodes函数加工处理
    edges = map(wrapEdges, graph.run('MATCH ()-[r]->() RETURN r,ID(r) as id').data())  # 从数据库里取出所有关系，交给buildEdges加工处理

    return jsonify(elements = {"nodes": nodes, "edges": edges}) #把处理好的数据，整理成json格式，然后返回给客户端



# 对数据库里取出来的节点进行包装（这里是规范一下数据的格式）
def wrapNodes(nodeRecord):
    global count
    data = {"id": nodeRecord['id'], "temp_index": count, "label": next(iter(nodeRecord['n'].labels()))}  # 对每一个节点都构造包装成一个这样的格式
    data.update(nodeRecord['n'].properties)
    count += 1
    return data


# 对数据库里取出来的关系进行包装（这里也是规范一下数据的格式）
def wrapEdges(relationRecord):
    data = {"id": relationRecord['id'],
            "source": relationRecord['r'].start_node()['name'],
            "target": relationRecord['r'].end_node()['name'],
            "relation": str(relationRecord['r'].type())}  # 对每一个关系都构造包装成一个这样的格式， str()是一个方法，把括号里的参数转换为字符串类型
    data.update(relationRecord['r'].properties)
    return data