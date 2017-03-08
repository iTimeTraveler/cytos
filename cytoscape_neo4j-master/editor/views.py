#!/usr/bin/env python
#coding:utf8

from . import editor
from models import NodeUtils, LinkUtils, GraphUtils ,graph
from flask import render_template, request, json, jsonify
import sys

# 防止中文编译不过
reload(sys)
sys.setdefaultencoding("utf-8")

nodeUtils = NodeUtils()
linkUtils = LinkUtils()
graphUtils = GraphUtils()

@editor.route('/',methods=['GET','POST'])
def getEditor(projectId):
    communities = GraphUtils.countCommunityPeoples(projectId)
    return render_template('editor_pages/index.html', navId = "editor", projectId=projectId, communities = communities)


# 修改节点或关系
@editor.route('/modify', methods=['POST'])
def modify(projectId):
    if request.method == 'POST':
        if request.values.get('type', "") == 'node':
            nodeStr = request.values.get('node', "")
            actionStr = request.values.get('act', "")
            newNode = json.loads(nodeStr, encoding="utf-8")
            return nodeUtils.dispacthNode(projectId, newNode, actionStr)
        elif request.values.get('type', "") == 'link':
            linkStr = request.values.get('link', "")
            actionStr = request.values.get('act', "")
            newLink = json.loads(linkStr, encoding="utf-8")
            return linkUtils.dispacthLink(projectId, newLink, actionStr)



# 给节点增加一个属性
@editor.route('/addproperty', methods=['POST'])
def addNodeProperty(projectId):
    if request.method == 'POST':
        nodesStr = request.values.get('nodes', "")
        property_name = request.values.get('property_name', "")
        property_value = request.values.get('property_value', "")
        all_nodes = json.loads(nodesStr, encoding="utf-8")
        if property_name != "":
            for node_obj in all_nodes:
                nodeUtils.addProperty(node_obj=node_obj, property_name=property_name, property_value=property_value)
        return ''


# 删除整个图谱
@editor.route('/delete_graph', methods=['POST'])
def deleteAllGraph(projectId):
    if request.method == 'POST':
        LinkUtils.deleteAllLinks(projectId)
        NodeUtils.deleteAllNodes(projectId)
        return ''


# 提供一个动态路由地址，供前端网页调用
@editor.route('/graph', methods=['GET', 'POST'])
def get_graph(projectId):
    nodes = NodeUtils.getAllNodes(projectId)
    edges = LinkUtils.getAllLinks(projectId)

    return jsonify(elements = {"nodes": nodes, "edges": edges}) #把处理好的数据，整理成json格式，然后返回给客户端