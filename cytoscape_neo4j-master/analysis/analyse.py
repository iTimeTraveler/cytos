#!/usr/bin/env python
#coding:utf8

from models import graph
from igraph import Graph as IGraph  # 从igraph这个文件里面引入Graph类
import sys

# 防止中文编译不过
reload(sys)
sys.setdefaultencoding("utf-8")


class AnalyseUtils:
    def __init__(self, projectId):
        self.projectId = projectId

        # 角色节点创建一个pagerank属性
        query = '''
        MATCH (c1:{}'''.format(projectId) + ''')-[r]->(c2:{}'''.format(projectId) + ''')
        RETURN ID(c1), ID(c2), r.weight AS weight
        '''
        self.ig = IGraph.TupleList(graph.run(query), weights=True)


    # 随机游走的社区发现算法
    def calculate_communities(self):
        # pageRank
        pageRank = self.ig.pagerank()     # 通过ig里面的PageRank（）函数直接计算出PageRank值，表示权重？
        pgvs = []
        for p in zip(self.ig.vs, pageRank):
            print(p)
            pgvs.append({"id": p[0]["name"], "pg": p[1]})
        write_clusters_query = '''
        UNWIND {nodes} AS n ''' + '''
        MATCH (c:{}'''.format(self.projectId) + ''')
        WHERE ID(c) = n.id
        SET c.pagerank = n.pg
        '''
        graph.run(write_clusters_query, nodes=pgvs)

        # 随机游走的社区发现算法
        clusters = IGraph.community_walktrap(self.ig, weights=None).as_clustering()     # 通过IGraph.community_walktra（）函数计算
        nodes = [{"id": node["name"], "tmp_index": node.index} for node in self.ig.vs]
        print(nodes)
        for n in nodes:
            print(n)
            idx = n["tmp_index"]
            n["community"] = clusters.membership[idx] + 1   # 社区编号从1开始，而不是0

        write_clusters_query = '''
        UNWIND {nodes} AS n ''' + '''MATCH (c:{projectId}'''.format(projectId=self.projectId) + ''')
        WHERE ID(c) = n.id
        SET c.community = toInt(n.community)
        '''
        graph.run(write_clusters_query, nodes=nodes)
        return



    # 度分布
    def degree_distribution(self):
        mylist = self.ig.vs.degree(type="in")
        myset = set(mylist)  #myset是另外一个列表，里面的内容是mylist里面的无重复项
        matrix = [[0 for col in range(2)] for row in range(len(myset))]
        m = 0
        for item in myset:
          matrix[m][0] = item
          matrix[m][1] = round(mylist.count(item)/float(len(mylist)), 3)
          m += 1
        return matrix


    # 累积度分布
    def cumulative_degree_distribution(self):
        mylist = self.ig.vs.degree()
        myset = set(mylist)  # myset是另外一个列表，里面的内容是mylist里面的无重复项
        matrix = [[0 for col in range(2)] for row in range(len(myset))]
        m = 0
        for item in myset:
            new_list = [i for i in mylist if i >= item]
            matrix[m][0] = item
            matrix[m][1] = round(len(new_list) / float(len(mylist)), 3)
            m += 1
        return matrix


    # 每个人物的度
    def degree_of_people(self):
        temp = {}
        degrees = self.ig.vs.degree()
        names = [graph.node(i)['name'] for i in self.ig.vs['name']]
        for i in range(0, len(names), 1):
            temp[names[i]] = degrees[i]
        mylist = sorted(temp.iteritems(), key=lambda (k,v): (v,k))
        return mylist


    # 图（网络）的直径
    def diameter_of_network(self):
        query = '''
        MATCH (a:Character), (b:Character) WHERE id(a) > id(b)
        MATCH p=shortestPath((a)-[:INTERACTS*]-(b))
        RETURN length(p) AS len, extract(x IN nodes(p) | x.name) AS path
        ORDER BY len DESC LIMIT 4
        '''
        return graph.run(query).data()


    # 最短路径
    def shortest_path(self):
        query = '''
        MATCH (catelyn:Character {name: "Catelyn"}), (drogo:Character {name: "Drogo"})
        MATCH p=shortestPath((catelyn)-[INTERACTS*]-(drogo))
        RETURN p
        '''
        return graph.run(query).data()


    # 关键节点
    def pivotal_nodes(self):
        query = '''
        MATCH (a:Character), (b:Character)
        MATCH p=allShortestPaths((a)-[:INTERACTS*]-(b)) WITH collect(p) AS paths, a, b
        MATCH (c:Character) WHERE all(x IN paths WHERE c IN nodes(x)) AND NOT c IN [a,b]
        RETURN a.name, b.name, c.name AS PivotalNode SKIP 490 LIMIT 10
        '''
        return graph.run(query).data()
