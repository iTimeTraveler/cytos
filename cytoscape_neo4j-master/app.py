#!/usr/bin/env python
#coding:utf8

from flask import Flask, redirect, url_for
from analysis.analyse import AnalyseUtils


# 连接到neo4j相应数据库
app = Flask(__name__)


from main import main as main_blueprint     # 蓝本类，调用实例对象，将网址分模块处理
app.register_blueprint(blueprint=main_blueprint, url_prefix='/')
from editor import editor as editor_blueprint
app.register_blueprint(blueprint=editor_blueprint, url_prefix='/<projectId>/editor')
from analysis import analysis as analysis_blueprint
app.register_blueprint(blueprint=analysis_blueprint, url_prefix='/<projectId>/analysis')



@app.route('/')
def index():
    return redirect(url_for('main.home'))

# 路由重定向，全部交给geteditor处理
@app.route('/<projectId>/')
def select_project(projectId):
    if not str(projectId).startswith('No'):
        return ''
    return redirect(url_for('editor.getEditor', projectId=projectId))


# 启动server服务器
if __name__ == '__main__':
    # app.run(debug = True)
    app.run(port=2000, debug = True)    # 显示调试信息