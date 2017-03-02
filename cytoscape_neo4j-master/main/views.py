#!/usr/bin/env python
#coding:utf8

from . import main
from analysis.analyse import *
from flask import render_template, request, json

@main.route('/',methods=['GET','POST'])
def home():
    calculate_communities()
    return render_template('main/index.html', navId = "main")