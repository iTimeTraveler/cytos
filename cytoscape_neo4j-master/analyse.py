#!/usr/bin/env python
#coding:utf8

from models import graph
from igraph import Graph as IGraph


# 角色节点创建一个pagerank属性
query = '''
MATCH (c1:Character)-[r]->(c2:Character)
RETURN c1.name, c2.name, r.weight AS weight
'''

ig = IGraph.TupleList(graph.run(query), weights=True)




# 随机游走的社区发现算法
def calculate_communities():
    # pageRank
    pageRank = ig.pagerank()
    pgvs = []
    for p in zip(ig.vs, pageRank):
        print(p)
        pgvs.append({"name": p[0]["name"], "pg": p[1]})
    write_clusters_query = '''
    UNWIND {nodes} AS n
    MATCH (c:Character) WHERE c.name = n.name
    SET c.pagerank = n.pg
    '''
    graph.run(write_clusters_query, nodes=pgvs)

    # 随机游走的社区发现算法
    clusters = IGraph.community_walktrap(ig, weights="weight").as_clustering()
    nodes = [{"name": node["name"]} for node in ig.vs]
    for node in nodes:
        idx = ig.vs.find(name=node["name"]).index
        node["community"] = clusters.membership[idx]

    write_clusters_query = '''
    UNWIND {nodes} AS n
    MATCH (c:Character) WHERE c.name = n.name
    SET c.community = toInt(n.community)
    '''
    graph.run(write_clusters_query, nodes=nodes)
    return



# 度分布
def degree_distribution():
    # dd = ig.degree_distribution()
    mylist = ig.vs.degree()
    ig.vs['name']
    myset = set(mylist)  #myset是另外一个列表，里面的内容是mylist里面的无重复项
    matrix = [[0 for col in range(2)] for row in range(len(myset))]
    m = 0
    for item in myset:
      matrix[m][0] = item
      matrix[m][1] = mylist.count(item)
      m += 1
    return matrix


# 每个人物的度
def degree_of_people():
    temp = {}
    degrees = ig.vs.degree()
    names = ig.vs['name']
    for i in range(0, len(names), 1):
        temp[names[i]] = degrees[i]
    mylist = sorted(temp.iteritems(), key=lambda (k,v): (v,k))
    return mylist

