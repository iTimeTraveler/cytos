#!/usr/bin/env python
#coding:utf8

from . import classes
from models import Classes
from flask import render_template

@classes.route('/classesmian',methods=['GET','POST'])
def classesmain():
    return render_template('secondPages/classes/mainpage.html')

@classes.route('/partone',methods=['GET','POST'])
def classes_partone():
    classinfo = Classes.query.filter_by(classes_sort=u'本科')
    return render_template('secondPages/classes/class-partone.html',classinfo=classinfo)

@classes.route('/thirdPage/<classesID>',methods=['GET','POST'])
def classes_thirdPage(classesID):
    classinfo = Classes.query.filter_by(id = classesID).first()
    return render_template('thirdPages/classes.html',classinfo=classinfo)

@classes.route('/parttwo',methods=['GET','POST'])
def classes_parttwo():
    classinfo = Classes.query.filter_by(classes_sort=u'硕士')
    return render_template('secondPages/classes/class-parttwo.html',classinfo=classinfo)

@classes.route('/partthree',methods=['GET','POST'])
def classes_partthree():
    classinfo = Classes.query.filter_by(classes_sort=u'学生活动')
    return render_template('secondPages/classes/class-partthree.html',classinfo=classinfo)

@classes.route('/partfour',methods=['GET','POST'])
def classes_partfour():
    classinfo = Classes.query.filter_by(classes_sort=u'优秀硕士毕业生')
    return render_template('secondPages/classes/class-partfour.html',classinfo=classinfo)



