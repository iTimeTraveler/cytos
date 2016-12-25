#!/usr/bin/env python
#coding:utf8 

from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

#学院新闻
class CollegeNews(db.Model):
    __tablename__ = 'collegenews'
    id = db.Column(db.Integer,primary_key=True)
    #新闻分类
    news_sort= db.Column(db.String(255))
    #新闻主题标签
    news_lable = db.Column(db.String(255))
    #主题
    news_theme = db.Column(db.String(255))
    #内容()
    news_content = db.Column(db.Text)
    #图片路径
    news_imgsrc = db.Column(db.String(255))
    #结尾内容
    news_endcontent = db.Column(db.Text)
    #上传时间
    news_update = db.Column(db.DateTime)

#师资力量
class Teachers(db.Model):
    __tablename__ = 'teachers'
    #主键id
    id = db.Column(db.Integer,primary_key=True)
    #教师分类
    teachers_sort= db.Column(db.String(255))
    #教师主题标签
    teachers_lable = db.Column(db.String(255))
    #排序id
    orderid =db.Column(db.Integer)
    #内容()
    teachers_content = db.Column(db.Text)
    #图片路径
    teachers_imgsrc = db.Column(db.String(255))
    #结尾内容
    teachers_endcontent = db.Column(db.Text)
    #上传时间
    #teachers_update = db.Column(db.String(255))
    #教师简介
    teachers_brief = db.Column(db.Text)
    #教师头像
    teachers_icon = db.Column(db.String(255))

#学生活动
class StudentAct(db.Model):
    __tablename__ = 'studentact'
    #主键id
    id = db.Column(db.Integer,primary_key=True)
    #活动分类
    student_sort = db.Column(db.String(255))
    #活动主题标签
    student_lable = db.Column(db.String(255))
    #题目
    student_theme = db.Column(db.String(255))
    #内容
    student_content = db.Column(db.Text)
    #图片路径
    student_imgsrc = db.Column(db.String(255))
    #结尾内容
    student_endcontent = db.Column(db.Text)
    #上传时间
    student_update = db.Column(db.DateTime)


class Classes(db.Model):
    __tablename__ = 'classes'
    #主键id
    id = db.Column(db.Integer,primary_key=True)
    #分类
    classes_sort= db.Column(db.String(255))
    #主题标签
    classes_lable = db.Column(db.String(255))
    #主题
    classes_theme = db.Column(db.String(255))
    #内容()
    classes_content = db.Column(db.Text)
    #图片路径
    classes_imgsrc = db.Column(db.String(255))
    #结尾内容
    classes_endcontent = db.Column(db.Text)
    #上传时间
    #classes_update = db.Column(db.String(255))
    #班级简介
    classes_brief = db.Column(db.Text)




























