#!/usr/bin/env python
#coding:utf8

from flask import jsonify
from py2neo import Graph, Node, Relationship


graph = Graph("http://neo4j:panchan@localhost:7474/db/data/")

hideKeys = {'id', 'label', 'index', 'x', 'y', 'px', 'py', 'temp_index', 'source', 'target', 'left', 'right', 'hash', 'fixed'}


#节点操作
class NodeUtils:
    def __init__(self):
        return

    # 取出所有节点
    @staticmethod
    def getAllNodes(projectId):
        query='''
        MATCH (n:{}'''.format(projectId) + ''')
        RETURN n,ID(n) as id
        '''
        allnodes = map(NodeUtils.wrapNodes, graph.run(query).data())  # 从数据库里取出所有节点，交给buildNodes函数加工处理
        return allnodes

    # 对数据库里取出来的节点进行包装（这里是规范一下数据的格式）
    @staticmethod
    def wrapNodes(nodeRecord):
        data = {"id": nodeRecord['id'], "label": next(iter(nodeRecord['n'].labels())), "weight": 1}  # 对每一个节点都构造包装成一个这样的格式
        data.update(nodeRecord['n'].properties)
        return data


    ##### 更改节点 #####
    def dispacthNode(self, projectId, node_obj, action):
        if action == '1':
            return self.createNode(projectId, node_obj)
        elif action == '2':
            return self.deleteNode(projectId, node_obj)
        elif action == '3':
            return self.createNode(projectId, node_obj)

    # 创建节点
    def createNode(self, projectId, node_obj):
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
            print(node_obj)
            newNode = Node('Character', name=node_obj['name'])
            for key in node_obj.keys():
                if key not in hideKeys:
                    newNode[key] = node_obj[key]
            newNode.add_label(str(projectId))
            h = str(hash(newNode))
            newNode['hash'] = h
            graph.merge(newNode)
            newNode.push()
            print("新增节点: %s" % newNode)

            # 返回新增节点的id
            query = '''
            MATCH (n:{}'''.format(projectId) + ''')
            WHERE n.hash = {x} and n.name = {y}
            RETURN n, ID(n) as id
            '''
            result = graph.run(query, x=h, y=node_obj['name']).data()
            print(result)
            return jsonify(result={"uid":result[0]['id']})

    # 删除节点
    def deleteNode(self, projectId, node_obj):
        query = '''
        MATCH (n:{}'''.format(projectId) + ''')
        WHERE ID(n) = {x}
        DELETE n
        '''
        graph.run(query, x=node_obj['id'])
        return ''

    # 删除全部节点
    @staticmethod
    def deleteAllNodes(projectId):
        query = '''
        MATCH (n:{}'''.format(projectId) + ''')
        DELETE n
        '''
        graph.run(query)
        return ''

    # 全部节点添加一个属性
    def addProperty(self, node_obj, property_name, property_value):
        # 数据库是否存在节点
        if node_obj.has_key('id') and graph.exists(graph.node(node_obj['id'])):
            n = graph.node(node_obj['id'])
            if not n.has_key(property_name) and property_name not in hideKeys:
                n[property_name] = property_value
            n.push()
            print("添加一个属性后: %s" % n)

    # 全部节点删除一个属性
    def removeProperty(self, projectId, property_name):
        query = '''
        MATCH (n:{}'''.format(projectId) + ''')
        REMOVE n.{x}
        '''
        graph.run(query, x=property_name)
        return ''





#关系操作
class LinkUtils:
    def __init__(self):
        return

    # 取出所有关系
    @staticmethod
    def getAllLinks(projectId):
        query = '''
        MATCH (a:{}'''.format(projectId) + ''')-[r]->(b:{}'''.format(projectId) + ''')
        RETURN r,ID(r) as id, ID(a) as sid, ID(b) as tid, a.name AS sname, b.name AS tname
        '''
        alllinks = map(LinkUtils.wrapEdges, graph.run(query).data())  # 从数据库里取出所有关系，交给buildEdges加工处理
        return alllinks

    # 对数据库里取出来的关系进行包装（这里也是规范一下数据的格式）
    @staticmethod
    def wrapEdges(relationRecord):
        data = {"id": relationRecord['id'],
                "source": relationRecord['sid'],
                "target": relationRecord['tid'],
                "sname": relationRecord['sname'],
                "tname": relationRecord['tname'],
                "weight": relationRecord['r']['weight'] if relationRecord['r']['weight'] else 1,
                "relation": str(relationRecord['r'].type())}  # 对每一个关系都构造包装成一个这样的格式， str()是一个方法，把括号里的参数转换为字符串类型
        data.update(relationRecord['r'].properties)
        return data

    ##### 更改关系 #####
    def dispacthLink(self, projectId, link_obj, action):
        if action == '1':
            return self.createLink(projectId, link_obj)
        elif action == '2':
            return self.deleteLink(projectId, link_obj)
        elif action == '3':
            return self.createLink(projectId, link_obj)

    # 创建关系
    def createLink(self, projectId, link_obj):
        if not link_obj.has_key('relation'):
            return
        print(link_obj)
        srcNode = graph.node(int(link_obj['source']['id']))
        tarNode = graph.node(int(link_obj['target']['id']))
        newLink = Relationship(srcNode, 'CONNECT', tarNode)
        self.deleteLink(projectId, link_obj)    # 删除已存在的关系
        graph.merge(newLink)
        for key in link_obj.keys():
            if key not in hideKeys:
                newLink[key] = link_obj[key]
        newLink.push()
        return ''

    # 删除关系
    def deleteLink(self, projectId, link_obj):
        print("deleteLink: %s" % link_obj)
        query = '''
        MATCH (n:{}'''.format(projectId) + ''')-[r]->(m:{}'''.format(projectId) + ''')
        WHERE (n.name = {src} and m.name = {tag})
        DELETE r
        '''
        graph.run(query, src=link_obj['source']['name'], tag=link_obj['target']['name'])
        return ''

    # 删除所有关系
    @staticmethod
    def deleteAllLinks(projectId):
        query = '''
        MATCH (a:{}'''.format(projectId) + ''')-[r]-(b:{}'''.format(projectId) + ''')
        DELETE r
        '''
        graph.run(query)
        return ''



class GraphUtils:
    def __init__(self):
        return

    # Number of Nodes: 50013
    # Number of Relationships: 4
    # Number of Labels: 4
    # Number of Relationships Types: 2
    # Number of Property Keys: 9
    # Number of Constraints:2
    # Number of Indexes: 7
    # Number of Procedures: 215
    def getInfo(self):
        query='''
        match (n) return 'Number of Nodes: ' + count(n) as output UNION
        match ()-[]->() return 'Number of Relationships: ' + count(*) as output UNION
        CALL db.labels() YIELD label RETURN 'Number of Labels: ' + count(*) AS output UNION
        CALL db.relationshipTypes() YIELD relationshipType  RETURN 'Number of Relationships Types: ' + count(*) AS output UNION
        CALL db.propertyKeys() YIELD propertyKey  RETURN 'Number of Property Keys: ' + count(*) AS output UNION
        CALL db.constraints() YIELD description RETURN 'Number of Constraints:' + count(*) AS output UNION
        CALL db.indexes() YIELD description RETURN 'Number of Indexes: ' + count(*) AS output UNION
        CALL dbms.procedures() YIELD name RETURN 'Number of Procedures: ' + count(*) AS output
        '''
        graph.run(query)

    # 获取所有节点的Labels
    def getNodeLabels(self):
        return graph.node_labels

    # 社区数量
    def countCommunities(self, projectId):
        query = '''
        MATCH (n:{}'''.format(projectId) + ''')
        RETURN distinct n.community AS index, count(*) as count
        ORDER BY n.community ASC
        '''
        count = graph.run(query).data()
        return count




class ProjectUtils:
    def __init__(self):
        return

    # 创建一个影视剧项目
    def createOne(self, prjname):
        query = '''
        CREATE (p:Project{name: \'''' + str(prjname) + '''\'})
        RETURN ID(p) as pid
        '''
        pid = graph.run(query).data()[0]['pid']

        info_query = '''
        MATCH (p:Project)
        RETURN max(p.no) as max_no
        '''
        max_no = graph.run(info_query).data()[0]['max_no']
        if max_no is None:
            max_no = 0
        new_prj_node = graph.node(pid)
        new_prj_node['no'] = (max_no + 1)
        new_prj_node['prj_id'] = "No" + str(max_no + 1)
        new_prj_node.push()
        return pid

    # 删除一个影视剧项目
    def deleteOne(self, pid):
        prj_node = graph.node(int(pid))
        if prj_node is not None:
            LinkUtils.deleteAllLinks(prj_node['prj_id'])
            NodeUtils.deleteAllNodes(prj_node['prj_id'])
            graph.delete(prj_node)

    # 获取所有的影视剧
    def getAllProjects(self):
        query = '''
        MATCH (p:Project)
        RETURN p, ID(p) as pid
        '''
        return graph.run(query).data()