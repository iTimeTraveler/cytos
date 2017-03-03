#!/usr/bin/env python
#coding:utf8

from . import editor
from models import NodeUtils, LinkUtils, graph
from flask import render_template, request, json, jsonify
import sys

# 防止中文编译不过
reload(sys)
sys.setdefaultencoding("utf-8")

nodeUtils = NodeUtils()
linkUtils = LinkUtils()

@editor.route('/',methods=['GET','POST'])
def getEditor():
    communities = graph.run('MATCH (n) RETURN distinct n.community AS index, count(*) as count ORDER BY n.community ASC').data()
    return render_template('editor_pages/index.html', navId = "editor", communities = communities)


# 修改节点或关系
@editor.route('/modify', methods=['POST'])
def modify():
    if request.method == 'POST':
        if request.values.get('type', "") == 'node':
            nodeStr = request.values.get('node', "")
            actionStr = request.values.get('act', "")
            newNode = json.loads(nodeStr, encoding="utf-8")
            return nodeUtils.dispacthNode(newNode, actionStr)
        elif request.values.get('type', "") == 'link':
            linkStr = request.values.get('link', "")
            actionStr = request.values.get('act', "")
            newLink = json.loads(linkStr, encoding="utf-8")
            return linkUtils.dispacthLink(newLink, actionStr)



# 给节点增加一个属性
@editor.route('/addproperty', methods=['POST'])
def addNodeProperty():
    if request.method == 'POST':
        nodesStr = request.values.get('nodes', "")
        property_name = request.values.get('property_name', "")
        property_value = request.values.get('property_value', "")
        all_nodes = json.loads(nodesStr, encoding="utf-8")
        if property_name != "":
            for node_obj in all_nodes:
                nodeUtils.addProperty(node_obj=node_obj, property_name=property_name, property_value=property_value)
        return ''


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