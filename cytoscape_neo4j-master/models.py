#!/usr/bin/env python
#coding:utf8

from flask import Flask, jsonify
from py2neo import Graph, Node, Relationship


graph = Graph("http://neo4j:panchan@localhost:7474/db/data/")

hideKeys = {'index', 'x', 'y', 'px', 'py', 'temp_index', 'source', 'target', 'left', 'right'}


#节点操作
class NodeUtils:
    global count
    count = 0
    def __init__(self):
        return

    # 对数据库里取出来的节点进行包装（这里是规范一下数据的格式）
    @staticmethod
    def wrapNodes(nodeRecord):
        global count
        data = {"id": nodeRecord['id'], "temp_index": count, "label": next(iter(nodeRecord['n'].labels()))}  # 对每一个节点都构造包装成一个这样的格式
        data.update(nodeRecord['n'].properties)
        count += 1
        return data


    ##### 更改节点 #####
    def dispacthNode(self, node_obj, action):
        if action == '1':
            return self.createNode(node_obj)
        elif action == '2':
            return self.deleteNode(node_obj)
        elif action == '3':
            return self.createNode(node_obj)

    # 创建节点
    def createNode(self, node_obj):
        # 数据库已存在则更新
        if node_obj.has_key('id') and graph.exists(graph.node(node_obj['id'])):
            n = graph.node(node_obj['id'])
            for key in node_obj.keys():
                if key not in hideKeys:
                    n[key] = node_obj[key]
            n.push()
            print("更新节点: %s" % n)
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
            print("新增节点: %s" % newNode)

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
    def deleteNode(self, node_obj):
        print("deleteNode: %s" % node_obj)
        query = '''
        MATCH (n)
        WHERE n.name = {x}
        DELETE n
        '''
        graph.run(query, x=node_obj['name'])
        return ''


    # 添加一个属性
    def addProperty(self, node_obj, property_name, property_value):
        # 数据库是否存在节点
        if node_obj.has_key('id') and graph.exists(graph.node(node_obj['id'])):
            n = graph.node(node_obj['id'])
            if property_name not in hideKeys:
                n[property_name] = property_value
            n.push()
            print("添加一个属性后: %s" % n)
        return ''





#关系操作
class LinkUtils:
    def __init__(self):
        return

    # 对数据库里取出来的关系进行包装（这里也是规范一下数据的格式）
    @staticmethod
    def wrapEdges(relationRecord):
        data = {"id": relationRecord['id'],
                "source": relationRecord['r'].start_node()['name'],
                "target": relationRecord['r'].end_node()['name'],
                "weight": relationRecord['r']['weight'],
                "relation": str(relationRecord['r'].type())}  # 对每一个关系都构造包装成一个这样的格式， str()是一个方法，把括号里的参数转换为字符串类型
        data.update(relationRecord['r'].properties)
        return data

    ##### 更改关系 #####
    def dispacthLink(self, link_obj, action):
        if action == '1':
            return self.createLink(link_obj)
        elif action == '2':
            return self.deleteLink(link_obj)
        elif action == '3':
            return self.createLink(link_obj)

    # 创建关系
    def createLink(self, link_obj):
        if not link_obj.has_key('relation'):
            return
        print(link_obj)
        srcNode = Node(link_obj['source']['label'], name=link_obj['source']['name'])
        tarNode = Node(link_obj['target']['label'], name=link_obj['target']['name'])
        newLink = Relationship(srcNode, link_obj['relation'], tarNode)
        self.deleteLink(link_obj)    # 删除已存在的关系
        graph.merge(newLink)
        for key in link_obj.keys():
            if key not in hideKeys:
                newLink[key] = link_obj[key]
        newLink.push()
        return ''

    # 删除关系
    def deleteLink(self, link_obj):
        print("deleteLink: %s" % link_obj)
        query = '''
        MATCH (n)-[r]->(m)
        WHERE (n.name = {src} and m.name = {tag})
        DELETE r
        '''
        graph.run(query, src=link_obj['source']['name'], tag=link_obj['target']['name'])
        return ''