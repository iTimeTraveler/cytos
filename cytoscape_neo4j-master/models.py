#!/usr/bin/env python
#coding:utf8

from flask import Flask, jsonify
from py2neo import Graph, Node, Relationship


graph = Graph("http://neo4j:panchan@localhost:7474/db/data/")

hideKeys = {'index', 'x', 'y', 'px', 'py', 'temp_index', 'source', 'target', 'left', 'right'}


#节点操作
class MyNode:
    def __init__(self):
        print()

    ##### 更改节点 #####
    def dispacthNode(node_obj, action):
        if action == '1':
            return MyNode.createNode(node_obj)
        elif action == '2':
            return MyNode.deleteNode(node_obj)
        elif action == '3':
            return MyNode.createNode(node_obj)

    # 创建节点
    def createNode(node_obj):
        # 数据库已存在则更新
        if node_obj.has_key('id') and graph.exists(graph.node(node_obj['id'])):
            n = graph.node(node_obj['id'])
            for key in node_obj.keys():
                if key not in hideKeys:
                    n[key] = node_obj[key]
            n.push()
            print("oldNode: %s" % n)
            return ''
        # 不存在则新建
        else:
            newNode = Node(node_obj['label'], name=node_obj['name'])
            for key in node_obj.keys():
                if key not in hideKeys:
                    newNode[key] = node_obj[key]
            h = str(hash(newNode))
            newNode['hash'] = h
            graph.merge(newNode)
            newNode.push()
            print("newNode: %s" % newNode)

            # 返回新增节点的id
            query = '''
            MATCH (n)
            WHERE n.hash = {x} and n.name = {y}
            RETURN n, ID(n) as id
            '''
            result = graph.run(query, x=h, y=node_obj['name']).data()
            print(result)
            return jsonify(result={"uid":result[0]['id']})


    # 删除节点
    def deleteNode(node_obj):
        print("deleteNode: %s" % node_obj)
        query = '''
        MATCH (n)
        WHERE n.name = {x}
        DELETE n
        '''
        graph.run(query, x=node_obj['name'])
        return ''





#关系操作
class MyLink:
    def __init__(link_obj):
        print()

    ##### 更改关系 #####
    def dispacthLink(link_obj, action):
        if action == '1':
            return MyLink.createLink(link_obj)
        elif action == '2':
            return MyLink.deleteLink(link_obj)
        elif action == '3':
            return MyLink.createLink(link_obj)

    # 创建关系
    def createLink(link_obj):
        if not link_obj.has_key('relation'):
            return
        print(link_obj)
        srcNode = Node(link_obj['source']['label'], name=link_obj['source']['name'])
        tarNode = Node(link_obj['target']['label'], name=link_obj['target']['name'])
        newLink = Relationship(srcNode, link_obj['relation'], tarNode)
        MyLink.deleteLink(link_obj)    # 删除已存在的关系
        graph.merge(newLink)
        for key in link_obj.keys():
            if key not in hideKeys:
                newLink[key] = link_obj[key]
        newLink.push()
        return ''

    # 删除关系
    def deleteLink(link_obj):
        print("deleteLink: %s" % link_obj)
        query = '''
        MATCH (n)-[r]->(m)
        WHERE (n.name = {src} and m.name = {tag})
        DELETE r
        '''
        graph.run(query, src=link_obj['source']['name'], tag=link_obj['target']['name'])
        return ''