#!/usr/bin/env python
#coding:utf8

from models import graph
from igraph import Graph as IGraph


# def findCommunities():

# 角色节点创建一个pagerank属性
query = '''
MATCH (c1:Character)-[r]->(c2:Character)
RETURN c1.name, c2.name, r.weight AS weight
'''

ig = IGraph.TupleList(graph.run(query), weights=True)

pageRank = ig.pagerank()
pgvs = []
for p in zip(ig.vs, pageRank):
    print(p)
    pgvs.append({"name": p[0]["name"], "pg": p[1]})
pgvs
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