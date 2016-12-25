#!/usr/bin/env python
#coding:utf8

from . import teachers
from models import Teachers
from flask import render_template

@teachers.route('/teacherinfo',methods=['GET','POST'])
def teacherInfo():
    return render_template('secondPages/teachers/mainpage.html')

@teachers.route('/partone',methods=['GET','POST'])
def teachers_partone():
    teacherinfo = Teachers.query.filter_by(teachers_sort=u'教授').order_by('orderid asc')
    return render_template('secondPages/teachers/teacher-partone.html',teacherinfo=teacherinfo)

@teachers.route('/thirdPage/<teachersID>',methods=['GET','POST'])
def teachers_thirdPage(teachersID):
    teacherinfo = Teachers.query.filter_by(id = teachersID).first()
    return render_template('thirdPages/teachers.html',teacherinfo=teacherinfo)

@teachers.route('/parttwo',methods=['GET','POST'])
def teachers_parttwo():
    teacherinfo = Teachers.query.filter_by(teachers_sort=u'副教授').order_by('orderid asc')
    return render_template('secondPages/teachers/teacher-parttwo.html',teacherinfo=teacherinfo)

@teachers.route('/partthree',methods=['GET','POST'])
def teachers_partthree():
    teacherinfo = Teachers.query.filter_by(teachers_sort=u'讲师').order_by('orderid asc')
    return render_template('secondPages/teachers/teacher-partthree.html',teacherinfo=teacherinfo)
