#!/usr/bin/env python
#coding:utf8

from . import studentAct
from models import StudentAct
from flask import render_template

@studentAct.route('/studentact',methods=['GET','POST'])
def studentact():
    return render_template('secondPages/student_act/mainpage.html')

@studentAct.route('/partone',methods=['GET','POST'])
def studentact_partone():
    studentact = StudentAct.query.filter_by(student_sort=u'论文专利').all()
    return render_template('secondPages/student_act/stuact-partone.html',studentact=studentact)

@studentAct.route('/thirdPage/<stuactID>',methods=['GET','POST'])
def studentact_thirdPage(stuactID):
    stuactinfo = StudentAct.query.filter_by(id = stuactID).first()
    return render_template('thirdPages/student_act.html',stuactinfo=stuactinfo)

@studentAct.route('/parttwo',methods=['GET','POST'])
def studentact_parttwo():
    studentact = StudentAct.query.filter_by(student_sort=u'科研项目').all()
    return render_template('secondPages/student_act/stuact-parttwo.html',studentact=studentact)

