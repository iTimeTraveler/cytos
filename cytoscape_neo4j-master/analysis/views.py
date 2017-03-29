#!/usr/bin/env python
#coding:utf8


from . import analysis
from analysis.analyse import AnalyseUtils
from flask import render_template, request
from models import  NodeUtils, LinkUtils

# 通过指定路由，返回渲染html页面
# 客户端的URL直接在链接里面
@analysis.route('/demo_force',methods=['GET','POST'])
def demo_force(projectId):
    return render_template('analysis_pages/demo_force.html', navId = "demoforce", projectId=projectId)

@analysis.route('/demo_image',methods=['GET','POST'])
def demo_image(projectId):
    return render_template('analysis_pages/demo_image.html', navId = "demoimage", projectId=projectId)


@analysis.route('/degree_distribute',methods=['GET','POST'])
def degree(projectId):
    analyse_utils = AnalyseUtils(projectId)
    matrix = analyse_utils.degree_distribution()    # 计算得到度分布的二维矩阵
    cdd = analyse_utils.cumulative_degree_distribution()    # 调用函数，计算累计度分布，赋给变量
    dl = analyse_utils.degree_of_people()   # 每个人物的度
    nd = analyse_utils.shortest_path()

    nodes = NodeUtils.getAllNodes(projectId)    # 供和弦图使用
    edges = LinkUtils.getAllLinks(projectId)    # 供和弦图使用

    return render_template('analysis_pages/degree_distribute.html', navId = "degreedistribute", projectId=projectId,
                           matrix = matrix, cumulative_degree = cdd, degreedict = dl, networkdiameter = nd, nodes = nodes, links = edges)


# 提供一个动态路由地址，匹配人物列表页面
@analysis.route('/peoplelist', methods=['GET', 'POST'])
def getGraph(projectId):
    nodes = NodeUtils.getAllNodes(projectId)    # 得到所有人物属性

    return render_template('analysis_pages/peoplelist.html', nodes = nodes, navId = "peoplelist", projectId=projectId)


# 重新计算划分社区
@analysis.route('/calculate_communities', methods=['GET'])
def calculateCommunities(projectId):
    analysis_utils = AnalyseUtils(projectId)    # 实例化类
    analysis_utils.calculate_communities()      # 调用函数 随机游走社区发现算法
    return ''