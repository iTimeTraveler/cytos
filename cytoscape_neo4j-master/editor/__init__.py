#!/usr/bin/env python
#coding:utf8
from flask import Blueprint

# 实例化一个蓝本类，赋值给editor变量
editor = Blueprint('editor',__name__)

from editor import views
from editor import uploadfiles
