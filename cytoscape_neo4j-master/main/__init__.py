#!/usr/bin/env python
#coding:utf8

from flask import Blueprint

main = Blueprint('main',__name__)   # 实例化一个蓝本类对象

from main import views
