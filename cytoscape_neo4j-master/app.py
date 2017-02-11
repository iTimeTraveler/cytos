# coding=utf-8
from flask import Flask, jsonify, json, render_template, redirect, request, url_for, current_app
# 导入py2neo包里的graph（图数据库）
from py2neo import Graph, Node, Relationship


# 连接到neo4j相应数据库
app = Flask(__name__)
graph = Graph("http://neo4j:panchan@localhost:7474/db/data/")


from main import main as main_blueprint
app.register_blueprint(blueprint=main_blueprint,url_prefix='/')
from editor import editor as editor_blueprint
app.register_blueprint(blueprint=editor_blueprint,url_prefix='/editor')
from analysis import analysis as analysis_blueprint
app.register_blueprint(blueprint=analysis_blueprint,url_prefix='/analysis')



@app.route('/')
def index():
    return redirect(url_for('main.home'))


# 启动server服务器
if __name__ == '__main__':
    # app.run(debug = True)
    app.run(port=2000)