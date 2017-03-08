#!/usr/bin/env python
#coding:utf8

from . import editor
from models import NodeUtils, LinkUtils, GraphUtils ,graph
from flask import render_template, request, json, jsonify
import sys

# 防止中文编译不过
# 路由就表示为用户请求的URL（网址）找出其对应的处理函数之意，建立他们之间的映射
reload(sys)
sys.setdefaultencoding("utf-8")

nodeUtils = NodeUtils()
linkUtils = LinkUtils()
graphUtils = GraphUtils()


# 渲染模板 ：转到编辑界面那个HTML
@editor.route('/',methods=['GET','POST'])
def getEditor(projectId):
    communities = GraphUtils.countCommunityPeoples(projectId)
    return render_template('editor_pages/index.html', navId = "editor", projectId=projectId, communities = communities)


# 修改节点或关系
@editor.route('/modify', methods=['POST'])
def modify(projectId):
    if request.method == 'POST':
        if request.values.get('type', "") == 'node':
            nodeStr = request.values.get('node', "")    # 把客户端的请求信息里的值取出来赋给nodeStr变量
            actionStr = request.values.get('act', "")
            newNode = json.loads(nodeStr, encoding="utf-8")
            return nodeUtils.dispacthNode(projectId, newNode, actionStr)    # 调用更改结点函数
        elif request.values.get('type', "") == 'link':
            linkStr = request.values.get('link', "")
            actionStr = request.values.get('act', "")
            newLink = json.loads(linkStr, encoding="utf-8")     # 把节点的字符串信息转换成json格式，方便后期处理
            return linkUtils.dispacthLink(projectId, newLink, actionStr)    # 调用更改关系函数


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
        return ''   # 调用给一个节点添加属性的函数


# 删除整个图谱
@editor.route('/delete_graph', methods=['POST'])
def deleteAllGraph(projectId):
    if request.method == 'POST':
        LinkUtils.deleteAllLinks(projectId)
        NodeUtils.deleteAllNodes(projectId)
        return ''


# 提供一个动态路由地址，获取某个项目的整个图谱（即所有的刷新页面）
@editor.route('/graph', methods=['GET'])
def get_graph(projectId):
    nodes = NodeUtils.getAllNodes(projectId)
    edges = LinkUtils.getAllLinks(projectId)

    return jsonify(elements = {"nodes": nodes, "edges": edges}) #把处理好的数据，整理成json格式，然后返回给客户端