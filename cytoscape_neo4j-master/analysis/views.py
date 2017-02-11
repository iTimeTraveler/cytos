#!/usr/bin/env python
#coding:utf8

from . import analysis
from flask import render_template

@analysis.route('/analysResult',methods=['GET','POST'])
def analysResult():
    return render_template('analysis_pages/index.html')
