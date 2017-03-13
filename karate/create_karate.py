from igraph  import *
from py2neo import Graph as pGraph

g=Graph.Read_GML('karate.gml')

pgraph = pGraph("http://neo4j:panchan@localhost:7474/db/data/")

# 如果存在先删除
pgraph.run('''MATCH p=()-[r:KARATE]->() delete p''')

nodes = g.vs
for node in nodes:
	query='''
	CREATE (n:No3{}'''.format('{name:\'' + str(int(node['id']))+ '\'}') + ''')
	'''
	pgraph.run(query)


edges = g.es
for edge in edges:
	query='''
	MATCH (a:No3{}'''.format('{name:\'' + str(int(edge.source) + 1) + '\'}') + '''), 
					(b:No3{}'''.format('{name:\'' + str(int(edge.target) + 1) + '\'}') + ''')
	CREATE (a)-[r:KARATE]->(b)
	'''
	print query
	pgraph.run(query)
