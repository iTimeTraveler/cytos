# coding=utf-8
from flask import Flask, jsonify, json, render_template, request, current_app
# 导入py2neo包里的graph（图数据库）
from py2neo import Graph, Node, Relationship

# 连接到neo4j相应数据库
app = Flask(__name__)
graph = Graph("http://neo4j:panchan@localhost:7474/db/data/")

count = 0

# 对数据库里取出来的节点进行包装（这里是规范一下数据的格式）
def wrapNodes(nodeRecord):
    global count
    count += 1
    data = {"id": count, "nid": nodeRecord['n'].__name__, "label": next(iter(nodeRecord['n'].labels()))}  # 对每一个节点都构造包装成一个这样的格式
    data.update(nodeRecord['n'].properties)

    return data

# 对数据库里取出来的关系进行包装（这里也是规范一下数据的格式）
def wrapEdges(relationRecord):
    data = {"id": relationRecord['r'].__uuid__,
            "source": relationRecord['r'].start_node()['name'],
            "target": relationRecord['r'].end_node()['name'],
            "relation": str(relationRecord['r'].type())}  # 对每一个关系都构造包装成一个这样的格式， str()是一个方法，把括号里的参数转换为字符串类型

    return data


# 更改节点
def dispacthNode(node_obj, action):
    if action == '1':
        createNode(node_obj)
    elif action == '2':
        deleteNode(node_obj)
    elif action == '3':
        deleteNode(node_obj)

# 更改关系
def dispacthLink(link_obj, action):
    if action == '1':
        createLink(link_obj)
    elif action == '2':
        deleteLink(link_obj)
    elif action == '3':
        deleteLink(link_obj)

# 创建节点
def createNode(node_obj):
    newNode = Node(node_obj['label'], name=node_obj['name'])
    if not graph.exists(newNode):
        print(newNode)
        graph.merge(newNode)


# 删除节点
def deleteNode(node_obj):
    query = '''
    MATCH (n)
    WHERE n.name = {x}
    DELETE n
    '''
    graph.run(query, x=node_obj['name'])


# 创建关系
def createLink(link_obj):
    if not link_obj.has_key('relation'):
        return

    srcNode = Node(link_obj['source']['label'], name=link_obj['source']['name'])
    tarNode = Node(link_obj['target']['label'], name=link_obj['target']['name'])
    newLink = Relationship(srcNode, link_obj['relation'], tarNode)
    if not graph.exists(newLink):
        print(newLink)
        graph.merge(newLink)

# 删除关系
def deleteLink(link_obj):
    query = '''
    MATCH (n)-[r:INTERACTS]->(m)
    WHERE (n.name = {src} and m.name = {tag})
    DELETE r
    '''
    graph.run(query, src=link_obj['source']['name'], tag=link_obj['target']['name'])

# 服务器的根路径
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('demo.html')

    if request.method == 'POST':
        if request.values.get('type', "") == 'node':
            nodesStr = request.values.get('node', "")
            actionStr = request.values.get('act', "")
            newNode = json.loads(nodesStr, encoding="utf-8")
            dispacthNode(newNode, actionStr)
        elif request.values.get('type', "") == 'link':
            linksStr = request.values.get('link', "")
            actionStr = request.values.get('act', "")
            newLink = json.loads(linksStr, encoding="utf-8")
            dispacthLink(newLink, actionStr)

        # nodesStr = request.values.get('node', "")
        # nodesDict = json.loads(nodesStr, encoding="utf-8")
        # map(createNode, nodesDict)
        #
        # linksStr = request.values.get('link', "")
        # linksDict = json.loads(linksStr, encoding="utf-8")
        # map(createLink, linksDict)
        print("over...")
        return render_template('demo.html')






# 提供一个动态路由地址，供前端网页调用
@app.route('/graph', methods=['GET', 'POST'])
def get_graph():
    global count
    count = 0
    nodes = map(wrapNodes, graph.run('MATCH (n:Character) RETURN n').data())  # 从数据库里取出所有节点，交给buildNodes函数加工处理
    edges = map(wrapEdges, graph.run('MATCH ()-[r:INTERACTS]->() RETURN r').data())  # 从数据库里取出所有关系，交给buildEdges加工处理

    return jsonify(elements = {"nodes": nodes, "edges": edges}) #把处理好的数据，整理成json格式，然后返回给客户端


# 启动server服务器
if __name__ == '__main__':
    # app.run(debug = True)
    app.run(port=2000)