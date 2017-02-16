#!/usr/bin/env python
#coding:utf8

from . import main
from flask import render_template, request, json

@main.route('/',methods=['GET','POST'])
def home():
    return render_template('main.html', navId = "main")