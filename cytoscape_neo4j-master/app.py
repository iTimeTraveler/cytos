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
    data = {"source": relationRecord['r'].start_node()['name'],
            "target": relationRecord['r'].end_node()['name'],
            "relation": str(relationRecord['r'].type())}  # 对每一个关系都构造包装成一个这样的格式， str()是一个方法，把括号里的参数转换为字符串类型

    return data



# 创建节点
def createNode(nodeObj):
    # print(nodeObj['name'], nodeObj['id'])
    newNode = Node(nodeObj['label'], name=nodeObj['name'])
    if not graph.exists(newNode):
        print(newNode)
        graph.merge(newNode)

# 创建关系
def createLink(linkObj):
    if not linkObj.has_key('relation'):
        return

    srcNode = Node(linkObj['source']['label'], name=linkObj['source']['name'])
    tarNode = Node(linkObj['target']['label'], name=linkObj['target']['name'])

    newLink = Relationship(srcNode, linkObj['relation'], tarNode)
    if not graph.exists(newLink):
        print(newLink)
        graph.merge(newLink)


# 服务器的根路径
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # # 定义相关节点
        # nicole = Node("Character", name="Nicole", age=24)
        # drew = Node("Character", name="Drew", age=20)
        # # 创建节点
        # graph.merge(nicole | drew)
        # # 创建关系
        # graph.merge(Relationship(nicole, "INTERACTS", drew))
        #
        # # 是否已存在
        # if graph.exists(nicole):
        #     print "exists Node nicole"

        return render_template('demo.html')

    if request.method == 'POST':
        nodesStr = request.values.get('nodes', "")
        nodesDict = json.loads(nodesStr, encoding="utf-8")
        map(createNode, nodesDict)

        linksStr = request.values.get('links', "")
        linksDict = json.loads(linksStr, encoding="utf-8")
        map(createLink, linksDict)
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